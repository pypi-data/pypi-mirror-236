import glob
import geopandas as gpd
import pandas as pd
import numpy as np
import pathlib
import multiprocessing as mp
from datetime import datetime, timedelta
from shapely import affinity
from shapely.geometry import LineString
from tqdm import tqdm
from .utils import get_columns, read_geodataframe, calculate_direction, update_progress, save_parquet, find_previous_frame
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def spatial_operations(name_list, read_function, parallel=True):
    '''Function to perform spatial operations between two consecutive time stamps'''
    print('Spatial operations has been started...')
    # Verify files into the output/features directory
    files_list = sorted(glob.glob(name_list['output_path'] + 'features/*.parquet', recursive=True))
    if not files_list:
        print('No files found in the input directory')
        return
    # Extract the timestamp from the path
    tstamp_list = [datetime.strptime(pathlib.Path(x).stem, '%Y%m%d_%H%M') for x in files_list]   
    # Boarder options
    if name_list['board'] == True:
        for files in range(len(files_list)):
            file_path = gpd.read_parquet(files_list[files])
            if len(file_path) > 0:
                file_path = file_path['file'].unique()[0] # Get the file name
                break                
        data_shape = read_function(file_path).shape
        board_1 = gpd.GeoDataFrame({'geometry': [LineString([(data_shape[1], 0),(data_shape[1], data_shape[0])])]})
        board_2 = gpd.GeoDataFrame({'geometry': [LineString([(0, 0),(0, data_shape[0])])]})
    else:
        board_1, board_2, data_shape = None, None, None
    # Number of cores
    if 'n_jobs' not in name_list.keys():
        name_list['n_jobs'] = mp.cpu_count()
    elif name_list['n_jobs'] == -1:
        name_list['n_jobs'] = mp.cpu_count()  
    # Create the progress bar
    pbar = tqdm(total=len(files_list), ncols=80, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [Elapsed:{elapsed} Remaining:<{remaining}]')
    if parallel: # Run parallel
        with mp.Pool(name_list['n_jobs']) as pool:
            for _ in pool.imap_unordered(process_time, [(ctime, tstamp_list, files_list, name_list,
                                                        board_1, board_2, data_shape) for ctime in range(len(tstamp_list))]):
                update_progress(1, pbar)
        pool.close()
    else: # Run serial
        for ctime in range(len(tstamp_list)):
            process_time((ctime, tstamp_list, files_list, name_list, board_1, board_2, data_shape))
            update_progress(1, pbar)
    pbar.close()


def process_time(args):
    """Function to process the spatial operations for a given time stamp"""
    
    current_time, timestamp_list, files_list, name_list, board_1, board_2, data_shape = args
    features_path = name_list['output_path'] + 'features/'
    current_timestamp = timestamp_list[current_time] # Get the current timestamp
    current_file = features_path + current_timestamp.strftime('%Y%m%d_%H%M') + '.parquet' # Get the current file
    current_frame = read_geodataframe(current_file, # Try to read the current file
                                      error_columns=get_columns()['features'] + 
                                      get_columns()['spatial'])
    # Initialize parameters for the current frame
    current_frame['status'] = 'NEW'
    current_frame['prev_idx'] = None
    current_frame['inside_idx'] = None
    current_frame['merge_idx'] = None
    current_frame['split_idx'] = None
    current_frame['dis_'] = 0
    current_frame['dir_'] = np.nan
    current_frame['trajectory'] = LineString().wkt
    current_frame['board'] = False
    current_frame['touching_idx'] = None
    
    if current_frame.empty: # Check if the current frame is empty
        save_parquet(current_frame, current_file)
        return
    # Find previous frame based on the timestamp list and delta tolerance
    dt_time = timedelta(minutes=name_list['delta_time'])
    previous_stamp = current_timestamp - dt_time
    previous_file = features_path + previous_stamp.strftime('%Y%m%d_%H%M') + '.parquet'
    # Check if previous frame exists
    if pathlib.Path(previous_file).exists():
        previous_frame = read_geodataframe(previous_file, get_columns()['features'] + get_columns()['spatial'])
    else: # Try to find previous frame based on the timestamp list and delta tolerance
        previous_frame, previous_stamp, dt_time = find_previous_frame(current_timestamp,
                                                                    current_time, 
                                                                    timestamp_list, 
                                                                    files_list, 
                                                                    name_list,
                                                                    dt_time,
                                                                    error_columns=get_columns()['features'] + get_columns()['spatial']) 
    # Compute the overlays for each threshold
    overlays = [operations(current_frame, previous_frame, threshold, name_list['min_overlap']) for threshold in name_list['thresholds']]
    result = pd.concat(overlays)
    if type(board_1) == gpd.GeoDataFrame: # Check if the boarders are defined
        result = edge_limit(result, board_1, board_2, name_list, data_shape)
    # Save the result
    save_parquet(result, current_file)

def operations(frame1, frame2, threshold, min_overlap):
    """ Perform spatial operations between two dataframes """
    # Get frame inside
    frame_inside = frame1.loc[frame1['threshold'] > threshold]
    frame1 = frame1.loc[frame1['threshold'] == threshold]
    # Check if frame1 is empty
    if frame1.empty:
        return frame1
    # First spatial operations is count of points #####    
    frame1 = count_inside(frame1,
                          frame_inside)
    # Check if frame2 is None
    if frame2 is None:
        return frame1
    if len(frame2) == 0:
        return frame1
    # Set frame2 to same threshold as frame1
    frame2 = frame2.loc[frame2['threshold'] == threshold]
    # Check if frame2 is None
    if frame2.empty:
        return frame1
    # OVERLAY OPERATIONS #######
    overlays = frame1.reset_index().overlay(frame2.reset_index(), how="intersection", keep_geom_type=True)
    overlays["ovrlp_area"] = overlays.area
    overlays["ovrlp_perc1"] = (overlays["ovrlp_area"] * 100) / overlays["size_1"]
    overlays["ovrlp_perc2"] = (overlays["ovrlp_area"] * 100) / overlays["size_2"]
    overlays = overlays.loc[(overlays["ovrlp_perc1"] >= min_overlap) & (overlays["ovrlp_perc2"] >= min_overlap)]
    # Get operations index    
    cont_indx_1, cont_indx_2 = continuous(overlays)
    mergs_idx_1, mergs_idx_2, merge_frame = merge(overlays)
    splits_idx_1, split_prev_idx, new_splts_idx, new_splts_prev_idx  = split(overlays)
    mergs_splits_idx = np.intersect1d(mergs_idx_1, splits_idx_1)
    mergs_splits_idx = np.unique(mergs_splits_idx)
    # Continuous #####
    if len(cont_indx_1) > 0:
        frame1.loc[cont_indx_1,'status'] =  'CON'
        frame1.loc[cont_indx_1, 'prev_idx'] = cont_indx_2
    # Merges #####
    if len(mergs_idx_1) > 0:
        frame1.loc[mergs_idx_1,'status'] =  'MRG'
        frame1.loc[mergs_idx_1,'prev_idx'] =  mergs_idx_2
        frame1.loc[mergs_idx_1,'merge_idx'] =  merge_frame['merge_ids'].values
    # Splits #####
    if len(splits_idx_1) > 0:
        frame1.loc[splits_idx_1,'status'] =  'SPL'
        frame1.loc[splits_idx_1,'prev_idx'] =  split_prev_idx
        frame1.loc[new_splts_idx,'status'] =  'NEW/SPL'
        frame1.loc[new_splts_idx,'split_idx'] =  new_splts_prev_idx
    # Merges/Splits
    if len(mergs_splits_idx) > 0:
        frame1.loc[mergs_splits_idx,'status'] =  'MRG/SPL'
    # WITHIN OPERATIONS #######
    within = frame1.loc[frame1['status'].isnull()].sjoin(frame2, predicate="within", lsuffix="1", rsuffix="2")
    if len(within) > 0:
        within.reset_index(inplace=True)
        within.rename(columns={'index':'index_1'}, inplace=True)
        cont_indx_1, cont_indx_2 = continuous(within)
        splits_idx_1, split_prev_idx, new_splts_idx, new_splts_prev_idx  = split(within)
        if len(cont_indx_1) > 0:
            frame1.loc[cont_indx_1,'status'] =  'CON'
            frame1.loc[cont_indx_1, 'prev_idx'] = cont_indx_2
        if len(splits_idx_1) > 0:
            frame1.loc[splits_idx_1,'prev_idx'] =  split_prev_idx
            frame1.loc[new_splts_idx,'status'] =  'NEW/SPL'
            frame1.loc[new_splts_idx,'split_idx'] =  new_splts_prev_idx
    # CONTAINS OPERATIONS BETWEEN FRAME2 and FRAME1 #######
    contains = frame2.sjoin(frame1.loc[frame1['status'].isnull()], predicate="contains", lsuffix="2", rsuffix="1")
    if len(contains) > 0:
        contains.reset_index(inplace=True)
        contains.rename(columns={'index':'index_2'}, inplace=True)
        cont_indx_1, cont_indx_2 = continuous(contains)
        mergs_idx_1, mergs_idx_2, merge_frame = merge(contains)
        if len(cont_indx_1) > 0:
            frame1.loc[cont_indx_1,'status'] =  'CON'
            frame1.loc[cont_indx_1, 'prev_idx'] = cont_indx_2
        if len( mergs_idx_1) > 0:
            frame1.loc[mergs_idx_1,'status'] =  'MRG'
            frame1.loc[mergs_idx_1,'prev_idx'] =  mergs_idx_2
            frame1.loc[mergs_idx_1,'merge_idx'] =  merge_frame['merge_ids'].values    
    # Add NEW values to status for the ones that are not in any of the previous categories
    frame1.loc[frame1['status'].isnull(),'status'] = 'NEW'
    # Calculate distance between centroids
    frame1['centroid'] = frame1['geometry'].centroid
    frame1['prev_centroid'] = frame1['prev_idx'].apply(lambda x: frame2.loc[x]['geometry'].centroid if x is not None else None)
    frame1['trajectory'] = frame1.apply(lambda x: LineString([x['centroid'], x['prev_centroid']]) if x['prev_centroid'] is not None else None, axis=1)
    frame1['dis_'] = frame1['trajectory'].apply(lambda x: x.length if x is not None else None)
    frame1['dir_'] = frame1['trajectory'].apply(lambda x: calculate_direction(x.coords[-1],x.coords[0]) if x is not None else None)
    # Calculate distance and direction of NEW/SPL
    frame1['prev_geometry_split'] = frame1['split_idx'].apply(lambda x: frame2.loc[x]['geometry'] if x is not None else None)
    frame1['intersec_centroid'] = frame1.apply(lambda x: x['geometry'].intersection(x['prev_geometry_split']).centroid if x['prev_geometry_split'] is not None else None, axis=1)
    frame1['trajectory_split'] = frame1.apply(lambda x: LineString([x['centroid'], x['intersec_centroid']]) if x['intersec_centroid'] is not None else None, axis=1)
    frame1['dis_spl'] = frame1['trajectory_split'].apply(lambda x: x.length if x is not None else None)
    frame1['dir_spl'] = frame1['trajectory_split'].apply(lambda x: calculate_direction(x.coords[-1],x.coords[0]) if x is not None else None)
    # Move values of distance_split to distance
    frame1.loc[frame1['trajectory'].isnull(),'trajectory'] = frame1['trajectory_split']
    # frame1.loc[frame1['dis_'].isnull(),'dis_'] = frame1['dis_spl']
    # frame1.loc[frame1['dir_'].isnull(),'dir_'] = frame1['dir_spl']
    # Fill Trajectory None with LINESTRING EMPTY
    frame1['trajectory'] = frame1['trajectory'].fillna(LineString())
    # Convert trajectory column to string and prevent error in pyarrow type
    frame1['trajectory'] = frame1['trajectory'].astype(str)
    frame1 = frame1.drop(columns=['prev_centroid','centroid', 'prev_geometry_split',
                                  'intersec_centroid','trajectory_split'])
    return frame1

def count_inside(frame_base, frame_inside):
    ''' Count the number of points inside each cluster '''
    if len(frame_inside) > 0:
        frame_inside['geometry'] = frame_inside['geometry'].buffer(-0.01)
        inside_clusters = frame_base[['geometry']].sjoin(frame_inside[['geometry']],
                                                         predicate="contains",
                                                         lsuffix="base", rsuffix="inside").reset_index()
        inside_clusters = inside_clusters.pivot_table(columns=["index","index_inside"], aggfunc="size")
        inside_clusters = inside_clusters.reset_index().groupby('index')['index_inside'].apply(list).to_frame()
        inside_clusters['inside_len'] = inside_clusters['index_inside'].apply(lambda x: len(x))
        frame_base.loc[inside_clusters.index, 'inside_idx'] = inside_clusters['index_inside']
        frame_base.loc[inside_clusters.index, 'inside_clusters'] = inside_clusters['inside_len']
        return frame_base
    else:
        return frame_base

def continuous(operation):
    ''' Get continuous clusters '''
    cont_current = operation.groupby("cluster_id_1").filter(lambda group: group["cluster_id_1"].count() == 1).index.values
    cont_past = operation.groupby("cluster_id_2").filter(lambda group: group["cluster_id_2"].count() == 1).index.values
    conts = np.intersect1d(cont_current, cont_past)
    cont_indx_1 = operation.loc[conts]['index_1'].values
    cont_indx_2 = operation.loc[conts]['index_2'].values
    return cont_indx_1, cont_indx_2

def merge(operation):
    ''' Get merges clusters '''
    mergs_ = np.array(operation[(operation.duplicated(subset=["cluster_id_1"], keep=False)) & ~operation["cluster_id_1"].isnull()].index.values)
    mergs_idx_1 = operation.loc[mergs_]['index_1'].values
    mergs_idx_1 = np.unique(mergs_idx_1)
    # Add complete merge information
    merges_group = operation.loc[mergs_][['index_1','index_2','cluster_id_2','size_2']]
    merges_ids = merges_group.groupby('index_1')['index_2'].apply(list).reset_index(name='merge_ids')
    merge_counts = merges_group.groupby('index_1')['size_2'].apply(list).reset_index(name='merge_counts')
    mergMax_area = merges_group.loc[merges_group.groupby('index_1')['size_2'].idxmax()].reset_index()[['index_1','index_2','cluster_id_2']]
    merge_frame = pd.merge(merges_ids, merge_counts, on='index_1')
    merge_frame = pd.merge(merge_frame, mergMax_area, on='index_1')
    merge_frame = merge_frame.loc[merge_frame['index_1'].isin(mergs_idx_1)]
    mergs_idx_2 = merge_frame['index_2'].values
    return mergs_idx_1, mergs_idx_2, merge_frame

def split(operation):
    """ Get splits clusters """
    splits_ = np.array(operation[(operation.duplicated(subset=["cluster_id_2"], keep=False)) & ~operation["cluster_id_2"].isnull()].index.values)
    splits_idx = operation.loc[splits_]['index_1'].values
    splits_idx = np.unique(splits_idx)
    # Add complete split information
    splits_group = operation.loc[splits_][['index_1','index_2','cluster_id_1','cluster_id_2','size_1']]
    splits_group = splits_group.groupby('cluster_id_2')
    splits_idx = []
    split_prev_idx = []
    new_splts_idx = []
    new_splts_prev_idx = []
    for _, sgroup in splits_group:
        max_count = sgroup['size_1'].max()
        max_idx = sgroup.loc[sgroup['size_1'] == max_count]['index_1'].values
        min_idx = sgroup.loc[sgroup['size_1'] != max_count]['index_1'].values
        splits_idx.append(max_idx[0])
        split_prev_idx.append(sgroup['index_2'].unique()[0])
        new_splts_idx.extend(min_idx)
        new_splts_prev_idx.extend([sgroup['index_2'].unique()[0]]*len(min_idx))
    return splits_idx, split_prev_idx, new_splts_idx, new_splts_prev_idx

def edge_limit(main_features, board_1, board_2, name_list, shape):
    '''Calculate clusters that are touching the boarders'''
    # Get geometries
    geo_boundaries = main_features.loc[main_features['threshold_level'] == 0].copy()
    geo_boundaries = geo_boundaries[["threshold_level","size","geometry"]]
    lef_board = gpd.sjoin(geo_boundaries, board_1, how="inner", predicate="intersects")
    right_board = gpd.sjoin(geo_boundaries, board_2, how="inner", predicate="intersects")  
    if not right_board.empty: # Check if there is any intersected lef_board   
        right_board['geometry'] = right_board['geometry'].apply(affinity.translate, xoff=shape[1])
        touches = gpd.sjoin(lef_board, right_board, how="inner", predicate="touches", lsuffix="1", rsuffix="2")
        # Groupby index of touches
        grouped_touches = touches.groupby(touches.index)
        for _, group in grouped_touches:
            g1 = group[['size_1']].reset_index().drop_duplicates().rename(columns={'size_1':'size'})
            g2 = group[['index_2','size_2']].rename(columns={'index_2':'index','size_2':'size'})
            mrg_g = pd.concat([g1,g2], ignore_index=True).set_index('index')
            # Get index of largest size using argmax
            largest_idx = mrg_g['size'].idxmax()
            other_idx = mrg_g.loc[mrg_g.index != largest_idx].index.values
            # Add touching index to main_features
            main_features.loc[main_features.index.isin(other_idx),'touching_idx'] = largest_idx
            main_features.loc[main_features.index.isin(other_idx),'board'] = True
            # Get prev_idx of largest_idx
            prev_idx = main_features.loc[main_features.index == largest_idx]['prev_idx'].values[0]
            # Add prev_idx to other_idx
            main_features.loc[main_features.index.isin(other_idx),'prev_idx'] = prev_idx
    return main_features