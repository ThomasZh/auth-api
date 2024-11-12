# coding=utf-8
# import ConfigParser # python2.6
import configparser # python3.7
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "./"))

import logging
from comm import Singleton


class GlobalConfig(Singleton):
    __loaded = None;

    def __init__(self):
        if self.__loaded is None:
            self.load("/opt/formas/conf/auth-api.cfg")
            self.__loaded = "loaded"

    def load(self, cfg_file):
        config = configparser.ConfigParser()
        default_cfg_file = "/opt/formas/conf/auth-api.cfg"
        if cfg_file:
            default_cfg_file = cfg_file
        ## 设置可选配置文件，最后优先级最高，文件不存在则忽略
        config.read([cfg_file, default_cfg_file])

        # svc
        self.svc_id = config.get('svc', 'id')
        self.svc_name = config.get('svc', 'name')
        self.svc_host = config.get('svc', 'host')
        self.svc_port = config.getint('svc', 'port')

        # mysql
        self.mysql_host = config.get('mysql', 'host')
        self.mysql_port = config.getint('mysql', 'port')
        self.mysql_db = config.get('mysql', 'db')
        self.mysql_usr = config.get('mysql', 'usr')
        self.mysql_pwd = config.get('mysql', 'pwd')
        self.mysql_charset = config.get('mysql', 'charset')
        self.pool_min_idle_connections = config.getint('mysql', 'pool_min_idle_connections')
        self.pool_max_idle_connections = config.getint('mysql', 'pool_max_idle_connections')
        self.pool_max_recycle_sec = config.getint('mysql', 'pool_max_recycle_sec')
        self.pool_max_open_connections = config.getint('mysql', 'pool_max_open_connections')
        self.mysql_cursorclass = config.get('mysql', 'cursorclass')

        # redis
        self.redis_host = config.get('redis', 'host')
        self.redis_port = config.getint('redis', 'port')
        self.redis_pwd = config.get('redis', 'pwd')
        self.redis_db = config.getint('redis', 'db')

        # log
        log_level = config.get('log', 'level')
        if log_level == 'DEBUG':
            self.log_level = logging.DEBUG
        elif log_level == 'INFO':
            self.log_level = logging.INFO
        elif log_level == 'WARNING':
            self.log_level = logging.WARNING
        elif log_level == 'ERROR':
            self.log_level = logging.ERROR
        elif log_level == 'CRITICAL':
            self.log_level = logging.CRITICAL
        self.log_path = config.get('log', 'path')

        # 存储
        self.storage_tmp_path = config.get('storage', 'tmp_path')
        self.storage_static_path = config.get('storage', 'static_path')
        self.storage_static_domain = config.get('storage', 'static_domain')

        # jwt私钥
        self.jwt_secret = config.get('jwt', 'secret')

        # camunda
        self.camunda_host = config.get('camunda', 'host')
        self.camunda_port = config.getint('camunda', 'port')
