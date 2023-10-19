import glob
import numpy
import os
import sys
import re
import numpy as np
import pandas as pd
import geopandas as gpd
import pathlib
import time
from datetime import datetime, timedelta
from shapely.geometry import LineString
from sklearn.cluster import DBSCAN


def get_filestamp(name_list, path_file):
    file_string = str(pathlib.Path(path_file).name)
    file_pattern = name_list['timestamp_pattern']
    timestamp = datetime.strptime(file_string, file_pattern)
    return timestamp

def set_operator(name_list):
    '''Set the operator to be used'''
    if name_list['operator'] == '>=':
        operator = numpy.greater_equal
    elif name_list['operator'] == '<=':
        operator = numpy.less_equal
    elif name_list['operator'] == '>':
        operator = numpy.greater
    elif name_list['operator'] == '<':
        operator = numpy.less
    elif name_list['operator'] == '==':
        operator = numpy.equal
    elif name_list['operator'] == '!=':
        operator = numpy.not_equal
    else:
        print('Invalid operator')
        sys.exit()
    return operator

def set_dbscan():
    # Set the DBSCAN parameters
    db = DBSCAN(
        algorithm="kd_tree",
        eps=1,
        metric="chebyshev",
        metric_params=None,
        min_samples=3,
        n_jobs=None,
        p=None,
        )
    return db

def get_columns():
    """Get the columns of the dataframe"""
    
    main_columns = dict()
    main_columns['features'] = ['timestamp','cluster_id', 'threshold', 'threshold_level', 
                                'size', 'mean', 'std', 'min', 'Q1', 'Q2', 'Q3', 'max',
                                'file', 'geometry']
    main_columns['spatial'] = ['status','prev_idx','merge_idx','board','touching_idx','split_idx','inside_idx','inside_clusters','dis_', 'dir_','trajectory']
    main_columns['trajectory'] = ['uid','iuid','lifetime']
    main_columns['error_column'] = []
    return main_columns

def read_geodataframe(path_file, error_columns, attempt=2):
    """Read the geodataframe"""
    while attempt > 0:
        try:
            geoframe = gpd.read_parquet(path_file)
            attempt = -1
        except:
            geoframe = gpd.GeoDataFrame(columns=error_columns)
        attempt -= 1
        time.sleep(0.5)
    return geoframe
    
def get_input_files(name_list):
    '''Get the list of files to be processed'''
    files_list = sorted(glob.glob(name_list['input_path'] + '**/*', recursive=True))
    if not files_list:
        print('No files found in the input directory')
        return
    files_list = [f for f in files_list if os.path.isfile(f)]
    return files_list

def save_feather(df, path_file):
    """Save the dataframe as a feather file"""
    df.to_feather(path_file)
    
def save_parquet(df, path_file):
    """Save the dataframe as a parquet file"""
    df.to_parquet(path_file)

def save_array(array, path_file):
    """Save the array as a numpy file"""
    np.savez_compressed(path_file, array)
    
def find_previous_frame(current_timestamp, current_time, timestamp_list, files_list, name_list, dt_time, error_columns):
    """Get the previous file in the list"""
    previous_frame = None
    previous_stamp = None
    dt_torelerance = timedelta(minutes=name_list['delta_tolerance'])
    dt_skip = name_list['delta_skip']
    last_stamps = timestamp_list[current_time - (dt_skip + 1):current_time]
    last_files = files_list[current_time - (dt_skip + 1):current_time]
    for l_stamp in range(len(last_stamps)):
        tolrcn = dt_time + dt_torelerance
        difrcn = current_timestamp - last_stamps[l_stamp]
        if difrcn <= tolrcn and pathlib.Path(last_files[l_stamp]).exists():
            previous_frame = read_geodataframe(last_files[l_stamp], error_columns=error_columns)
            previous_stamp = last_stamps[l_stamp]
            dt_time = current_timestamp - last_stamps[l_stamp]
            break
        if len(last_files) > 1 and pathlib.Path(last_files[l_stamp + 1]).exists():
            previous_frame = read_geodataframe(last_files[l_stamp + 1], error_columns=error_columns)
            previous_stamp = last_stamps[l_stamp + 1]
            dt_time += dt_time
    return previous_frame, previous_stamp, dt_time

def calculate_direction(p0, p1):
    """ Calculate direction of vector. """
    radians_ = np.arctan2(p1[1] - p0[1],
                          p1[0] - p0[0])
    direction = np.degrees(radians_)
    if direction < 0:
        direction = direction + 360
    return direction

# Create a loading bar
def loading_bar(current, total, barLength = 50):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))
    sys.stdout.write('\rProgress: [%s%s] %d%%' % (arrow, spaces, percent))
    sys.stdout.flush()
    
def update_progress(progress, pbar):
    pbar.update(progress)

# def get_edge_limit(name_list, files_list, read_function):
#     """Get the edge limit of the data"""
#     if name_list['board'] == True:
#         for files in range(len(files_list)):
#             file_path = gpd.read_parquet(files_list[files])
#             if len(file_path) > 0:
#                 file_path = file_path['file'].unique()[0] # Get the file name
#                 break                
#         data_shape = read_function(file_path)
#         data_shape = data_shape.shape # Get the shape of the data
#         board_1 = gpd.GeoDataFrame({'geometry': [LineString([(data_shape[1], 0),(data_shape[1], data_shape[0])])]})
#         board_2 = gpd.GeoDataFrame({'geometry': [LineString([(0, 0),(0, data_shape[0])])]})
#         # if name_list['edge_limit'] == 'right':
#         # elif name_list['edge_limit'] == 'left':
#         #     board_1 = gpd.GeoDataFrame({'geometry': [LineString([(0, 0),(0, data_shape[0])])]})
#         #     board_2 = gpd.GeoDataFrame({'geometry': [LineString([(data_shape[1], 0),(data_shape[1], data_shape[0])])]})
#         # elif name_list['edge_limit'] == 'top':
#         #     board_1 = gpd.GeoDataFrame({'geometry': [LineString([(0, 0),(data_shape[0], 0)])]})
#         #     board_2 = gpd.GeoDataFrame({'geometry': [LineString([(0, data_shape[0]),(data_shape[0], data_shape[0])])]})
#         # elif name_list['edge_limit'] == 'bottom':
#         #     board_1 = gpd.GeoDataFrame({'geometry': [LineString([(0, data_shape[0]),(data_shape[0], data_shape[0])])]})
#         #     board_2 = gpd.GeoDataFrame({'geometry': [LineString([(0, 0),(data_shape[0], 0)])]})
#     else:
#         board_1, board_2, data_shape = None, None, None
#     return board_1, board_2, data_shape

def calc_statistic(feature, dbz_mean):
    """ Calculate the statistic of the feature. """  
    features = pd.DataFrame(feature).describe().T
    if dbz_mean:
        R = dbz2mmh(feature)
        # Calculate the mean rainfall rate
        rr_mean = np.mean(R)
        rr_q1 = np.quantile(R, 0.25)
        rr_q2 = np.quantile(R, 0.75)
        # Convert mm/h to dBZ
        dbz_mean = mmh2dbz(rr_mean)
        dbz_q1 = mmh2dbz(rr_q1)
        dbz_q2 = mmh2dbz(rr_q2)
        # Replace in features dataframe
        features['mean'] = dbz_mean
        features['25%'] = dbz_q1
        features['75%'] = dbz_q2
    return features

def dbz2mmh(dBZ, a=200.0, b=1.6):
    Z = 10.0 ** (dBZ / 10.0) # Convert reflectivity to mm^6/m^3
    R = (Z / a) ** (1.0 / b) # Apply Marshall-Palmer formula
    return R

def mmh2dbz(mmh, a=200.0, b=1.6):
    Z = a * mmh**b # Convert mm/h to mm^6/m^3
    dBZ = 10.0 * np.log10(Z) # Convert mm^6/m^3 to dBZ
    return dBZ
