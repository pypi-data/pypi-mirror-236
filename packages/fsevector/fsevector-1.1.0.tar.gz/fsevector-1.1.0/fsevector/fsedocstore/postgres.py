import json, psycopg2
from psycopg2 import pool
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from threading import RLock
import logging
from typing import (
    TYPE_CHECKING,
    Optional
)

minconn = 1
maxconn = 10

class PostgresDB:
    def __init__(self, logger: Optional[logging.Logger] = None, host="127.0.0.1", port="5432", user="admin", password="123456", name="knowledge_test"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.name = name
        self.logger = logger or logging.getLogger(__name__)
        self.lock = RLock()

        # connect postgres
        conn = psycopg2.connect(database="postgres", user=self.user, password=self.password, host=self.host, port=self.port)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute("SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower(%s)", (self.name,))

        # if db is not exist, create db
        if cursor.fetchone() is None:
            cursor.execute("CREATE DATABASE {}".format(self.name))
        cursor.close()
        conn.close()

        # create tables
        conn = psycopg2.connect(database=self.name, user=self.user, password=self.password, host=self.host, port=self.port)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS docs (
                        docid text PRIMARY KEY,
                        textcontent text,
                        metadata text,
                        cts BIGINT DEFAULT EXTRACT(EPOCH FROM NOW())::BIGINT,
                        uts BIGINT DEFAULT EXTRACT(EPOCH FROM NOW())::BIGINT,
                        dts BIGINT DEFAULT 0)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS keywords (
                        keyid SERIAL PRIMARY KEY, docid text, keycontent text,
                        cts BIGINT DEFAULT EXTRACT(EPOCH FROM NOW())::BIGINT,
                        uts BIGINT DEFAULT EXTRACT(EPOCH FROM NOW())::BIGINT,
                        dts BIGINT DEFAULT 0)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS features (
                        featureid SERIAL PRIMARY KEY, docid text, keyid integer, feature text,
                        cts BIGINT DEFAULT EXTRACT(EPOCH FROM NOW())::BIGINT,
                        uts BIGINT DEFAULT EXTRACT(EPOCH FROM NOW())::BIGINT,
                        dts BIGINT DEFAULT 0)''')
        conn.commit()
        cursor.close()
        conn.close()
        # set default index
        self.logger.info('create all tables success')

        # create postgres connect pool
        self.pg_pool = psycopg2.pool.ThreadedConnectionPool(minconn, maxconn, dbname=self.name, user=self.user, 
                                                          password=self.password, host=self.host, port=self.port)

        self.logger.info('PostgresDB init success')

    @contextmanager
    def get_resource(self, RealDictCursor = False) :
        conn = self.pg_pool.getconn()
        
        if RealDictCursor == True:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
        else:
            cursor = conn.cursor()
        try:
            yield cursor, conn
        finally:
            cursor.close()
            self.pg_pool.putconn(conn)

    def shutdown_pool(self):
        if self.pg_pool is not None:
            self.pg_pool.closeall()

    def clear(self):
        with self.lock:
            with self.get_resource() as (cursor, conn):
                cursor.execute('DELETE FROM docs')
                cursor.execute('DELETE FROM keywords')
                cursor.execute('DELETE FROM features')
                conn.commit()
        self.logger.info('PostgresDB clear success')

    def add_key(self, key: str, docid: str, base64str: str) -> int:
        # check
        if key == '' or docid == '' or base64str == '':
            self.logger.warning('add key fail, key or docid or keyvector is empty')
            return -1
        # add

        with self.lock:
            with self.get_resource() as (cursor, conn):
                cursor.execute('INSERT INTO keywords (docid, keycontent) VALUES(%s,%s) RETURNING keyid;', (docid, key))
                keyid = cursor.fetchone()[0]
                cursor.execute('INSERT INTO features (docid, keyid, feature) VALUES(%s,%s,%s) RETURNING featureid;', (docid, keyid, base64str))
                featureid = cursor.fetchone()[0]
                conn.commit()

        self.logger.info('add key: %s success', key)
        return featureid

    def add_doc(self, docid: str, textcontent: str, metadata: str, base64str: str) -> int:
        # check
        if docid == '' or textcontent == '':
            self.logger.error('docid or doccontent is null')
            return -1

        # add
        with self.lock:
            with self.get_resource() as (cursor, conn):
                cursor.execute('INSERT INTO docs (docid, textcontent, metadata) VALUES(%s,%s,%s);', (docid, textcontent, metadata))
                cursor.execute('INSERT INTO features (docid, keyid, feature) VALUES(%s,%s,%s) RETURNING featureid;', (docid, -1, base64str))
                featureid = cursor.fetchone()[0]
                conn.commit()

        self.logger.info('add docid: %s success', docid)
        return featureid

    def get_doc_by_docid(self, docid: str):
        with self.get_resource() as (cursor, conn):
            # check
            if docid == '':
                cursor.execute('SELECT docid, textcontent, metadata FROM docs')
                self.logger.warning('docid is empty, query all docs')
            else:
                cursor.execute('SELECT docid, textcontent, metadata FROM docs WHERE docid=%s', (docid,))
            rows = cursor.fetchall()
            conn.commit()

        return rows

    def get_doccontent_by_docid(self, docid: str) -> str:
        # check
        if docid == '':
            self.logger.warning('docid is empty')
            return ''

        with self.get_resource() as (cursor, conn):
            cursor.execute('SELECT textcontent FROM docs WHERE docid=%s', (docid,))
            rows = cursor.fetchall()
            conn.commit()

        if len(rows) == 0:
            return ''
        else:
            return rows[0][0]

    def get_dict_docid_content_dict_docid_metadata_by_docids(self, doc_list: list) -> [dict, dict]:
        str = ', '.join("'{}'".format(docid) for docid in doc_list)
        query_sql = 'SELECT docid, textcontent, metadata FROM docs WHERE docid IN (' + str + ')'
        with self.get_resource() as (cursor, conn):
            cursor.execute(query_sql)
            rows = cursor.fetchall()
            conn.commit()

        dict_docid_content = {}
        dict_docid_metadata = {}
        for docid, textcontent, metadata in rows:
            dict_docid_content.setdefault(docid, textcontent)
            dict_docid_metadata.setdefault(docid, metadata)
        return dict_docid_content, dict_docid_metadata

    def get_key_by_docid(self, docid: str):
        with self.get_resource() as (cursor, conn):
            #check 
            if docid == '':
                cursor.execute('SELECT keyid, docid, keycontent FROM keywords')
                self.logger.warning('docid is empty, query all docs')
            else:
                cursor.execute('SELECT keyid, docid, keycontent FROM keywords WHERE docid=%s', (docid, ))

            rows = cursor.fetchall()
            conn.commit()

        return rows

    def get_keycontent_by_docid(self, docid: str) -> list:
        with self.get_resource() as (cursor, conn):
            #check 
            if docid == '':
                cursor.execute('SELECT keycontent FROM keywords')
                self.logger.warning('docid is empty, query all docs')
            else:
                cursor.execute('SELECT keycontent FROM keywords WHERE docid=%s', (docid, ))

            rows = cursor.fetchall()
            conn.commit()

        return [item[0] for item in rows]

    def get_dict_keyid_content_by_keyids(self, key_list: list) -> dict:
        with self.get_resource() as (cursor, conn):
            str = ', '.join("'{}'".format(keyid) for keyid in key_list)
            query_sql = 'SELECT keyid, keycontent FROM keywords WHERE keyid IN (' + str + ')'
            cursor.execute(query_sql)
            rows = cursor.fetchall()
            conn.commit()

        result = {}
        for keyid, keyword in rows:
            result.setdefault(keyid, keyword)

        return result

    def get_dict_docid_key_by_docids(self, doc_list: list) -> dict:
        str = ', '.join("'{}'".format(docid) for docid in doc_list)
        query_sql = 'SELECT docid, keycontent FROM keywords WHERE docid IN (' + str + ')'
        with self.get_resource() as (cursor, conn):
            cursor.execute(query_sql)
            rows = cursor.fetchall()
            conn.commit()

        result = {}
        for docid, keyword in rows:
            result.setdefault(docid, []).append(keyword)
        
        return result

    def get_dict_docid_key_and_dict_keyid_content_by_docids(self, doc_list: list) -> [dict, dict]:
        str = ', '.join("'{}'".format(docid) for docid in doc_list)
        query_sql = 'SELECT keyid, docid, keycontent FROM keywords WHERE docid IN (' + str + ')'
        with self.get_resource() as (cursor, conn):
            cursor.execute(query_sql)
            rows = cursor.fetchall()
            conn.commit()

        dict_docid_keycontent = {}
        dict_key_keycontent = {}
        for keyid, docid, keyword in rows:
            dict_docid_keycontent.setdefault(docid, []).append(keyword)
            dict_key_keycontent.setdefault(keyid, keyword)

        return dict_docid_keycontent, dict_key_keycontent

    def get_feature_by_docid(self, docid: str) -> [dict, str]:
        #check 
        with self.get_resource() as (cursor, conn):
            cursor.execute('SELECT feature FROM features WHERE keyid = -1 AND features.docid=%s', (docid, ))
            rows = cursor.fetchall()
            conn.commit()
            if len(rows) == 0:
                return [], ''
            content = rows[0][0]

            cursor.execute('SELECT keywords.keycontent, features.feature FROM features, keywords WHERE keywords.keyid = features.keyid AND features.docid=%s', (docid, ))
            rows = cursor.fetchall()
            conn.commit()

        keyword_dict = {}
        for keyword, feature in rows:
            keyword_dict.setdefault(keyword, feature)

        return keyword_dict, content

    def get_featureid_list_by_docid(self, docid: str) -> list:
        with self.get_resource() as (cursor, conn):
            #check 
            if docid == '':
                cursor.execute('SELECT featureid FROM features')
            else:
                cursor.execute('SELECT featureid FROM features WHERE docid=%s', (docid, ))

            rows = cursor.fetchall()
            conn.commit()

        return [item[0] for item in rows]

    def get_keylist_doclist_featinfo_by_featureids(self, featureids: list) -> [list, list, dict]:
        #check 
        if len(featureids) == 0:
            return []

        with self.get_resource() as (cursor, conn):
            query_sql = 'SELECT featureid, docid, keyid FROM features WHERE featureid IN (' + ', '.join(str(id) for id in featureids) + ')'
            cursor.execute(query_sql)
            rows = cursor.fetchall()
            conn.commit()

        keyid_list = []
        docid_list = []
        featureid_dict = {}
        for featureid, docid, keyid in rows:
            self.logger.debug("[db] featureid: %d, docid: %s, keyid: %d", featureid, docid, keyid)
            keyid_list.append(keyid)
            docid_list.append(docid)
            featureid_dict[featureid] = {"docid": docid, "keyid": keyid}

        self.logger.debug("keyid_list: %s", json.dumps(keyid_list))
        self.logger.debug("docid_list: %s", json.dumps(docid_list))
        self.logger.debug("featureid_dict: %s", json.dumps(featureid_dict))
        return keyid_list, list(set(docid_list)), featureid_dict

    def delete_doc_by_docid(self, docid: str):
        #check 
        if docid == '':
            self.logger.error('docid is empty, delete failed')
            return []

        with self.lock:
            with self.get_resource() as (cursor, conn):
                # 从features表中根据docid先删除特征(包括从关键字提取的特征和从正文内容提取的特征)
                cursor.execute('DELETE FROM features WHERE docid=%s', (docid, ))
                conn.commit()

                # 从keywords表中根据docid删除该文档所属的所有关键字(keyid)
                cursor.execute('DELETE FROM keywords WHERE docid=%s', (docid, ))
                conn.commit()

                # 从docs表中根据docid删除该文档
                cursor.execute('DELETE FROM docs WHERE docid=%s', (docid, ))
                conn.commit()

