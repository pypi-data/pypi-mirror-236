import os, time, logging, re
import json, base64, struct
import numpy as np
import fsevector.fsedocstore.fseapi as fseapi
import fsevector.fsedocstore.postgres as postgres
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    List,
    Optional
)

logging.basicConfig(format='[%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s] %(message)s', level=logging.INFO)

class FseDoc:
  def __init__(self, dbhost="127.0.0.1", dbport=5432, user="admin", password="123456",
               fsehost="127.0.0.1", fseport=3154, repo="knowledge_test", dim=1536, logger: Optional[logging.Logger] = None):
    self.logger = logger or logging.getLogger()
    self.fse_index = fseapi.IndexFse(self.logger, "http://" + fsehost + ":" + str(fseport), dim, repo, bgpu=False)
    self.my_pgsql = postgres.PostgresDB(self.logger, host=dbhost, port=dbport, user=user, password=password, name=repo)

    response = self.fse_index.query_repo()
    if response.status_code != 200:
      self.fse_index.create_repo()
    self.logger.info('procedures init success')

  def clear(self):
    self.fse_index.delete_repo()
    time.sleep(1)
    self.fse_index.create_repo()
    self.my_pgsql.clear()
    return {"errorcode": "ok"}

  def search(self, embedding: List[float], type = "fulltext", topk = 3, threshold = 0.0):
    self.logger.debug('type: %s, content: %s', type)

    #check params
    if not embedding:
      return {"errorcode": "search embedding field is empty"}

    if type != "key" and type != 'content' and type != 'fulltext':
      return {"errorcode": "search type not support"}

    if type == "fulltext":
      type = ''

    if self.fse_index.query_repo_size() == 0:
      return {"errorcode": "fse repo size is 0"}

    # query from fse
    scores, idx = self.fse_index.sync_search(np.array([embedding], dtype='float32'), topk, type)

    # duplicate removal, generate dict_id_score
    id_list = []
    dict_id_score = {}
    for index, id in enumerate(idx[0]):
      self.logger.debug("search id: %d, score: %f", id, scores[0][index])
      if id > 0 and scores[0][index] >= threshold and id not in id_list:
        id_list.append(id)
        dict_id_score[id] = scores[0][index]

    if len(id_list) == 0:
      return {"errorcode": "not match"}

    #get info from sqlite/postgres
    _, doc_list, featureid_dict = self.my_pgsql.get_keylist_doclist_featinfo_by_featureids(id_list)
    if len(doc_list) == 0:
      return {"errorcode": "not match"}

    self.logger.debug("search doc_list: %s", json.dumps(doc_list))
    # query info from db
    dict_docid_content, dict_docid_metadata = self.my_pgsql.get_dict_docid_content_dict_docid_metadata_by_docids(doc_list)
    dict_docid_key, dict_keyid_content = self.my_pgsql.get_dict_docid_key_and_dict_keyid_content_by_docids(doc_list)
    self.logger.debug("search dict_docid_content: %s", json.dumps(dict_docid_content))
    self.logger.debug("search dict_keyid_content: %s", json.dumps(dict_keyid_content))

    #get info docid->score
    dict_docid_score = {}
    dict_docid_matchkey = {}
    for id in dict_id_score:
      docid = featureid_dict[id]["docid"]
      if docid not in dict_docid_score or dict_id_score[id] > dict_docid_score[docid]:
        dict_docid_score[docid] = dict_id_score[id]
        keycontent = featureid_dict[id]["keyid"]
        dict_docid_matchkey[docid] = dict_keyid_content.get(keycontent, '')

    results = []
    for docid in doc_list:
      # some text has no key
      if docid not in dict_docid_key:
        dict_docid_key[docid] = []

      one_reult = {"id": docid, "key": dict_docid_key[docid], "content": dict_docid_content[docid], "metadata": dict_docid_metadata[docid], "similarity": dict_docid_score[docid]}
      if dict_docid_matchkey[docid] != '':
        one_reult["matchkey"] = dict_docid_matchkey[docid]

      #results.append
      results.append(one_reult)
    results = sorted(results, key=lambda x: x["similarity"], reverse=True)

    return {"results": results, "errorcode": "ok"}

  def is_doc_exist(self, docid: str) -> bool:
    results = self.my_pgsql.get_doc_by_docid(docid)
    if len(results) != 0:
      return True
    else:
      return False

  def add_doc(self, docid: str, content: str, content_embedding: List[float],
              metadata: str = '{}', key_list: List[str] = [], key_embeddings: List[List[float]] = [[]]):
    #check
    if docid == '' or content == '':
      self.logger.error('docid or content field is missing')
      return {"errorcode": "docid or content field is missing"}
    
    #check docid是否已经存在
    if self.is_doc_exist(docid):
      self.logger.warning('docid: %s is existed', docid)
      return {"errorcode": "docid is existed"}

    #先把key 提取向量，入fse、入数据库
    if len(key_list) == 0:
      self.logger.debug('docid: %s, key field is None', docid)
    else:
      for key, key_embedding in zip(key_list, key_embeddings):
        bytes_str = struct.pack('%sf' % len(key_embedding), *key_embedding)
        feat_str = str(base64.b64encode(bytes_str))
        featid = self.my_pgsql.add_key(key, docid, feat_str)
        if featid == -1:
          self.logger.error('docid: %s, add_key failed', docid)
        else:
          self.fse_index.sync_add_batch(np.array([key_embedding], dtype='float32'), [featid], "key")

    # 把body.content 提取向量，入fse、入数据库
    bytes_str = struct.pack('%sf' % len(content_embedding), *content_embedding)
    feat_str = str(base64.b64encode(bytes_str))
    featid = self.my_pgsql.add_doc(docid, content, metadata, feat_str)
    if featid == -1:
      self.logger.error('docid: %s, add_doc failed', docid)
      return {"errorcode": "add_doc failed"}
    else:
      self.fse_index.sync_add_batch(np.array([content_embedding], dtype='float32'), [featid], "content")

    return {"id": docid, "key": key_list, "content": content, "errorcode": "ok"}

  def get_doc(self, docid: str):
    #docid, textcontent, metadata
    sql_results = self.my_pgsql.get_doc_by_docid(docid)
    if len(sql_results) == 0:
      self.logger.warning('docid: %s is not exsit', docid)
      return {"errorcode": "docid is not exsit"}
    
    key_list = self.my_pgsql.get_keycontent_by_docid(docid)
    return {"id": docid, "key": key_list, "content": sql_results[0][1], "metadata": sql_results[0][2], "errorcode": "ok"}

  def delete_doc(self, docid: str):
    #check
    if docid == '':
      return {"errorcode": "docid field is missing"}
    
    # 获取删除文档的所有特征id
    results = self.my_pgsql.get_featureid_list_by_docid(docid)
    # 循环删除fse中特征
    for featid in results:
      self.fse_index.delete_feature(featid)
    # 删除数据库中特征
    self.my_pgsql.delete_doc_by_docid(docid)

    return {"errorcode": "ok"}

  def get_key(self, docid: str):
    doc_content = self.my_pgsql.get_doccontent_by_docid(docid)
    if doc_content == '':
      self.logger.warning('docid: %s is not exsit', docid)
      return {"errorcode": "docid is not exsit"}

    key_list = self.my_pgsql.get_keycontent_by_docid(docid)
    return {"id": docid, "key": key_list, "errorcode": "ok"}

  def get_feature(self, docid: str):
    keyword_dict, content = self.my_pgsql.get_feature_by_docid(docid)
    if content == '':
      return {"errorcode": "docid is not exsit"}
    else:
      return {"results": {"key": keyword_dict, "content": content}, "errorcode": "ok"}

  def get_list(self):
    sql_results = self.my_pgsql.get_doc_by_docid('')
    doc_list = []
    for docid, doccontent, _ in sql_results:
      doc_list.append(docid)

    if len(doc_list) == 0:
      return {"results": {}, "errorcode": "ok"}

    dict_docid_key = self.my_pgsql.get_dict_docid_key_by_docids(doc_list)
    results = []
    for docid, doccontent, metadata in sql_results:
      if docid not in dict_docid_key:
        dict_docid_key[docid] = []
      results.append({"id": docid, "key": dict_docid_key[docid], "content": doccontent, "metadata": metadata})

    return {"results": results, "errorcode": "ok"}
