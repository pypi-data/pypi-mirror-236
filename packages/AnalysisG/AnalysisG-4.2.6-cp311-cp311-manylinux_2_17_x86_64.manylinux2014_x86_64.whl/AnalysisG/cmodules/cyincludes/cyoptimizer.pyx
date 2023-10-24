# distutils: language = c++
# cython: language_level = 3

from libcpp.string cimport string, stoi
from libcpp.vector cimport vector
from libcpp.algorithm cimport count
from libcpp.map cimport map, pair
from libcpp cimport tuple
from libcpp cimport bool

from cython.operator cimport dereference
from cython.parallel cimport prange

from cytools cimport env, enc, penc, pdec, map_to_dict, recast
from cyoptimizer cimport CyOptimizer, CyEpoch, CheckDifference
from cytypes cimport folds_t, data_t, metric_t, graph_t

from AnalysisG._cmodules.cPlots import MetricPlots
import numpy as np

from torch_geometric.data import Batch
import multiprocessing
from tqdm import trange
import psutil
import torch
import h5py
import pickle

cdef vector[folds_t] kfold_build(string* hash_, vector[tuple[string, bool]]* kf) noexcept nogil:
    cdef vector[folds_t] folds
    cdef folds_t fold = folds_t()
    fold.event_hash = dereference(hash_)
    fold.train = False
    fold.test = False
    fold.evaluation = False

    cdef tuple[string, bool] i
    for i in dereference(kf):
        if not i[0].rfind(b"k-", 0): folds.push_back(fold)
        elif not i[0].rfind(b"train", 0): fold.train = True
        elif not i[0].rfind(b"test", 0):  fold.test = True

    if not fold.train:
        folds.push_back(fold)
        return folds

    cdef int idx = 0
    cdef string mode
    for i in dereference(kf):
        mode = i[0]
        if mode.rfind(b"k-", 0): continue
        folds[idx].kfold = stoi(mode.substr(2, mode.size()))
        if i[1]: folds[idx].train = True
        else: folds[idx].evaluation = True
        idx += 1
    return folds



cdef void _check_h5(f, str key, data_t* inpt):
    f.create_dataset(key + "-truth"       , data = np.array(inpt.truth),     chunks = True)
    f.create_dataset(key + "-pred"        , data = np.array(inpt.pred) ,     chunks = True)
    f.create_dataset(key + "-index"       , data = np.array(inpt.index),     chunks = True)
    f.create_dataset(key + "-nodes"       , data = np.array(inpt.nodes),     chunks = True)
    f.create_dataset(key + "-loss"        , data = np.array(inpt.loss) ,     chunks = True)
    f.create_dataset(key + "-accuracy"    , data = np.array(inpt.accuracy),  chunks = True)

    cdef pair[int, vector[vector[float]]] itr
    for itr in inpt.mass_pred:
        f.create_dataset(key + "-masses-pred ->" + str(itr.first), data = np.array(itr.second),  chunks = True)

    for itr in inpt.mass_truth:
        f.create_dataset(key + "-masses-truth ->" + str(itr.first), data = np.array(itr.second),  chunks = True)

cdef void _rebuild_h5(f, list var, CyOptimizer* ptr, string mode, int epoch, int kfold):
    cdef map[string, data_t] mp_data
    cdef data_t* data

    try: file = f[env(mode)]
    except KeyError: return

    cdef str i, key
    cdef int idx = 0
    cdef int idy = 0
    cdef int chnks = 1000000
    cdef int end = file[var[0] + "-truth"].shape[0]
    for _ in trange(0, int(end/chnks)+1):
        idy = (end - idy)%chnks + idy
        for key in var:
            mp_data[enc(key)] = data_t()
            data = &mp_data[enc(key)]
            data.truth = <vector[vector[float]]>file[key + "-truth"][idx : idy].tolist()
            data.pred = <vector[vector[float]]>file[key + "-pred"][idx : idy].tolist()
            data.index = <vector[vector[float]]>file[key + "-index"][idx : idy].tolist()
            data.nodes = <vector[vector[float]]>file[key + "-nodes"][idx : idy].tolist()
            data.loss = <vector[vector[float]]>file[key + "-loss"][idx : idy].tolist()
            data.accuracy = <vector[vector[float]]>file[key + "-accuracy"][idx : idy].tolist()

            for i in file:
                if not "masses" in i: continue
                if "pred"  in i: data.mass_pred[int(i.split("->")[1])]  = <vector[vector[float]]>file[i][idx : idy].tolist()
                if "truth" in i: data.mass_truth[int(i.split("->")[1])] = <vector[vector[float]]>file[i][idx : idy].tolist()
        if   mode == b"training": ptr.train_epoch_kfold(epoch, kfold, &mp_data)
        elif mode == b"validation": ptr.validation_epoch_kfold(epoch, kfold, &mp_data)
        elif mode == b"evaluation": ptr.evaluation_epoch_kfold(epoch, kfold, &mp_data)
        mp_data.clear()
        idx = idy
        idy = idy + chnks

cdef _check_sub(f, str key):
    try: return f.create_group(key)
    except ValueError: return f[key]

cdef struct k_graphed:
    string pkl
    int node_size

cdef class DataLoader:

    cdef CyOptimizer* ptr
    cdef map[string, k_graphed] data
    cdef map[string, k_graphed*] this_batch
    cdef map[int, vector[string]] batch_hash

    cdef int indx_s
    cdef int indx_e
    cdef int kfold
    cdef string mode

    cdef str device
    cdef dict online
    cdef public bool purge
    cdef public sampletracer

    def __cinit__(self):
        self.sampletracer = None
        self.purge = False
        self.online = {}

    def __init__(self): pass
    def __dealloc__(self): pass
    def __len__(self): return self.batch_hash.size()

    cdef DataLoader set_batch(self, int kfold, int batch_size, string mode):
        cdef vector[vector[string]] batches
        if   mode == b"train": batches = self.ptr.fetch_train(kfold, batch_size)
        elif mode == b"valid": batches = self.ptr.fetch_validation(kfold, batch_size)
        elif mode == b"eval":  batches = self.ptr.fetch_evaluation(batch_size)
        else: return self

        self.device = self.sampletracer.Device
        self.this_batch.clear()
        self.batch_hash.clear()
        self.kfold = kfold
        self.mode = mode

        cdef int idx
        cdef string hash_
        cdef int size = batches.size()
        cdef map[string, k_graphed*] to_fetch
        for idx in prange(size, nogil = True, num_threads = size):
            if   mode == b"train": self.batch_hash[idx] = self.ptr.check_train(&batches[idx], kfold)
            elif mode == b"valid": self.batch_hash[idx] = self.ptr.check_validation(&batches[idx], kfold)
            elif mode == b"eval":  self.batch_hash[idx] = self.ptr.check_evaluation(&batches[idx])
            for hash_ in batches[idx]: self.this_batch[hash_] = &self.data[hash_]
            for hash_ in self.batch_hash[idx]: to_fetch[hash_] = &self.data[hash_]
            if self.batch_hash[idx].size(): pass
            else: self.batch_hash[idx] = batches[idx]
        self.indx_e = size

        if not to_fetch.size(): return self
        cdef pair[string, k_graphed*] itr
        cdef vector[string] cfetch = [itr.first for itr in to_fetch]
        cdef list fetch = pdec(&cfetch)
        self.sampletracer.RestoreGraphs(fetch)

        cdef map[string, graph_t] graphs = self.sampletracer.makelist(fetch, True)[1]
        if not graphs.size(): self.ptr.flush_train(&cfetch, self.kfold)
        else: self.sampletracer.FlushGraphs(fetch)

        cdef graph_t* gr
        for idx in prange(graphs.size(), nogil = True, num_threads = graphs.size()):
            gr = &graphs[cfetch[idx]]
            to_fetch[gr.event_hash].pkl = gr.pickled_data
            to_fetch[gr.event_hash].node_size = gr.hash_particle.size()
        graphs.clear()
        return self

    def __iter__(self):
        self.indx_s = 0
        return self

    def __next__(self):
        if self.indx_s == self.indx_e: raise StopIteration
        cdef vector[string]* hash_ = &self.batch_hash[self.indx_s]
        if not len(self.sampletracer.MonitorMemory("Graph")): pass
        elif self.mode.compare(b"train"): self.ptr.flush_train(hash_, self.kfold)
        elif self.mode.compare(b"valid"): self.ptr.flush_validation(hash_, self.kfold)
        elif self.mode.compare(b"eval"):  self.ptr.flush_evaluation(hash_)
        self.indx_s += 1

        cdef list out = []
        cdef string t_hash
        cdef k_graphed* gr
        for t_hash in dereference(hash_):
            try: data = self.online[env(t_hash)]
            except KeyError:
                gr = self.this_batch[t_hash]
                if gr.pkl.size(): pass
                else: return None
                data = pickle.loads(gr.pkl).to(device = self.device)
                self.online[env(t_hash)] = data
            out.append(data)

        cdef int idx = self.sampletracer.MaxGPU
        cdef tuple cuda = (None, None) if idx == -1 else torch.cuda.mem_get_info()

        if cuda[0] is not None and (cuda[1] - cuda[0])/(1024**3) > idx:
            self.purge = True
            data = Batch().from_data_list(out)
            for k in self.online.values(): del k
            torch.cuda.empty_cache()
            return data
        self.purge = False
        return Batch().from_data_list(out)




cdef class cOptimizer:
    cdef CyOptimizer* ptr
    cdef DataLoader data

    cdef dict online_
    cdef map[string, k_graphed] graphs_
    cdef vector[string] cached_

    cdef bool _train
    cdef bool _test
    cdef bool _val


    cdef public metric_plot
    cdef public sampletracer

    def __cinit__(self):
        self.ptr = new CyOptimizer()
        self.data = DataLoader()
        self.data.ptr = self.ptr
        self.metric_plot = MetricPlots()
        self.sampletracer = None
        self._train = False
        self._test = False
        self._val = False

    def __init__(self):
        pass

    def __dealloc__(self):
        del self.ptr

    def length(self):
        return map_to_dict(<map[string, int]>self.ptr.fold_map())

    @property
    def kFolds(self): return self.ptr.use_folds

    cpdef bool GetHDF5Hashes(self, str path):
        if path.endswith(".hdf5"): pass
        else: path += ".hdf5"

        try: f = h5py.File(path, "r")
        except FileNotFoundError: return False

        cdef bool k
        cdef str h_, h__
        cdef map[string, vector[tuple[string, bool]]] res
        for h_ in f: res[enc(h_)] = [(enc(h__), k) for h__, k in f[h_].attrs.items()]
        cdef vector[string] idx = <vector[string]>(list(res))

        cdef int i, j
        cdef map[string, vector[folds_t]] output
        for i in prange(idx.size(), nogil = True, num_threads = idx.size()):
            output[idx[i]] = kfold_build(&idx[i], &res[idx[i]])
            for j in range(output[idx[i]].size()): self.ptr.register_fold(&output[idx[i]][j])
        output.clear()
        return True

    cpdef UseAllHashes(self, list inpt):
        cdef int idx
        cdef folds_t fold_hash
        cdef vector[string] data = penc(inpt)
        for idx in prange(data.size(), nogil = True, num_threads = 12):
            fold_hash = folds_t()
            fold_hash.kfold = 1
            fold_hash.train = True
            fold_hash.event_hash = data[idx]
            self.ptr.register_fold(&fold_hash)
        data.clear()

    def FetchTraining(self, int kfold, int batch_size):
        if self.data.sampletracer is not None: pass
        else: self.data.sampletracer = self.sampletracer
        self._train = True
        self._val = False
        self._test = False
        return self.data.set_batch(kfold, batch_size, b"train")

    def FetchValidation(self, int kfold, int batch_size):
        if self.data.sampletracer is not None: pass
        else: self.data.sampletracer = self.sampletracer
        self._train = False
        self._val = True
        self._test = False
        return self.data.set_batch(kfold, batch_size, b"valid")

    def FetchEvaluation(self, int batch_size):
        if self.data.sampletracer is not None: pass
        else: self.data.sampletracer = self.sampletracer
        self._train = False
        self._val = False
        self._test = True
        return self.data.set_batch(-1, batch_size, b"eval")

    def UseTheseFolds(self, list inpt): self.ptr.use_folds = <vector[int]>inpt

    cpdef AddkFold(self, int epoch, int kfold, dict inpt, dict out_map):
        cdef map[string, data_t] map_data = recast(inpt, out_map)
        if  self._train: self.ptr.train_epoch_kfold(epoch, kfold, &map_data)
        elif  self._val: self.ptr.validation_epoch_kfold(epoch, kfold, &map_data)
        elif self._test: self.ptr.evaluation_epoch_kfold(epoch, kfold, &map_data)
        map_data.clear()

    cpdef FastGraphRecast(self, int epoch, int kfold, list inpt, dict out_map):
        cdef str key
        cdef int i, l
        cdef list graphs
        cdef map[string, data_t] map_data
        for i in trange(len(inpt)):
            graphs = inpt[i].pop("graphs")
            graphs = [Batch().from_data_list(graphs)]
            graphs = [{k : j.numpy(force = True) for k, j in k.to_dict().items()} for k in graphs[0].to_data_list()]
            for k in inpt[i]:
                if not isinstance(inpt[i][k], dict): inpt[i][k] = inpt[i][k].numpy(force = True)
                else: inpt[i][k] = {l : inpt[i][k][l].numpy(force = True) for l in inpt[i][k]}
            inpt[i]["graphs"] = graphs

            map_data = recast(inpt[i], out_map)
            if  self._train: self.ptr.train_epoch_kfold(epoch, kfold, &map_data)
            elif  self._val: self.ptr.validation_epoch_kfold(epoch, kfold, &map_data)
            elif self._test: self.ptr.evaluation_epoch_kfold(epoch, kfold, &map_data)
            map_data.clear()

    cpdef DumpEpochHDF5(self, int epoch, str path, int kfold):

        cdef CyEpoch* ep
        cdef pair[string, data_t] dt
        f = h5py.File(path + str(kfold) + "/epoch_data.hdf5", "w")
        if self.ptr.epoch_train.count(epoch):
            grp = _check_sub(f, "training")
            ep = self.ptr.epoch_train[epoch]
            for dt in ep.container[kfold]: _check_h5(grp, env(dt.first), &dt.second)

        if self.ptr.epoch_valid.count(epoch):
            grp = _check_sub(f, "validation")
            ep = self.ptr.epoch_valid[epoch]
            for dt in ep.container[kfold]: _check_h5(grp, env(dt.first), &dt.second)

        if self.ptr.epoch_test.count(epoch):
            grp = _check_sub(f, "evaluation")
            ep = self.ptr.epoch_test[epoch]
            for dt in ep.container[kfold]: _check_h5(grp, env(dt.first), &dt.second)
        f.close()


    cpdef RebuildEpochHDF5(self, int epoch, str path, int kfold):
        f = h5py.File(path + str(kfold) + "/epoch_data.hdf5", "r")

        cdef str key
        cdef dict unique = {}
        for key in f["training"].keys():
            key = key.split("-")[0]
            if key in unique: pass
            else: unique[key] = None
        _rebuild_h5(f, list(unique), self.ptr, b"training", epoch, kfold)
        _rebuild_h5(f, list(unique), self.ptr, b"validation", epoch, kfold)
        _rebuild_h5(f, list(unique), self.ptr, b"evaluation", epoch, kfold)
        f.close()


    cpdef BuildPlots(self, int epoch, str path):
        self.metric_plot.epoch = epoch
        self.metric_plot.path = path

        cdef CyEpoch* eptr = NULL
        if not self.ptr.epoch_train.count(epoch): pass
        else: eptr = self.ptr.epoch_train[epoch]
        if eptr != NULL: self.metric_plot.AddMetrics(eptr.metrics(), b'training')

        cdef CyEpoch* eptv = NULL
        if not self.ptr.epoch_valid.count(epoch): pass
        else: eptv = self.ptr.epoch_valid[epoch]
        if eptv != NULL: self.metric_plot.AddMetrics(eptv.metrics(), b'validation')

        cdef CyEpoch* eptt = NULL
        if not self.ptr.epoch_test.count(epoch): pass
        else: eptt = self.ptr.epoch_test[epoch]
        if eptt != NULL: self.metric_plot.AddMetrics(eptt.metrics(), b'evaluation')

        if   eptr != NULL: self.metric_plot.ReleasePlots(path)
        elif eptv != NULL: self.metric_plot.ReleasePlots(path)
        elif eptt != NULL: self.metric_plot.ReleasePlots(path)

        if eptr != NULL: del eptr; self.ptr.epoch_train.erase(epoch)
        if eptv != NULL: del eptv; self.ptr.epoch_valid.erase(epoch)
        if eptt != NULL: del eptt; self.ptr.epoch_test.erase(epoch)


