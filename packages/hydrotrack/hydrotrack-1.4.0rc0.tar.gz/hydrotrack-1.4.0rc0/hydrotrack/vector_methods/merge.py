from scipy import stats
import pandas as pd
pd.set_option('mode.chained_assignment', None)

def merge_corretion(current_frame, previous_frames):
    """  This method get Merge events (MRG) into current frame and compute the mean of vectors (distance and direction) of individual clusters in the previous frame. """
    if len(previous_frames) < 2 or len(previous_frames[-1]) == 0:
        return pd.DataFrame(columns=['dis_mrg', 'dir_mrg'])
    if current_frame.empty:
        return pd.DataFrame(columns=['dis_mrg', 'dir_mrg'])
    past_frame = previous_frames[-1] # Get the last frame
    # Select only MRG status in current frame
    current_frame = current_frame[current_frame['status'] == 'MRG']
    # Add columns dis_mrg and dir_mrg in current frame
    current_frame['dis_mrg'] = None
    current_frame['dir_mrg'] = None
    if current_frame.empty:
        return pd.DataFrame(columns=['dis_mrg', 'dir_mrg'])
    for idx, row in current_frame.iterrows():
        if row['merge_idx'] is None:
            continue
        # Check if past_frame contains merge_idx
        prev_idx = past_frame.index.isin(row['merge_idx'])
        if not prev_idx.any():
            continue
        prev_values = past_frame[past_frame.index.isin(prev_idx)]
        # Check if prev_values contains dis_ values
        distance_values = prev_values['dis_'].dropna()
        direction_values = prev_values['dir_'].dropna()
        if distance_values.empty or direction_values.empty:
            continue
        mean_dis = distance_values.mean()
        mean_dir = stats.circmean(direction_values, high=360, low=0, nan_policy='omit')
        # Update current frame with mean values at column dis_mrg and dir_mrg
        current_frame.loc[idx, 'dis_mrg'] = mean_dis
        current_frame.loc[idx, 'dir_mrg'] = mean_dir
    return current_frame[['dis_mrg', 'dir_mrg']]
