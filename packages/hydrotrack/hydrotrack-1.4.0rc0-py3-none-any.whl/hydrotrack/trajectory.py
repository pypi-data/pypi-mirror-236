import glob
import geopandas as gpd
import pathlib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from shapely.ops import linemerge
from shapely.wkt import loads
from shapely.geometry import MultiLineString
from tqdm import tqdm
from .utils import update_progress, get_columns, find_previous_frame, save_parquet


def trajectory_linking(name_list):
    """ Link trajectories together.
    """
    print('Linking clusters has been started (Serial mode)...')
    # Get features files
    files_list = sorted(glob.glob(name_list['output_path'] + 'features/*.parquet', recursive=True))
    if not files_list:
        print('No files found in the input directory')
        return
    tstamp_list = [datetime.strptime(pathlib.Path(x).stem, '%Y%m%d_%H%M') for x in files_list]
    dt_time = timedelta(minutes=name_list['delta_time'])
    features_path = name_list['output_path'] + 'features/'
    # Create the progress bar
    pbar = tqdm(total=len(files_list), ncols=80, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [Elapsed:{elapsed} Remaining:<{remaining}]')
    # Set initial UID
    uid = 1
    # TODO: Need to refactor iuid max cluster update function
    counter = 0
    # Loop through the files
    for cstamp in range(len(tstamp_list)):
        current_timestamp = tstamp_list[cstamp]# Get the current timestamp
        current_path = features_path + current_timestamp.strftime('%Y%m%d_%H%M') + '.parquet'
        current_frame = gpd.read_parquet(current_path) # Read the current frame
        # Initialize the uid and iuid columns
        current_frame.loc[:, 'uid'] = np.nan
        current_frame.loc[:, 'iuid'] = np.nan
        current_frame.loc[:,'lifetime'] = dt_time
        if current_frame.empty: # Check if the current frame is empty
            update_progress(1, pbar)
            save_parquet(current_frame, current_path)
            continue
        if counter == 0:  # First frame
            current_frame = new_frame(current_frame, uid, dt_time) # Add new clusters
            board_idx = current_frame[(current_frame['board'] == True)]
            if len(board_idx) > 0: # Copy values from touching_idx to board_idx
                current_frame = board_clusters(current_frame, board_idx) # Copy values from touching_idx
            current_frame = refact_inside_uids(current_frame, dt_time) # Refactor inside clusters
            uid = update_max_uid(uid, current_frame['uid'].max() + 1) # Update the max uid
            counter += 1
            save_parquet(current_frame, current_path) # Save the current frame
            update_progress(1, pbar)
            continue
        # Get previous frame to compare with current frame
        previous_stamp = current_timestamp - dt_time
        previous_file = features_path + previous_stamp.strftime('%Y%m%d_%H%M') + '.parquet'
        if pathlib.Path(previous_file).exists():
            previous_frame = gpd.read_parquet(previous_file) # Read the previous frame
        else:
            previous_frame, previous_stamp, dt_time = find_previous_frame(current_timestamp,
                                                                          cstamp,
                                                                          tstamp_list,
                                                                          files_list,
                                                                          name_list,
                                                                          dt_time,
                                                                          error_columns=get_columns()['features'] + \
                                                                                        get_columns()['spatial'] + \
                                                                                        get_columns()['trajectory'])
        # Check if previous frame is empty
        if previous_frame is None: # All clusters are new
            current_frame = new_frame(current_frame, uid, dt_time) # Add new clusters
            board_idx = current_frame[(current_frame['board'] == True)]
            if len(board_idx) > 0: # Copy values from touching_idx to board_idx
                current_frame = board_clusters(current_frame, board_idx) # Copy values from touching_idx
            current_frame = refact_inside_uids(current_frame, dt_time) # Refactor inside clusters
            uid = update_max_uid(uid, current_frame['uid'].max() + 1) # Update the max uid
            counter += 1 # Update the counter
            save_parquet(current_frame, current_path) # Save the current frame
            update_progress(1, pbar) # Update the progress bar
            continue
        # Get prev_idx in current frame are not null
        not_none_current = current_frame.loc[(~current_frame['prev_idx'].isnull()) &
                                             (current_frame['status'] != 'NEW/SPL') &
                                             (current_frame['board'] != True)]
         # All clusters are new at current frame if not_none_current is empty
        if not_none_current.empty:
            current_frame = new_frame(current_frame, uid, dt_time)
            board_idx = current_frame[(current_frame['board'] == True)]
            if len(board_idx) > 0: # Copy values from touching_idx to board_idx
                current_frame = board_clusters(current_frame, board_idx) # Copy values from touching_idx
            current_frame = refact_inside_uids(current_frame, dt_time)
            if np.isnan(current_frame['uid'].max()):
                uid_list = np.arange(uid, uid + len(current_frame), 1, dtype=int)
                iuids = [float(str(uid_list[x]) + '.' + str(x)) for x in range(len(uid_list))]
                current_frame['uid'] = uid_list
                current_frame['iuid'] = iuids
            uid = update_max_uid(uid, current_frame['uid'].max() + 1) # Update the max uid
            counter += 1
            save_parquet(current_frame, current_path) # Save the current frame
            update_progress(1, pbar)
            continue
        # Set previous_frame only are not none['prev_idx']
        c_previous_idx = pd.Index(not_none_current['prev_idx'].values.astype(int))
        previous_uids = previous_frame.loc[c_previous_idx]['uid'].values # Get previous uids
        previous_iuids = previous_frame.loc[c_previous_idx]['iuid'].values # Get previous iuids
        previous_lifetimes = previous_frame.loc[c_previous_idx]['lifetime'].values # Get previous lifetimes
        current_frame.loc[not_none_current.index,'uid'] = previous_uids # Update the uid
        current_frame.loc[not_none_current.index,'iuid'] = previous_iuids # Update the iuid
        current_frame.loc[not_none_current.index,'lifetime'] = current_frame.loc[not_none_current.index,'lifetime'] + previous_lifetimes
        # Get NEW/SPL clusters index in current frame
        new_spl_idx = current_frame[(current_frame['status'] == 'NEW/SPL')]['split_idx'].dropna()
        if len(new_spl_idx) > 0:
            cur_lifetimes = previous_frame.loc[new_spl_idx.values.astype(int)]['lifetime'].values
            current_frame.loc[new_spl_idx.index,'lifetime'] = cur_lifetimes
            current_frame.loc[new_spl_idx.index,'lifetime'] = current_frame.loc[new_spl_idx.index,'lifetime'] + dt_time
        # Merge trajectories between previous_frame and current_frame
        current_frame['trajectory'] = loads(current_frame['trajectory'])
        previous_frame['trajectory'] = loads(previous_frame['trajectory'])
        previous_trajectory = previous_frame.loc[c_previous_idx]['trajectory'].values
        current_trajectory = current_frame.loc[not_none_current.index]['trajectory'].values
        merged_trajectory = [merge_trajectory(current_trajectory[x], previous_trajectory[x]) for x in range(len(current_trajectory))]
        current_frame.loc[not_none_current.index, 'trajectory'] = merged_trajectory # Update the trajectory
        current_frame['trajectory'] = current_frame['trajectory'].astype(str) # Convert to string
        # Add news clusters into to cluster where uid is null
        current_frame = new_frame(current_frame, uid, dt_time) # Add new clusters
        # Get board clusters and Refactored board clusters
        board_idx = current_frame[(current_frame['board'] == True)]
        if len(board_idx) > 0: # Copy values from touching_idx to board_idx
            current_frame = board_clusters(current_frame, board_idx) # Copy values from touching_idx
        current_frame = refact_inside_uids(current_frame, dt_time) # Refactor inside clusters
        uid = update_max_uid(uid, current_frame['uid'].max() + 1) # Update the max uid
        counter += 1 # Update the counter
        save_parquet(current_frame, current_path) # Save the current frame
        update_progress(1, pbar) # Update the progress bar
    pbar.close()

def new_frame(frame, max_uid, time_delta):
    ''' Add new clusters uids to the frame. '''
    new_index = frame.loc[frame['uid'].isnull()].index.values
    if len(new_index) == 0:
        return frame
    # max_uid = max_uid + 1
    uid_list = np.arange(max_uid, max_uid + len(new_index), 1, dtype=int)
    frame.loc[new_index, 'uid'] = uid_list
    frame.loc[frame.lifetime.isnull(), 'lifetime'] = time_delta
    return frame

def update_max_uid(current_max_uid, global_uid):
    ''' Update the max uid. '''
    if current_max_uid < global_uid:
        global_uid = current_max_uid + 1
    else:
        global_uid = current_max_uid
    return global_uid

def refact_inside_uids(frame, delta_time):
    ''' Refactor the inside clusters uids. '''
    # Get the inside index
    insd_inx = frame[(~frame['inside_idx'].isnull())]
    # Lock inside index threshold level 0
    insd_idx_lv0 = insd_inx[insd_inx['threshold_level'] == 0]
    insd_idx_idx = insd_idx_lv0.index
    insd_idx_val = insd_idx_lv0['inside_idx'].values
    for idx, val in zip(insd_idx_idx, insd_idx_val):
        uid_vl = str(int(frame.loc[idx]['uid']))
        for v in val:
            # Check if the rame.loc[v]['iuid'] is not nan
            if ~np.isnan(frame.loc[v]['iuid']):
                if int(frame.loc[v]['iuid']) == int(uid_vl):
                    continue # Skip this iteration
            elif np.isnan(frame.loc[v,'iuid']):
                thld_vl = frame.loc[v]['threshold_level']
                frame.loc[v,'uid'] = int(uid_vl) # Add the uid to the inside index
                frame.loc[v,'iuid'] = float(uid_vl +'.'+'0' * (thld_vl - 1) + str(np.random.randint(1, 999)))
                frame.loc[v,'lifetime'] = delta_time
            else:
                frame.loc[v,'uid'] = int(uid_vl)
    return frame

def merge_trajectory(current_line, previous_line):
    """ Merge two trajectories. """
    if current_line.is_empty:
        return loads('LINESTRING EMPTY')
    if previous_line.is_empty:
        return current_line
    to_merg = []
    if isinstance(previous_line, MultiLineString):
        previous_line = [line for line in previous_line.geoms]
        to_merg.extend(previous_line)
    if isinstance(current_line, MultiLineString):
        current_line = [line for line in current_line.geoms if not line.is_empty]
        to_merg.extend(current_line)
    if len(to_merg) > 0:
        merged = linemerge(to_merg)
    else:
        merged = linemerge([current_line, previous_line])
    return merged

def board_clusters(current_frame, board_idx):
    ''' Copy values from touching_idx to board_idx. '''
    touching_idx = pd.Index(current_frame.loc[board_idx.index]['touching_idx'].values.astype(int))
    board_uids = current_frame.loc[touching_idx]['uid'].values
    board_iuids = current_frame.loc[touching_idx]['iuid'].values
    board_lifetimes = current_frame.loc[touching_idx]['lifetime'].values
    board_status = current_frame.loc[touching_idx]['status'].values
    current_frame.loc[board_idx.index,'uid'] = board_uids
    current_frame.loc[board_idx.index,'iuid'] = board_iuids
    current_frame.loc[board_idx.index,'lifetime'] = board_lifetimes
    current_frame.loc[board_idx.index,'status'] = board_status
    return current_frame