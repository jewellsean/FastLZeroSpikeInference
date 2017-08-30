import numpy as np
import ctypes as ct 

lib = np.ctypeslib.load_library('FastLZeroSpikeInference', '/Users/jewellsean/Desktop/cloned_ar/FastLZeroSpikeInference/src')

def arfpop(dat, gam, penalty, constraint):
	dat = np.ascontiguousarray(dat, dtype = float)
	dat_count = dat.shape[0]
	cost_mat = np.ascontiguousarray(np.zeros(dat_count, dtype=float))
	end_vec = np.ascontiguousarray(np.zeros(dat_count, dtype=np.int32))
	mean_vec = np.ascontiguousarray(np.zeros(dat_count, dtype=float))
	intervals_mat = np.ascontiguousarray(np.zeros(dat_count, dtype=np.int32))
	constraint = constraint
	success = False

	lib.ARFPOP_interface(dat.ctypes.data_as(ct.POINTER(ct.c_double)), # data ptr
	                                ct.pointer(ct.c_int(dat_count)),  # data count
	                                ct.pointer(ct.c_double(penalty)), # penalty
	                                ct.pointer(ct.c_double(gam)),  # gamma
	                                cost_mat.ctypes.data_as(ct.POINTER(ct.c_double)), # cost mat
	                                end_vec.ctypes.data_as(ct.POINTER(ct.c_int)), # end_vec
	                                mean_vec.ctypes.data_as(ct.POINTER(ct.c_double)), # mean_vec
	                                intervals_mat.ctypes.data_as(ct.POINTER(ct.c_int)), # int_vec
	                                ct.pointer(ct.c_bool(constraint)), # constraint
	                                ct.pointer(ct.c_bool(success)))

	out = {}
	out['mean_vec'] = np.flip(mean_vec, 0)
	out['intervals_mat'] = intervals_mat
	out['changePts'] = np.unique(end_vec) + 1
	out['spikes'] = out['changePts'][1:] + 1
	out['spike_mag'] = out['mean_vec'][1:] - out['mean_vec'][0:-1] 

	padded = np.array([0])

	out['pos_spike_mag'] = np.concatenate((padded, 
		np.maximum(fit['spike_mag'], np.zeros(fit['spike_mag'].shape))))

	## TODO: add error catching here! 

	return out 