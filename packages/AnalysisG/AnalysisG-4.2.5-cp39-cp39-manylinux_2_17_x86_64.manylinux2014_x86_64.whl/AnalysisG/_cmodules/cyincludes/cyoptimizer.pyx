# distutils: language = c++
# cython: language_level = 3
# cython: c_string_type=unicode, c_string_encoding=utf8

from libcpp.string cimport string, stoi
from libcpp.vector cimport vector
from libcpp.map cimport map, pair
from libcpp cimport tuple
from libcpp cimport bool

from cython.operator cimport dereference
from cython.parallel cimport prange
from cytools cimport env, enc, penc, pdec, map_to_dict, recast
from cyoptimizer cimport CyOptimizer, CyEpoch, CheckDifference
from cytypes cimport folds_t, data_t, metric_t

from AnalysisG._cmodules.cPlots import MetricPlots
import numpy as np

from torch_geometric.data import Batch
import multiprocessing
import psutil
import torch
import h5py
import pickle

cpdef vector[map[string, data_t]] threaded_recast(list inpt, dict out_map):
    dct = multiprocessing.Manager().dict()
    cdef int i
    cdef list jobs = []
    for i in range(len(inpt)):
        p = multiprocessing.Process(target = recast, args = (inpt[i], out_map, i, dct))
        p.start()
        if i%24 == 0:
            jobs += [p]
            for p in jobs: p.join()
            jobs = []
            continue

        jobs.append(p)
    for j in jobs: p.join()
    return list(dct.values())

cdef dict fetch_data(list inpt, map[string, k_graphed*]* gr, bar, str device):
    cdef int i
    cdef k_graphed* gx
    cdef dict output = {}
    for i in range(len(inpt)):
        if not inpt[i].Graph: continue
        x = inpt[i].release_graph()
        x = x.to("cpu", non_blocking = True)
        output[inpt[i].hash] = x.to(device, non_blocking = True)
        gx = dereference(gr)[enc(inpt[i].hash)]
        gx.pkl = pickle.dumps(x)
        gx.online = True
        bar.update(1)
    return output

cdef vector[folds_t] kfold_build(string* hash_, vector[tuple[string, bool]]* kf) nogil:
    cdef vector[folds_t] folds
    cdef folds_t fold = folds_t()
    fold.event_hash = dereference(hash_)
    fold.train = False
    fold.train = False
    fold.evaluation = False

    cdef tuple[string, bool] i
    for i in dereference(kf):
        if not i[0].rfind(b"k-", 0): folds.push_back(fold)
        elif not i[0].rfind(b"train", 0): fold.train = True
        elif not i[0].rfind(b"test", 0):fold.test = True
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

cdef void _rebuild_h5(f, str key, data_t* inpt):
    x = np.zeros(f[key + "-truth"].shape)
    f[key + "-truth"].read_direct(x)
    inpt.truth    = <vector[vector[float]]>x.tolist()

    x = np.zeros(f[key + "-pred"].shape)
    f[key + "-pred"].read_direct(x)
    inpt.pred    = <vector[vector[float]]>x.tolist()

    x = np.zeros(f[key + "-index"].shape)
    f[key + "-index"].read_direct(x)
    inpt.index    = <vector[vector[float]]>x.tolist()

    x = np.zeros(f[key + "-nodes"].shape)
    f[key + "-nodes"].read_direct(x)
    inpt.nodes    = <vector[vector[float]]>x.tolist()

    x = np.zeros(f[key + "-loss"].shape)
    f[key + "-loss"].read_direct(x)
    inpt.loss    = <vector[vector[float]]>x.tolist()

    x = np.zeros(f[key + "-accuracy"].shape)
    f[key + "-accuracy"].read_direct(x)
    inpt.accuracy    = <vector[vector[float]]>x.tolist()

    cdef str i
    for i in f:
        if not "masses" in i: continue
        x = np.zeros(f[i].shape)
        f[i].read_direct(x)
        if "pred"  in i: inpt.mass_pred[int(i.split("->")[1])] = <vector[vector[float]]>x.tolist()
        if "truth" in i: inpt.mass_truth[int(i.split("->")[1])] = <vector[vector[float]]>x.tolist()

cdef _check_sub(f, str key):
    try: return f.create_group(key)
    except ValueError: return f[key]

cdef struct k_graphed:
    string pkl
    bool online

cdef class cOptimizer:
    cdef CyOptimizer* ptr
    cdef dict _kModel
    cdef dict _kOptim
    cdef bool _train
    cdef bool _test
    cdef bool _val

    cdef dict online_
    cdef map[string, k_graphed] graphs_
    cdef vector[string] cached_
    cdef public metric_plot

    def __cinit__(self):
        self.ptr = new CyOptimizer()
        self._train = False
        self._test  = False
        self._val   = False
        self.online_ = {}

        self.metric_plot = MetricPlots()

    def __init__(self): pass
    def __dealloc__(self): del self.ptr
    def length(self): return map_to_dict(<map[string, int]>self.ptr.fold_map())

    @property
    def kFolds(self): return self.ptr.use_folds

    cpdef bool GetHDF5Hashes(self, str path):
        if path.endswith(".hdf5"): pass
        else: path += ".hdf5"

        try: f = h5py.File(path, "r")
        except FileNotFoundError: return False


        cdef int i, j
        cdef map[string, vector[folds_t]] output
        cdef map[string, vector[tuple[string, bool]]] res = {hash_ : list(f[hash_].attrs.items()) for hash_ in f}
        cdef vector[string] idx = <vector[string]>(list(res))
        for i in prange(idx.size(), nogil = True, num_threads = idx.size()):
            output[idx[i]] = kfold_build(&idx[i], &res[idx[i]])
            for j in range(output[idx[i]].size()): self.ptr.register_fold(&output[idx[i]][j])
        output.clear()
        return True

    cpdef UseAllHashes(self, dict inpt):
        cdef int idx
        cdef folds_t fold_hash
        cdef pair[string, vector[string]] itr
        cdef map[string, vector[string]] data = inpt["graph"]
        for itr in data:
            for idx in prange(itr.second.size(), nogil = True, num_threads = 12):
                fold_hash = folds_t()
                fold_hash.kfold = 1
                fold_hash.train = True
                fold_hash.event_hash = itr.second[idx]
                self.ptr.register_fold(&fold_hash)
        data.clear()

    cpdef MakeBatch(self, sampletracer, vector[string] batch, int kfold):
        cdef string x
        cdef tuple cuda
        cdef vector[string] lst_

        if   self._train: lst_ = self.ptr.check_train(&batch, kfold)
        elif   self._val: lst_ = self.ptr.check_validation(&batch, kfold)
        elif  self._test: lst_ = self.ptr.check_evaluation(&batch)
        if not lst_.size(): return Batch().from_data_list([self.online_[env(x)] for x in batch])
        self.frost([lst_], batch.size(), sampletracer)

        if len(sampletracer.MonitorMemory("Graph")):
            if  self._train: self.ptr.flush_train(&lst_, kfold)
            elif  self._val: self.ptr.flush_validation(&lst_, kfold)
            elif self._test: self.ptr.flush_evaluation(&lst_)
            self.FlushRunningCache(True)

        if sampletracer.MaxGPU != -1: pass
        else: return Batch().from_data_list([self.online_[env(x)] for x in batch])

        cuda = torch.cuda.mem_get_info()
        if (cuda[1] - cuda[0])/(1024**3) > sampletracer.MaxGPU:
            self.FlushRunningCache(True)
            torch.cuda.empty_cache()

        return Batch().from_data_list([self.online_[env(x)] for x in batch])

    cpdef frost(self, vector[vector[string]] inpt, int batch_size, sampletracer):

        cdef vector[string] itx, full
        for itx in inpt: full.insert(full.end(), itx.begin(), itx.end())

        cdef list fetch = []
        cdef pair[string, int] itm_
        cdef map[string, int] itm = CheckDifference(full, self.cached_, sampletracer.Threads)

        cdef k_graphed* gr
        cdef map[string, k_graphed*] tmp
        for itm_ in itm:
            gr = &self.graphs_[itm_.first]
            if itm_.second and gr.online: continue
            elif itm_.second and not gr.online:
                self.online_[itm_.second] = pickle.loads(gr.pkl).to(sampletracer.Device)
                gr.online = True
                continue
            self.cached_.push_back(itm_.first)
            fetch.append(env(env(itm_.first)))
            tmp[itm_.first] = gr

        if not len(fetch): return
        _, bar = sampletracer._makebar(len(fetch), "Transferring Graphs to " + sampletracer.Device)
        sampletracer.RestoreGraphs(fetch)
        cdef list these = sampletracer[fetch] if len(fetch) > 1 else [sampletracer[fetch]]
        cdef dict load = fetch_data(these, &tmp, bar, sampletracer.Device)
        self.online_.update(load)
        sampletracer.FlushGraphs(fetch)
        tmp.clear()
        del bar

    def FetchTraining(self, int kfold, int batch_size):
        self._train = True
        self._test  = False
        self._val   = False
        return self.ptr.fetch_train(kfold, batch_size)

    def FetchValidation(self, int kfold, int batch_size):
        self._train = False
        self._test  = False
        self._val   = True
        return self.ptr.fetch_validation(kfold, batch_size)

    def FetchEvaluation(self, int batch_size):
        self._train = False
        self._test  = True
        self._val   = False
        return self.ptr.fetch_evaluation(batch_size)

    def UseTheseFolds(self, list inpt): self.ptr.use_folds = <vector[int]>inpt

    cdef void FlushRunningCache(self, bool flush):
        if not flush: return
        cdef string x
        cdef int index = int(len(self.online_)*0.1)
        for x, i in self.online_.items():
            self.graphs_[x].online = False
            del i
            if index == 0: break
            index -= 1

    cpdef AddkFold(self, int epoch, int kfold, dict inpt, dict out_map):
        cdef map[string, data_t] map_data = recast(inpt, out_map)
        if  self._train: self.ptr.train_epoch_kfold(epoch, kfold, &map_data)
        elif self._test: self.ptr.evaluation_epoch_kfold(epoch, kfold, &map_data)
        elif  self._val: self.ptr.validation_epoch_kfold(epoch, kfold, &map_data)
        map_data.clear()
        graphs = []

    cpdef FastGraphRecast(self, int epoch, int kfold, list inpt, dict out_map):
        cdef int i, l
        cdef list graphs
        cdef str key
        for i in range(len(inpt)):
            graphs = inpt[i].pop("graphs")
            graphs = [Batch().from_data_list(graphs)]
            graphs = [{k : j.numpy(force = True) for k, j in k.to_dict().items()} for k in graphs[0].to_data_list()]
            for k in inpt[i]:
                if not isinstance(inpt[i][k], dict): inpt[i][k] = inpt[i][k].numpy(force = True)
                else: inpt[i][k] = {l : inpt[i][k][l].numpy(force = True) for l in inpt[i][k]}
            inpt[i]["graphs"] = graphs

        cdef map[string, data_t] map_data
        for map_data in threaded_recast(inpt, out_map):
            if  self._train: self.ptr.train_epoch_kfold(epoch, kfold, &map_data)
            elif self._test: self.ptr.evaluation_epoch_kfold(epoch, kfold, &map_data)
            elif  self._val: self.ptr.validation_epoch_kfold(epoch, kfold, &map_data)
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
        cdef map[string, data_t] ep_k

        for key in f["training"].keys():
            key = key.split("-")[0]
            if key in unique: pass
            else: unique[key] = None

        cdef CyEpoch* ep
        for key in unique:
            ep_k[enc(key)] = data_t()
            _rebuild_h5(f["training"], key, &ep_k[enc(key)])
        self.ptr.train_epoch_kfold(epoch, kfold, &ep_k)
        ep_k.clear()

        for key in unique:
            ep_k[enc(key)] = data_t()
            _rebuild_h5(f["validation"], key, &ep_k[enc(key)])
        self.ptr.validation_epoch_kfold(epoch, kfold, &ep_k)
        ep_k.clear()

        for key in unique:
            ep_k[enc(key)] = data_t()
            _rebuild_h5(f["evaluation"], key, &ep_k[enc(key)])
        self.ptr.evaluation_epoch_kfold(epoch, kfold, &ep_k)
        ep_k.clear()
        f.close()

    cpdef BuildPlots(self, int epoch, str path):
        self.metric_plot.epoch = epoch
        self.metric_plot.path = path
        cdef CyEpoch* eptr
        if self.ptr.epoch_train.count(epoch):
            eptr = self.ptr.epoch_train[epoch]
            self.metric_plot.AddMetrics(eptr.metrics(), b'training')
            self.ptr.epoch_train.erase(epoch)
            del eptr

        cdef CyEpoch* epva
        if self.ptr.epoch_valid.count(epoch):
            epva = self.ptr.epoch_valid[epoch]
            self.metric_plot.AddMetrics(epva.metrics(), b'validation')
            self.ptr.epoch_valid.erase(epoch)
            del epva

        cdef CyEpoch* epte
        if self.ptr.epoch_test.count(epoch):
            epte = self.ptr.epoch_test[epoch]
            self.metric_plot.AddMetrics(epte.metrics(), b'evaluation')
            self.ptr.epoch_test.erase(epoch)
            del epte

        self.metric_plot.ReleasePlots(path)


