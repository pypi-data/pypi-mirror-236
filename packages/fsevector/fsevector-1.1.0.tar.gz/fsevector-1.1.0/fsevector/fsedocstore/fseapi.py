import time, math
import numpy as np
# from tqdm import tqdm, trange
import requests
import json
import base64
import asyncio
import aiohttp
import uvloop

# repo params
capacity = 100000000

async def request_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def send_request(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            return await response.text()

async def index_add(index, feats, idxs):
    await index.add_batch(feats, idxs)

async def index_search(index, query, dists, idxs, topk, threshold, normaliztion):
    await index.search_batch(query, dists, idxs, topk, threshold, normaliztion)

def sync_search_batch(index, query, dists, idxs, topk, type, threshold, normaliztion):
    index.sync_search_batch(query, dists, idxs, topk, type, threshold, normaliztion)

def sync_send_request(url, data):
    resp = requests.post(url, data)
    return resp.text

class IndexFse:
    def __init__(self, logger, fse_addr, dim, repo="repo", bgpu=False, itype="int8"):
        self.logger = logger
        self.dim = dim
        self.repo_id = repo
        self.bgpu = bgpu
        self.itype = itype
        self.ntotal = 0
        self.x_api = fse_addr + "/x-api/v1/repositories"

    # feats - features matrix
    # idxs - numeric id of every feature
    def add(self, feats, idxs=None):
        size = feats.shape[0]
        if idxs is None:
            idxs = np.arange(self.ntotal, self.ntotal + size)
        else:
            size = max(size, len(idxs))

        st = time.time()
        batch_size = 1000
        num_iter = math.ceil(size / batch_size)
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        loop = asyncio.get_event_loop()
        for i in range(num_iter):
            batch = batch_size if i != num_iter - 1 else size - i * batch_size
            start = i * batch_size
            loop.run_until_complete(index_add(self, feats[start: start + batch], idxs[start: start + batch]))
        ed = time.time()
        self.logger.info('add feature completed, elapsed: %fs', ed - st)

    async def add_batch(self, feats, idxs):
        size = max(feats.shape[0], len(idxs))

        st = time.time()
        tasks = []
        for i in range(size):
            feat_str = base64.b64encode(feats[i])
            feat_data = {"id": str(idxs[i]),
                         "data": {"value": feat_str.decode(), "type": "feature"},
                         "location_id": "1",
                         "time": 1}
            tasks.append(send_request(self.x_api + "/%s/entities" % self.repo_id, json.dumps(feat_data)))
        await asyncio.gather(*tasks)
        ed = time.time()

        self.ntotal += size
        self.logger.info('add feature success, ntotal: %d, qps: %d', self.ntotal, size / (ed - st))

    def sync_add_batch(self, feats, idxs, type):
        size = max(feats.shape[0], len(idxs))
        location = "key" if type == 'key' else "content"

        st = time.time()
        tasks = []
        for i in range(size):
            feat_str = base64.b64encode(feats[i])
            feat_data = {"id": str(idxs[i]),
                         "data": {"value": feat_str.decode(), "type": "feature"},
                         "location_id": location,
                         "time": 1695091681005}
            sync_send_request(self.x_api + "/%s/entities" % self.repo_id, json.dumps(feat_data))
        ed = time.time()

        self.ntotal += size
        self.logger.info('add feature success, ntotal: %d, qps: %d', self.ntotal, size / (ed - st))

    def sync_search_batch(self, query, dists, idxs, topk, type="key", threshold=0, normaliztion="false"):
        size = query.shape[0]
        location = [] if type == '' else [type]

        st = time.time()
        response = []
        for i in range(size):
            feat_str = base64.b64encode(query[i])
            query_data = {"include": {"data": {"value": feat_str.decode(), "type": "feature"}},
                          "include_threshold": threshold,
                          "repositories": [self.repo_id],
                          "locations": location,
                          "max_candidates": topk,
                          "options": {"normalization": normaliztion}}
            response.append(sync_send_request(self.x_api + "/search", json.dumps(query_data)))

        # convert results
        for i in range(len(response)):
            res_data = json.loads(response[i])
            if "results" not in res_data:
                continue
            results = res_data["results"]
            for j in range(len(results)):
                dists[i][j] = float(results[j]["similarity"])
                idxs[i][j] = int(results[j]["id"])
        ed = time.time()
        self.logger.debug('search success, ntotal: %d, qps: %d', self.ntotal, size / (ed - st))

    # query - query feature
    # topk - topk
    # threshold - similarity threshold
    # normalization - whether conduct score verification
    def sync_search(self, query, topk, type="key", threshold=0, normaliztion="false"):
        size = query.shape[0]
        dists = np.zeros((size, topk), "float")
        #idxs = np.zeros((size, topk), "int32")
        idxs = np.full((size, topk), -1, "int32")

        st = time.time()
        batch_size = 200
        num_iter = math.ceil(size / batch_size)
        for i in range(num_iter):
            batch = batch_size if i != num_iter - 1 else size - i * batch_size
            start = i * batch_size
            sync_search_batch(self, query[start : start + batch],
                                        dists[start : start + batch],
                                        idxs[start : start + batch],
                                        topk, type, threshold, normaliztion)
        ed = time.time()
        self.logger.info('search completed, elapsed: %fs', ed - st)
        return dists, idxs

    # query - query feature
    # topk - topk
    # threshold - similarity threshold
    # normalization - whether conduct score verification
    def search(self, query, topk, threshold=0, normaliztion="false"):
        size = query.shape[0]
        dists = np.zeros((size, topk), "float")
        idxs = np.zeros((size, topk), "int32")

        st = time.time()
        batch_size = 1000
        num_iter = math.ceil(size / batch_size)
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        loop = asyncio.get_event_loop()
        for i in range(num_iter):
            batch = batch_size if i != num_iter - 1 else size - i * batch_size
            start = i * batch_size
            loop.run_until_complete(index_search(self, query[start : start + batch],
                                                       dists[start : start + batch],
                                                       idxs[start : start + batch],
                                                       topk, threshold, normaliztion))
        ed = time.time()
        self.logger.info('search completed, elapsed: %fs', ed - st)
        return dists, idxs

    async def search_batch(self, query, dists, idxs, topk, threshold=0, normaliztion="false"):
        size = query.shape[0]

        st = time.time()
        tasks = []
        for i in range(size):
            feat_str = base64.b64encode(query[i])
            query_data = {"include": {"data": {"value": feat_str.decode(), "type": "feature"}},
                          "include_threshold": threshold,
                          "repositories": [self.repo_id],
                          "max_candidates": topk,
                          "options": {"normalization": normaliztion}}
            tasks.append(send_request(self.x_api + "/search", json.dumps(query_data)))
        response = await asyncio.gather(*tasks)

        # convert results
        for i in range(len(response)):
            res_data = json.loads(response[i])
            if "results" not in res_data:
                continue
            results = res_data["results"]
            for j in range(len(results)):
                dists[i][j] = float(results[j]["similarity"])
                idxs[i][j] = int(results[j]["id"])
        ed = time.time()
        self.logger.info('search success, qps: %d', size / (ed - st))

    def create_repo(self):
        feat_type = "face"
        level = "gpu" if self.bgpu else "ram"
        repo_data = {"id": self.repo_id,
                     "type": feat_type,
                     "index_type": self.itype,
                     "level": level,
                     "capacity": capacity,
                     "default_version": {"feature_length": self.dim},
                     "options": {"UseFeatureIDMap": "true",
                                 "PreFilter": "true"}}

        res = requests.post(self.x_api, json.dumps(repo_data))
        if res.status_code != 201:
            self.logger.error('fail to create repo, response: %s', json.loads(res.content.decode("utf-8")))
            exit(-1)
        self.logger.info('create repo success, repo_id: %s', self.repo_id)

    def delete_repo(self):
        requests.delete(self.x_api + "/%s" % self.repo_id)
        self.logger.info('delete repo, repo_id: %s', self.repo_id)

    def query_repo(self):
        resp = requests.get(self.x_api + "/%s" % self.repo_id)
        return resp

    def query_repo_size(self):
        resp = requests.get(self.x_api + "/%s" % self.repo_id)
        result = json.loads(resp.content.decode('utf-8'))
        if resp.status_code != 200:
            self.logger.error('query repo failed, code: %s, msg: %s', resp.status_code, result)
            return 0
        size = result.get('size')
        if size is not None:
            return size
        else:
            self.logger.info('Key "size" not found in the result')
            return 0

    def query_feature(self, feat_id):
        resp = requests.get(self.x_api + "/%s/entities/%s" % (self.repo_id, feat_id))
        result = json.loads(resp.content.decode('utf-8'))
        if resp.status_code != 200:
            self.logger.error('query feature failed, code: %s, msg: %s', resp.status_code, result)
            return 0
        return result['data']['value']
    
    def delete_feature(self, feat_id) -> int:
        resp = requests.delete(self.x_api + "/%s/entities/%s" % (self.repo_id, feat_id))
        result = json.loads(resp.content.decode('utf-8'))
        if resp.status_code != 200:
            self.logger.error('delete feature failed, code: %s, msg: %s', resp.status_code, result)
            return -1
        else:
            return 0
