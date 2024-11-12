#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2023 cyber-life.cn
# thomas@cyber-life.cn
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
import pymysql
from dbutils.pooled_db import PooledDB
from foo.svc_config import *


pool = PooledDB(
    creator=pymysql,  # 使用 PyMySQL 库进行连接
    maxconnections=GlobalConfig().pool_max_open_connections,  # 连接池中最多同时存在的连接数
    mincached=GlobalConfig().pool_min_idle_connections,  # 初始化时连接池中的空闲连接数量
    maxcached=GlobalConfig().pool_max_idle_connections,  # 连接池中最多存在的空闲连接数量
    host=GlobalConfig().mysql_host,
    port=GlobalConfig().mysql_port,
    user=GlobalConfig().mysql_usr,
    password=GlobalConfig().mysql_pwd,
    database=GlobalConfig().mysql_db,
    charset=GlobalConfig().mysql_charset,
    # cursorclass=pymysql.cursors.DictCursor # 设置为字典的形式返回数据（默认是元组）
    # cursorclass=GlobalConfig().mysql_cursorclass,
)
