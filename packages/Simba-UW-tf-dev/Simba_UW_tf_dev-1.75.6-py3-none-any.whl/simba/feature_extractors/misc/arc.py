import time

from numba import prange, njit, types, typed, jit
from numba.typed import Dict
import numpy as np
import pickle

@njit('(float32[:], float64, float64, float64, float64, float64)', fastmath=True)
def spike_finder(data: np.ndarray,
                 sample_rate: int,
                 baseline: float,
                 min_spike_amplitude: float,
                 min_fwhm: float = -np.inf,
                 min_half_width: float = -np.inf) -> float:

    """
    Identify and characterize spikes in a given time-series data sequence.

    This function identifies spikes in the input data based on the specified criteria and characterizes
    each detected spike by computing its amplitude, full-width at half maximum (FWHM), and half-width.

    :param np.ndarray data: A 1D array containing the input data sequence to analyze.
    :param int sample_rate: The sample rate, indicating how many data points are collected per second.
    :param float baseline: The baseline value used to identify spikes. Any data point above (baseline + min_spike_amplitude) is considered part of a spike.
    :param float min_spike_amplitude: The minimum amplitude (above baseline) required for a spike to be considered.
    :param Optional[float] min_fwhm: The minimum full-width at half maximum (FWHM) for a spike to be included. If not specified, it defaults to negative infinity, meaning it is not considered for filtering.
    :param Optional[float] min_half_width: The minimum half-width required for a spike to be included. If not specified, it defaults to negative infinity, meaning it is not considered for filtering.
    :return tuple: A tuple containing three elements:
        - spike_idx (List[np.ndarray]): A list of 1D arrays, each representing the indices of the data points belonging to a detected spike.
        - spike_vals (List[np.ndarray]): A list of 1D arrays, each containing the values of the data points within a detected spike.
        - spike_dict (Dict[int, Dict[str, float]]): A dictionary where the keys are spike indices, and the values are dictionaries containing spike characteristics including 'amplitude' (spike amplitude), 'fwhm' (FWHM), and 'half_width' (half-width).

    .. notes::
       - The function uses the Numba JIT (Just-In-Time) compilation for optimized performance. Without fastmath=True there is no runtime improvement over standard numpy.

    :example:
    >>> data = np.array([0.1, 0.1, 0.3, 0.1, 10, 10, 8, 0.1, 0.1, 0.1, 10, 10, 8, 99, 0.1, 99, 99, 0.1]).astype(np.float32)
    >>> spike_idx, spike_vals, spike_stats = spike_finder(data=data, baseline=1, min_spike_amplitude=5, sample_rate=2, min_fwhm=-np.inf, min_half_width=0.0002)
    """

    spike_idxs = np.argwhere(data >= baseline + min_spike_amplitude).flatten()
    spike_idx = np.split(spike_idxs, np.argwhere(spike_idxs[1:] - spike_idxs[:-1] != 1).flatten() + 1)
    spike_dict = Dict.empty(key_type=types.int64, value_type=Dict.empty(key_type=types.unicode_type, value_type=types.float64))
    spike_vals = []
    for i in prange(len(spike_idx)):
        spike_data = data[spike_idx[i]]
        spike_amplitude = np.max(spike_data) - baseline
        half_width_idx = np.argwhere(spike_data > spike_amplitude / 2).flatten()
        spike_dict[i] = {'amplitude': np.max(spike_data) - baseline, 'fwhm': (half_width_idx[-1] - half_width_idx[0]) / sample_rate, 'half_width': half_width_idx.shape[0] / sample_rate}
        spike_vals.append(spike_data)

    remove_idx = []
    for k, v in spike_dict.items():
        if (v['fwhm'] < min_fwhm) or (v['half_width'] < min_half_width):
            remove_idx.append(k)
    for idx in remove_idx: spike_dict.pop(idx)
    spike_idx = [i for j, i in enumerate(spike_idx) if j not in remove_idx]
    spike_vals = [i for j, i in enumerate(spike_vals) if j not in remove_idx]

    return spike_idx, spike_vals, spike_dict

#@njit("(float32[:], types.List(types.Array(types.int64, 1, 'C')), int64, float64, float64)", fastmath=True)
@jit(nopython=True, fastmath=True)
def spike_train_finder(data: np.ndarray,
                       spike_idx: list,
                       sample_rate: float,
                       min_spike_train_length: float = np.inf,
                       max_spike_train_separation: float = np.inf):
    """
    Identify and analyze spike trains from a list of spike indices.

    This function takes spike indices and additional information, such as the data, sample rate,
    minimum spike train length, and maximum spike train separation, to identify and analyze
    spike trains in the data.

    :param np.ndarray data: The data from which spike trains are extracted.
    :param types.List(types.Array(types.int64, 1, 'C')) data: A list of spike indices, typically as integer timestamps.
    :param float sample_rate: The sample rate of the data.
    :param Optional[float] min_spike_train_length: The minimum length a spike train must have to be considered. Default is set to positive infinity, meaning no minimum length is enforced.
    :param Optional[float] max_spike_train_separation: The maximum allowable separation between spikes in the same train. Default is set to positive infinity, meaning no maximum separation is enforced.
    :return DictType[int64,DictType[unicode_type,float64]]: A dictionary containing information about identified spike trains.
    Each entry in the dictionary is indexed by an integer and contains the following information:
        - 'train_start_time': Start time of the spike train in seconds.
        - 'train_end_time': End time of the spike train in seconds.
        - 'train_start_obs': Start time index in observations.
        - 'train_end_obs': End time index in observations.
        - 'spike_cnt': Number of spikes in the spike train.
        - 'train_length_obs_cnt': Length of the spike train in observations.
        - 'train_length_obs_s': Length of the spike train in seconds.
        - 'train_spike_mean_lengths_s': Mean length of individual spikes in seconds.
        - 'train_spike_std_length_obs': Standard deviation of spike lengths in observations.
        - 'train_spike_std_length_s': Standard deviation of spike lengths in seconds.
        - 'train_spike_max_length_obs': Maximum spike length in observations.
        - 'train_spike_max_length_s': Maximum spike length in seconds.
        - 'train_spike_min_length_obs': Minimum spike length in observations.
        - 'train_spike_min_length_s': Minimum spike length in seconds.
        - 'train_mean_amplitude': Mean amplitude of the spike train.
        - 'train_std_amplitude': Standard deviation of spike amplitudes.
        - 'train_min_amplitude': Minimum spike amplitude.
        - 'train_max_amplitude': Maximum spike amplitude.


    .. note::
       - The function may return an empty dictionary if no spike trains meet the criteria.
       - ``spike_idx`` is returned by ``spike_finder``.


    :example:
    >>> data = np.array([0.1, 0.1, 0.3, 0.1, 10, 10, 8, 0.1, 0.1, 0.1, 10, 10, 8, 99, 0.1, 99, 99, 0.1]).astype(np.float32)
    >>> spike_idx, _, _ = spike_finder(data=data, baseline=0.3, min_spike_amplitude=0.2, sample_rate=2, min_fwhm=-np.inf, min_half_width=-np.inf)
    >>> spike_train_finder(data=data, spike_idx=typed.List(spike_idx), sample_rate=2.0, min_spike_train_length=2.0, max_spike_train_separation=2.0)
    """

    l, r, = 0, 1
    train_data_idx = []
    train_spikes_idx = []
    max_spike_train_separation = int(max_spike_train_separation * sample_rate)
    min_spike_train_length = int(min_spike_train_length * sample_rate)
    while l < len(spike_idx):
        current_train, current_spike_idx = spike_idx[l], [l]
        while r < len(spike_idx) and ((spike_idx[r][0] - current_train[-1]) <= max_spike_train_separation):
            current_train = np.hstack((current_train, spike_idx[r]))
            current_spike_idx.append(r)
            r += 1
        l, r = r, r+1
        train_data_idx.append(current_train)
        train_spikes_idx.append(current_spike_idx)

    spike_dict = Dict.empty(key_type=types.int64, value_type=Dict.empty(key_type=types.unicode_type, value_type=types.float64))
    for i in prange(len(train_data_idx)):
        if train_data_idx[i].shape[0] >= min_spike_train_length:
            spike_train_amps = data[train_data_idx[i]]
            spike_train_idx = [k for j, k in enumerate(spike_idx) if j in train_spikes_idx[i]]
            train_spike_lengths = np.array(([len(j) for j in spike_train_idx]))
            spike_dict[int(i)] = {'train_start_time': float(train_data_idx[i][0] * sample_rate),
                                  'train_end_time': train_data_idx[i][-1] * sample_rate,
                                  'train_start_obs': train_data_idx[i][0],
                                  'train_end_obs': train_data_idx[i][-1],
                                  'spike_cnt': len(train_spikes_idx[i]),
                                  'train_length_obs_cnt': len(spike_train_amps),
                                  'train_length_obs_s': len(spike_train_amps) / sample_rate,
                                  'train_spike_mean_lengths_s': np.mean(train_spike_lengths) * sample_rate,
                                  'train_spike_std_length_obs': np.mean(train_spike_lengths),
                                  'train_spike_std_length_s': np.mean(train_spike_lengths) * sample_rate,
                                  'train_spike_max_length_obs': np.max(train_spike_lengths),
                                  'train_spike_max_length_s': np.max(train_spike_lengths) * sample_rate,
                                  'train_spike_min_length_obs': np.min(train_spike_lengths),
                                  'train_spike_min_length_s': np.min(train_spike_lengths) * sample_rate,
                                  'train_mean_amplitude': np.mean(spike_train_amps),
                                  'train_std_amplitude': np.std(spike_train_amps),
                                  'train_min_amplitude': np.min(spike_train_amps),
                                  'train_max_amplitude': np.max(spike_train_amps)}

    return spike_dict

data = np.array([0.1, 0.1, 0.3, 0.1, 10, 10, 8, 0.1, 0.1, 0.1, 10, 10, 8, 99, 0.1, 99, 99, 0.1]).astype(np.float32)
spike_idx, _, _ = spike_finder(data=data, baseline=0.3, min_spike_amplitude=0.2, sample_rate=2, min_fwhm=-np.inf, min_half_width=-np.inf)
start = time.time()
for i in range(1000):
    results = spike_train_finder(data=data, spike_idx=typed.List(spike_idx), sample_rate=2.0, min_spike_train_length=2.0, max_spike_train_separation=2.0)
print(time.time() - start)




#
#
# start = time.time()
# for i in range(10):
#     #data = np.array([0.1, 0.1, 0.3, 0.1, 10, 10, 8, 0.1, 0.1, 0.1, 10, 10, 8, 99, 0.1, 99, 99, 0.1]).astype(np.float32)
#     spike_idx, spike_vals, spike_stats = spike_finder(data=data,
#                                                       baseline=0.3,
#                                                       min_spike_amplitude=0.2,
#                                                       sample_rate=20000,
#                                                       min_fwhm=-np.inf,
#                                                       min_half_width=0.0002)
# print(time.time() - start)




#with open('/Users/simon/Desktop/envs/eeg/sample_data/converted/split/A-011.pickle', 'rb') as handle:
#data = pickle.load(handle)['data'] / 1000

#baseline = 0.15

#

#
#
#
#
#
# ### FIND SPIKE TRAINS

#
# train_dict = Dict.empty(key_type=types.int64, value_type=Dict.empty(key_type=types.unicode_type, value_type=types.float64))
# for i in prange(len(train_idx)):
#     train_spikes = [k for j, k in enumerate(spike_idx) if j in train_spike_idx[i]]
#     train_spike_lengths = np.array(([len(j) for j in train_spikes]))
#     train_length_obs = len(train_idx[i])
#     train_length_time = len(train_idx[i]) / sample_rate
#     train_spike_cnt = len(train_spike_idx[i])
#     train_spike_length_mean = np.mean(train_spike_lengths)
#     train_spike_length_std = np.std(train_spike_lengths)
#     train_spike_length_max = np.max(train_spike_lengths)
#     train_spike_length_min = np.min(train_spike_lengths)
#
#     train_spike_amplitude_mean = np.nan
#     train_spike_amplitude_std = np.nan
#     train_spike_amplitude_max = np.nan
#     train_spike_amplitude_min = np.nan
#
#
#
#
#
#
#
#
#     #train_dict[i] = {}
#
# # spike_trains = np.split(spike_trains, np.argwhere(spike_trains[1:] - spike_trains[:-1] > max_spike_train_separation)[0] + 1)
# # print(spike_trains)
#




