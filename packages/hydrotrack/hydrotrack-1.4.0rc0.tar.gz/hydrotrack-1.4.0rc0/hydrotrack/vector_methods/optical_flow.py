import pandas as pd
import numpy as np
import cv2
import geopandas as gpd
from shapely.geometry import Point, LineString, MultiLineString, MultiPoint
from shapely.ops import linemerge
from scipy import stats
from .image_filters import *
from ..utils import calculate_direction, set_operator

# import time

# import matplotlib.pyplot as plt


def optflow_corretion(current_df, previous_df, read_function, name_list, method='lucas-kanade',opt_times=2):
    """Optical Flow corretion method used to compute the optical flow for a sparse feature set using the iterative
    Using reverse image order (t-1,t-2,t-3,...)
    """
    # Initialize output frame    
    output_frame = pd.DataFrame(columns=['index','dis_opt', 'dir_opt','vector_field'])
    if len(current_df) == 0: # Check if current_frame is empty
        return output_frame
    if len(previous_df[-1]) == 0: # Check if previous_frames is empty
        return output_frame
    if opt_times > len(previous_df): # Check if opt_times is greater than previous_frames
        opt_times = len(previous_df)
    prev_dfs = pd.concat(previous_df[-opt_times:]) # Concatenate previous frames
    # Set read_function parameters to use in map function
    min_val = current_df['threshold'].min()
    max_val = current_df['threshold'].max()
    operator = set_operator(name_list)
    # Set optical flow method
    if method == 'lucas-kanade':
        optical_flow = lucas_kanade
    elif method == 'farneback':
        optical_flow = farneback
    # Initialize empty array for current points
    currPts = np.empty((0,1,2), dtype=int)
    # Mount img_frames list
    img_frames = list(prev_dfs.file.unique()) # Get previous paths
    img_frames.append(current_df.file.unique()[0]) # Add current path
    img_frames = sorted(img_frames)[::-1] # Reverse the list to use reverse image order (t-1,t-2,t-3,...)
    # Read images, segment the image based on the threshold and normalize the image
    img_frames = list(map(lambda x: read_norm(x, read_function, operator, min_val, max_val), img_frames))
    vector_field = []
    # start_time = time.time()
    for tm in range(len(img_frames) - 1): # Iterate over the images
        cur_img = img_frames[tm] # Current image
        prv_img = img_frames[tm + 1] # Previous image
        # Call Optical Flow Methods
        prevPts, currPts = optical_flow(cur_img, prv_img, currPts)
        vector_field.extend(list(map(lambda x: LineString([Point(x[0]), Point(x[1])]), zip(prevPts,currPts))))
        currPts = prevPts # Set current points
    # print('\nNumber of vectors:', len(vector_field))
    # print('-- %s seconds --' % (time.time() - start_time))
    # Merge lines comming from Optical Flow
    vector_field = linemerge(vector_field)
    # check if merged_lines is empty
    if vector_field.is_empty:
        return output_frame
    elif isinstance(vector_field, LineString):
        vector_field = gpd.GeoDataFrame(geometry=[vector_field])
    elif isinstance(vector_field, MultiLineString):
        vector_field = gpd.GeoDataFrame(geometry=list(vector_field.geoms))
    else:
        return output_frame
    # Set p0 column (p0 is the first point of the line, used to verify if is inside the threshold_levels geometry)
    vector_field['p0'] = vector_field.geometry.apply(lambda x: Point(x.coords[-1]))
    vector_field = vector_field.set_geometry('p0')
    # Group by inside threshold_levels
    thd_curframe = current_df.groupby('threshold_level')
    for _, idx in reversed(thd_curframe.groups.items()):
        operation = gpd.sjoin(vector_field, current_df.loc[idx][['threshold_level','geometry']], how='inner', predicate='within')
        vector_field = vector_field.loc[~vector_field.index.isin(operation.index)] # Remove inside vectors from vector_field
        vector_field = vector_field.set_geometry('p0') # Reset geometry of vector_field
        # Group by index_right at operation from inside threshold_levels to outside
        for idx2, ggroup in operation.groupby('index_right'):
            qtd_coords = ggroup['geometry'].apply(lambda x: len(x.coords))
            lenght_coords = ggroup['geometry'].length
            mean_leangth = np.mean(lenght_coords / qtd_coords)
            direct_coords = ggroup['geometry'].apply(lambda x: calculate_direction(x.coords[0], x.coords[1]))
            mean_direction = stats.circmean(direct_coords.to_numpy(), high=360, axis=0,nan_policy='omit')
            v_field = str(ggroup['geometry'].unary_union)
            output_frame = pd.concat([output_frame, pd.DataFrame([[idx2, mean_leangth, mean_direction,v_field]],
                                                                 columns=['index','dis_opt', 'dir_opt','vector_field'])])
    output_frame = output_frame.set_index('index') # Set index
    return output_frame

def read_norm(path,read_function, operator, min_val, max_val):
    """ Read image, segment and normalize image """
    img = read_function(path) # Read image
    img = np.where(operator(img, min_val), img, np.nan) # Segment the image based on the threshold
    img = norm_img(img, min_value=min_val, max_value=max_val) # Normalize image
    return img

def norm_img(matrix, min_value=None, max_value=None):
    """ Normalize image between 0 and 255 """
    matrix = np.nan_to_num(matrix, nan=0.0) # Replace nan values to 0
    matrix = cv2.normalize(matrix, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U) # Normalize matrix
    # matrix = apply_gaussian_blur(matrix, kernel_size=(5, 5), sigma=1.0) # Apply Gaussian blur
    # matrix = add_gaussian_noise(matrix, mean=0, stddev=25) # Add gaussian noise
    matrix = histogram_equalization(matrix) # Apply histogram equalization
    #matrix = detect_edges_canny(matrix, low_threshold=min_value, high_threshold=max_value) # Apply canny edge detection
    return matrix

def lucas_kanade(current_img, previous_img, currPts):
    """Lucas Kanade optical flow method used to compute the optical flow for a sparse feature set using the iterative
    Using reverse image order (t-1,t-2,t-3,...)
    """
    # Check if currPts is empty (first iteration) and call ShiTomasi corner detection
    if len(currPts) == 0:
        # Params for ShiTomasi corner detection
        feature_params = dict(
            maxCorners=None,
            qualityLevel=0.01,  # Parameter characterizing the minimal accepted quality of image corners.
            minDistance=0.5,  # Minimum possible Euclidean distance between the returned corners.
            blockSize=2,  # Size of an average block for computing a derivative covariation matrix over each pixel neighborhood.
            useHarrisDetector=False,  # Parameter indicating whether to use a Harris detector (see cornerHarris) or cornerMinEigenVal.
            k=0.04,  # Free parameter of the Harris detector.
        )
        # ShiTomasi corner detection
        currPts = cv2.goodFeaturesToTrack(current_img, mask=None, **feature_params)
    # Call Lucas Kanade optical flow
    win_percent = 20 # Percent of image size to use as window size
    nextPts, status, _ = cv2.calcOpticalFlowPyrLK(prevImg=current_img,
                                                  nextImg=previous_img,
                                                  prevPts=currPts,
                                                  nextPts=None,
                                                  winSize=(current_img.shape[1] // win_percent,
                                                           current_img.shape[0] // win_percent),
                                                  maxLevel=3,
                                                  criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01),
                                                  flags=cv2.OPTFLOW_LK_GET_MIN_EIGENVALS,
                                                  minEigThreshold=1e-4)
    # Select good points
    nextPts = nextPts[status == 1]
    currPts = currPts[status == 1]
    nextPts = nextPts[:, np.newaxis, :] # Add new axis
    currPts = currPts[:, np.newaxis, :] # Add new axis
    return nextPts, currPts

def farneback(current_img, previous_img, _):
    """Farneback optical flow method used to compute the optical flow for a sparse feature set using the iterative
    Using reverse image order (t-1,t-2,t-3,...)
    """
    flow = cv2.calcOpticalFlowFarneback(prev=current_img,
                                        next=previous_img,
                                        flow=None,
                                        pyr_scale=0.5, # Parâmetro de escala piramidal.
                                        levels=3, # Número de níveis piramidais.
                                        winsize=50, # Tamanho da janela de busca.
                                        iterations=3, # Número de iterações do algoritmo a cada nível piramidal.
                                        poly_n=10, # Tamanho da vizinhança considerada ao calcular o polinômio de expansão.
                                        poly_sigma=1.1, # Desvio padrão do filtro gaussiano aplicado ao polinômio de expansão.
                                        flags=0)
    magn, angle = cv2.cartToPolar(flow[...,0], flow[...,1]) 
    y_idx, x_idx = np.where(magn > 1)  # Get position of points with magnitude > 1
    pixel_sparsity = 10 # Sparsity of pixels
    y_idx = y_idx[::pixel_sparsity]
    x_idx = x_idx[::pixel_sparsity]
    magn = magn[y_idx, x_idx] # Get magnitude of points with magnitude > 1
    angle = np.rad2deg(angle[y_idx, x_idx]) # Get angle of points with magnitude > 1
    points = [point_position(x_idx[p],y_idx[p], magn[p], angle[p]) for p in range(len(y_idx))]
    nextPts = np.array(points).reshape(-1, 1, 2)
    currPts = np.array([x_idx, y_idx]).T.reshape(-1, 1, 2)
    if np.any(np.isinf(nextPts)): # Verify if have inf values in nextPts
        inf_idx = np.where(np.isinf(nextPts))
        nextPts = np.delete(nextPts, inf_idx[0], axis=0)
        currPts = np.delete(currPts, inf_idx[0], axis=0)
    return nextPts, currPts

def point_position(x1=None, y1=None, lenght=None, angle=None):
    """
    Calculates the position of a point for displacement.
    """
    rad_theta = np.radians(angle)
    x2 = x1 + lenght * np.cos(rad_theta)
    y2 = y1 + lenght * np.sin(rad_theta)
    return x2, y2


