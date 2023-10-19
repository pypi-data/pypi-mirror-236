import pandas as pd
from scipy import stats

def innerc_corretion(current_frame):
    """"  This method get inner cores (INC) into current frame and compute the mean of vectors (distance and direction) of individual clusters in the previous frame. """
    # if current_frame[current_frame['threshold_level'] > 0].empty:
    #     return pd.DataFrame(columns=['dis_inc', 'dir_inc'])
    if len(current_frame) < 1:
        return pd.DataFrame(columns=['dis_inc', 'dir_inc'])
    # Add columns dis_inc and dir_inc in current frame
    current_frame['dis_inc'] = None
    current_frame['dir_inc'] = None
    current_copy = current_frame.copy()
    # Select not nan uids
    current_copy = current_copy[~current_copy['uid'].isnull()]
    # Current frame transform all values into int in uid column
    current_copy['uid'] = current_copy['uid'].astype(int)
    # Groupby uid and threshold_level in current frame
    current_frame_group = current_copy.groupby(['uid'])
    for _, cur_group in current_frame_group:
        cur_group = cur_group[['dis_','dir_']].dropna()
        if len(cur_group) < 1:
            continue
        # Update current frame with mean values at column dis_mrg and dir_mrg
        current_frame.loc[cur_group.index[0], 'dis_inc'] = cur_group['dis_'].mean()
        current_frame.loc[cur_group.index[0], 'dir_inc'] = stats.circmean(cur_group['dir_'], high=360, low=0, nan_policy='omit')
    return current_frame[['dis_inc', 'dir_inc']]
