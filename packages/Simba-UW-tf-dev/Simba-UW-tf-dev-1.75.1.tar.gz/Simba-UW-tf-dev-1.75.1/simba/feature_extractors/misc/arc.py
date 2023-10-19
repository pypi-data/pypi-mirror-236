import time

from numba import prange, njit, types
from numba.typed import Dict
import numpy as np

@njit('(float32[:], float64, float64, float64, float64, float64, float64)')
def spike_finder(data: np.ndarray,
                 sample_rate: int,
                 baseline: float,
                 min_spike_amplitude: float,
                 min_fwhm: float = -np.inf,
                 min_half_width: float = -np.inf,
                 max_spike_train_separation: float = np.inf,
                 ) -> float:

    spike_idxs = np.argwhere(data >= baseline + min_spike_amplitude).flatten()
    spike_idx = np.split(spike_idxs, np.argwhere(spike_idxs[1:] - spike_idxs[:-1] != 1)[0] + 1)
    spike_dict = Dict.empty(key_type=types.int64, value_type=Dict.empty(key_type=types.unicode_type, value_type=types.float64))
    #spike_dict = {}

    for i in prange(len(spike_idx)):
        spike_data = data[spike_idx[i]]
        spike_amplitude = np.max(spike_data) - baseline
        half_width_idx = np.argwhere(spike_data > spike_amplitude / 2).flatten()
        spike_dict[i] = {'amplitude': np.max(spike_data) - baseline, 'fwhm': (half_width_idx[-1] - half_width_idx[0]) / sample_rate, 'half_width': half_width_idx.shape[0] / sample_rate}

    ## REMOVE SPIKES NOT MEETING CRITERIA
    remove_idx = []
    for k, v in spike_dict.items():
        if (v['fwhm'] < min_fwhm) or (v['half_width'] < min_half_width):
            remove_idx.append(k)
    for idx in remove_idx: spike_dict.pop(idx)
    spike_idx = [i for j, i in enumerate(spike_idx) if j not in remove_idx]

    ### FIND SPIKE TRAINS
    l, r, train_idx= 0, 1, []
    train_spike_idx = []
    while l < len(spike_idx):
        current_train, current_spike_idx = spike_idx[l], [l]
        while r < len(spike_idx) and ((spike_idx[r][0] - current_train[-1]) <= max_spike_train_separation):
            current_train = np.hstack((current_train, spike_idx[r]))
            current_spike_idx.append(r)
            r += 1
        l, r = r, r+1
        train_idx.append(current_train)
        train_spike_idx.append(current_spike_idx)

    train_dict = Dict.empty(key_type=types.int64, value_type=Dict.empty(key_type=types.unicode_type, value_type=types.float64))
    for i in prange(len(train_idx)):
        train_spikes = [k for j, k in enumerate(spike_idx) if j in train_spike_idx[i]]
        train_spike_lengths = np.array(([len(j) for j in train_spikes]))
        train_length_obs = len(train_idx[i])
        train_length_time = len(train_idx[i]) / sample_rate
        train_spike_cnt = len(train_spike_idx[i])
        train_spike_length_mean = np.mean(train_spike_lengths)
        train_spike_length_std = np.std(train_spike_lengths)
        train_spike_length_max = np.max(train_spike_lengths)
        train_spike_length_min = np.min(train_spike_lengths)

        train_spike_amplitude_mean = np.nan
        train_spike_amplitude_std = np.nan
        train_spike_amplitude_max = np.nan
        train_spike_amplitude_min = np.nan








        #train_dict[i] = {}

    # spike_trains = np.split(spike_trains, np.argwhere(spike_trains[1:] - spike_trains[:-1] > max_spike_train_separation)[0] + 1)
    # print(spike_trains)







data = np.array([4, 4, 4, 4, 10, 10, 8, 4, 4, 4, 10, 10, 8, 99]).astype(np.float32)
spike_finder(data=data,
             baseline=4,
             min_spike_amplitude=4,
             sample_rate=2,
             min_fwhm=-np.inf,
             min_half_width=-np.inf,
             max_spike_train_separation=4)
