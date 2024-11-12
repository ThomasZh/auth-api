#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2016 7x24hs.com
# thomas@7x24hs.com

import logging
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "./"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
from foo.comm import *
from foo.dao.mysql_util import *


class AuthPolicyDao():
    def select_pagination(self, start, limit):
        sql = """SELECT id,type,objId,objName,resPath,action,access,priority
                 FROM auth_policy
                 ORDER BY priority ASC LIMIT %s,%s"""
        params = (start,limit)
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        return datas


    def count(self):
        sql = """SELECT count(1) AS count
                 FROM auth_policy"""
        params = ()
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data['count']


    def insert(self, id,type,obj_name,obj_id,res_path,action,access,priority):
        _dt = timestamp_to_datetime(current_timestamp())
        sql = """INSERT INTO auth_policy (id,type,objId,objName,resPath,action,access,priority,ctime)
                 VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (id,type,obj_name,obj_id,res_path,action,access,priority,_dt)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().insert_one(sql, params)
        return rowcount


    def select(self, id):
        sql = """SELECT id,type,objId,objName,resPath,action,access,priority
                 FROM auth_policy
                 WHERE id=%s"""
        params = (id,)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data


    def delete(self, id):
        sql = """DELETE FROM auth_policy
                 WHERE id=%s"""
        params = (id,)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().delete(sql, params)
        return rowcount


    def update(self, id,type,obj_name,obj_id,res_path,action,access,priority):
        sql = """UPDATE auth_policy
                 SET type=%s,objId=%s,objName=%s,resPath=%s,action=%s,access=%s,priority=%s
                 WHERE id=%s"""
        params = (type,obj_name,obj_id,res_path,action,access,priority,id)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def selectPaginationByFilters(self, searchs, orders, idx, limit):
        params = ()
        sql = """SELECT id,type,objId,objName,resPath,action,access,priority
                 FROM auth_policy
                 WHERE 1=1 """

        if searchs and len(searchs) > 0:
            for i in range(len(searchs)):
                search = searchs[i]
                # 当X为None,  False, 空字符串"", 0, 空列表[], 空字典{}, 空元组()这些时，not X为真，即无法分辨出他们之间的不同。
                if "value" in search and (not search['value'] is None):
                    if search['op'] == "like":
                        sql = sql + " AND " + search['column'] + " LIKE %s "
                        params = params + ("%"+search['value']+"%",)
                    elif search['op'] == "eq":
                        sql = sql + " AND " + search['column'] + " = %s "
                        params = params + (search['value'],)

        if orders and len(orders) > 0:
            sql = sql + " ORDER BY "
            for i in range(len(orders)):
                order = orders[i]
                if i == len(orders) -1:
                    sql = sql + order['column'] + " " + order['dir']
                else:
                    sql = sql + order['column'] + " " + order['dir'] + ","
            # sql = sql + ", id" # 额外加个id排序去确保顺序稳定

        sql = sql + " LIMIT %s,%s"
        params = params + (idx, limit)
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        if datas:
            return datas
        else:
            return []


    def countPaginationByFilters(self, searchs):
        params = ()
        sql = """SELECT count(1) AS count
                 FROM auth_policy
                 WHERE 1=1 """

        if searchs and len(searchs) > 0:
            for i in range(len(searchs)):
                search = searchs[i]
                # 当X为None,  False, 空字符串"", 0, 空列表[], 空字典{}, 空元组()这些时，not X为真，即无法分辨出他们之间的不同。
                if "value" in search and (not search['value'] is None):
                    if search['op'] == "like":
                        sql = sql + " AND " + search['column'] + " LIKE %s "
                        params = params + ("%"+search['value']+"%",)
                    elif search['op'] == "eq":
                        sql = sql + " AND " + search['column'] + " = %s "
                        params = params + (search['value'],)

        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data['count']
