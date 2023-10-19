import numpy as np
import pandas as pd
import geopandas as gpd
import pathlib
import multiprocessing as mp
from shapely.geometry import Polygon
from rasterio import features
from .utils import update_progress, get_filestamp, set_operator, set_dbscan, get_input_files
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

def extract_features(name_list, read_func, save_feat=True, parallel=True):
    '''Return a list of features from a list of names'''
    # Get the input files
    files_list = get_input_files(name_list)
    if len(files_list) < 1:
        print('There are not enough files to process')
        return
    # Set the operator to be used
    operator = set_operator(name_list)
    # Set the DBSCAN parameters
    dbscan = set_dbscan()
    # Number of cores
    if 'n_jobs' not in name_list.keys():
        name_list['n_jobs'] = mp.cpu_count()
    elif name_list['n_jobs'] == -1:
        name_list['n_jobs'] = mp.cpu_count()
    print('Extract features process has been started...')
    # Create the output features directories
    pathlib.Path(name_list['output_path'] + 'features/').mkdir(parents=True, exist_ok=True)
    # Create the progress bar
    pbar = tqdm(total=len(files_list), ncols=80, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [Elapsed:{elapsed} Remaining:<{remaining}]')
    if parallel: # Run parallel
        with mp.Pool(name_list['n_jobs']) as pool:
            for _ in pool.imap_unordered(get_features, [(file, name_list, operator, read_func, dbscan, save_feat) for _, file in enumerate(files_list)]):
                update_progress(1, pbar)
        pool.close()
    else: # Run serial
        for _, file in enumerate(files_list):
            get_features((file, name_list, operator, read_func, dbscan, save_feat))
            update_progress(1, pbar)
    pbar.close()


def get_features(args):
    '''Calculate the features for a single file'''

    file, name_list, operator, read_func, dbscan, save_feat = args
    # Initialize the features
    main_features = pd.DataFrame(columns=['timestamp', 'cluster_id', 'threshold', 'threshold_level', 'size',
       'mean', 'std', 'min', 'Q1', 'Q2', 'Q3', 'max', 'file', 'geometry',
       'array_values', 'array_x', 'array_y']) # Empty dataframe to store the features
    timestamp = get_filestamp(name_list, file)
    feature_file = name_list['output_path'] + 'features/{}.parquet'.format(timestamp.strftime('%Y%m%d_%H%M'))
    # Read the data from the file using the read_func
    try:
        data = read_func(file)
    except Exception as e:
        print('Error reading file: {}'.format(file), e)
        if save_feat:
            # main_features to geodataframe
            main_features = gpd.GeoDataFrame(main_features, geometry='geometry')
            main_features.to_parquet(feature_file)
        return
    mean_dbz = False # Default value
    if 'mean_dbz' in name_list.keys() and name_list['mean_dbz']:
        mean_dbz = True
    ###### Start processing the data ######
    # Loop over the thresholds
    for thld_lvl, threshold in enumerate(name_list['thresholds']):
        # Step 1: Segment the data based on the threshold
        coordinates = np.argwhere(operator(data, threshold))
        # Step 2: Clustering the data
        clusters = clustering(dbscan,
                              coordinates,
                              name_list['min_cluster_size'][thld_lvl])
        # Step 3: Calculate the statistics for each cluster
        cluster_statistics = statistics(clusters, data, dbz=mean_dbz)
        cluster_statistics['threshold'] = threshold
        cluster_statistics['threshold_level'] = thld_lvl
        main_features = pd.concat([main_features, cluster_statistics], axis=0)
    main_features['file'] = file
    main_features['timestamp'] = timestamp
    main_features.reset_index(inplace=True, drop=True)
    if save_feat:
        main_features = gpd.GeoDataFrame(main_features, geometry='geometry')
        main_features.to_parquet(feature_file)
    return

def clustering(dbscan, points, min_cluster_size):
    '''Return the cluster labels for each point'''
    # Fit the dbscan model
    dbscan.fit(points)
    clusters = np.concatenate((points, dbscan.labels_[:, np.newaxis]), axis=1)
    # Remove noise
    clusters = clusters[clusters[:, -1] != -1]
    # Filter by count of points labels
    items, count = np.unique(clusters[:, -1], return_counts=True)
    filter_ids = items[count < min_cluster_size]
    # Remove points with less than min_cluster_size points
    clusters = clusters[~np.isin(clusters[:, -1], filter_ids)]
    # Increment label to start from 1
    clusters[:, -1] += 1
    return clusters

def statistics(clusters, data, dbz=True):
    y_ = clusters[:, 0] # Get the y coordinates of the clusters
    x_ = clusters[:, 1] # Get the x coordinates of the clusters
    labels = clusters[:, -1] # Get the labels of the clusters
    raster = np.zeros(data.shape, dtype=np.int16) # Create an empty raster
    raster[y_, x_] = labels # Fill the raster with the labels
    mask_array = raster != 0 # Create a mask array
    # Calculate the statistics for each cluster
    clusters_stats = pd.DataFrame()
    for geo in features.shapes(raster, mask_array, connectivity=8, transform=(1,0,0,0,1,0)):
        boundary = Polygon(geo[0]['coordinates'][0])
        cluster_id = int(geo[-1])
        cluster_indices = np.argwhere(labels == cluster_id).ravel()
        array_y = y_[cluster_indices]
        array_x = x_[cluster_indices]
        cluster_values = data[array_y, array_x]
        if dbz:
            mm6m3_values = 10.0 ** (cluster_values / 10.0) # Convert to mm^6 m^-3
            mean_value = 10*np.log10(np.nanmean(mm6m3_values))
            std_value = 10*np.log10(np.nanstd(mm6m3_values))
        else:
            mean_value = np.nanmean(cluster_values)
            std_value = np.nanstd(cluster_values)
        # Calculate the statistics
        cluster_stat = pd.DataFrame({'cluster_id': cluster_id,
                                     'size': len(cluster_values),
                                     'min': np.nanmin(cluster_values),
                                     'mean': mean_value,
                                     'max': np.nanmax(cluster_values),
                                     'std': std_value,
                                     'Q1': np.quantile(cluster_values, 0.25),
                                     'Q2': np.quantile(cluster_values, 0.50),
                                     'Q3': np.quantile(cluster_values, 0.75),
                                     'array_values': [cluster_values],
                                     'array_x': [array_x],
                                     'array_y': [array_y],
                                     'geometry':boundary})
        # Concate cluster_id, array_values, array_x, array_y to stats
        clusters_stats = pd.concat([clusters_stats,cluster_stat], axis=0)
    return clusters_stats
