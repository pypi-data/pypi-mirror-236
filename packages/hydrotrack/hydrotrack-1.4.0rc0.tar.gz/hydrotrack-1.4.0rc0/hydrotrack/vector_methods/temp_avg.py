import pandas as pd
from scipy import stats
# pd.set_option('mode.chained_assignment', None)

def temporal_avg_corretion(current_frame, previous_frames):
    """"  This method get latest previous frames and compute the mean vector into current frame. """
    if len(previous_frames) < 1 or len(previous_frames[-1]) == 0:
        return pd.DataFrame(columns=['dis_avg', 'dir_avg'])
    if len(current_frame) < 1:
        return pd.DataFrame(columns=['dis_avg', 'dir_avg'])
    # Concatenate previous frames into one dataframe if not empty in previous_frames list
    past_frames = pd.concat(previous_frames)
    # Add columns dis_tavg and dir_tavg in current frame
    current_frame['dis_avg'] = None
    current_frame['dir_avg'] = None
    current_frame_group = current_frame.groupby(['uid', 'threshold_level','status'])
    for gidx, cur_group in current_frame_group:
        previous_values = past_frames[(past_frames['uid'] == gidx[0]) & 
                                      (past_frames['threshold_level'] == gidx[1])][['dis_','dir_']].dropna()
        if cur_group['status'].iloc[0] == 'NEW' or len(previous_values) <= 1:
            continue
        # Compute mean vector
        distance_mean = previous_values['dis_'].mean()
        direction_mean = stats.circmean(previous_values['dir_'], high=360, low=0, nan_policy='omit')
        # Update current frame with mean values at column dis_mrg and dir_mrg
        current_frame.loc[cur_group.index, 'dis_avg'] = distance_mean
        current_frame.loc[cur_group.index, 'dir_avg'] = direction_mean
    return current_frame[['dis_avg', 'dir_avg']]