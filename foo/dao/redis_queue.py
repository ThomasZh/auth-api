#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2021 cyber-life.cn
# thomas@cyber-life.cn

import redis
import logging
import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
from comm import Singleton
from foo.svc_config import *


class RedisQueue(object):
    __connection = None;


    def __init__(self, name, namespace='queue'):
        if self.__connection is None:
            connection = redis.Redis(host=GlobalConfig().redis_host, port=GlobalConfig().redis_port, db=GlobalConfig().redis_db, password=GlobalConfig().redis_pwd)
            self.__connection = connection
            logging.info("redis_dao__connection redis://%s:%d/%s has inited......", GlobalConfig().redis_host, GlobalConfig().redis_port, GlobalConfig().redis_db);
            self.key = '%s:%s' %(namespace, name)


    def qsize(self):
        return self.__connection.llen(self.key)  # 返回队列里面list内元素的数量


    def put(self, item):
        self.__connection.rpush(self.key, item)  # 添加新元素到队列最右方


    def get_wait(self, timeout=None):
        # 返回队列第一个元素，如果为空则等待至有元素被加入队列（超时时间阈值为timeout，如果为None则一直等待）
        item = self.__connection.blpop(self.key, timeout=timeout)
        if item:
            item = item[1]  # 返回值为一个tuple
        return item


    def get_nowait(self):
        # 直接返回队列第一个元素，如果队列为空返回的是None
        item = self.__connection.lpop(self.key)
        return item
