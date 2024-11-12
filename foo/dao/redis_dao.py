# coding=utf-8
import redis
import logging
import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
from comm import Singleton
from foo.svc_config import *


class redis_dao(Singleton):
    __connection = None;

    def __init__(self):
        if self.__connection is None:
            connection = redis.Redis(host=GlobalConfig().redis_host, port=GlobalConfig().redis_port, db=GlobalConfig().redis_db, password=GlobalConfig().redis_pwd)
            self.__connection = connection
            logging.info("redis_dao__connection redis://%s:%d/%s has inited......", GlobalConfig().redis_host, GlobalConfig().redis_port, GlobalConfig().redis_db);


    def keys(self, patten):
        return self.__connection.keys(patten)


    def delete(self, key):
        return self.__connection.delete(key)


    def get_object(self, key):
        strJson = self.__connection.get(key)
        if strJson:
            obj = json.loads(strJson) # Decode into a Python object
            return obj
        else:
            return None


    def put_object(self, key, value):
        if value:
            strJson = json.dumps(value) # Encode the data
            return self.__connection.set(key, strJson)
        else:
            return False


    def get_string(self, key):
        return self.__connection.get(key)


    def put_string(self, key, value):
        return self.__connection.set(key, value)


    def set_expire(self, key, expire):
        return self.__connection.expire(key, expire)
