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


class AuthAccountGroupDao():
    def select_groups_pagination(self, accountId, start, limit):
        sql = """SELECT a.id,a.title
                 FROM auth_group a, auth_account_group b
                 WHERE a.id=b.groupId
                 AND b.accountId=%s
                 LIMIT %s,%s"""
        params = (accountId,start,limit)
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        return datas


    def count_groups(self, accountId):
        sql = """SELECT count(1) AS count
                 FROM auth_group a, auth_account_group b
                 WHERE a.id=b.groupId
                 AND b.accountId=%s"""
        params = (accountId,)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data['count']


    def select_accounts_pagination(self, groupId, start, limit):
        sql = """SELECT a.id AS accountId,a.username,a.status,a.ctime
                 FROM auth_account a, auth_account_group b
                 WHERE a.id=b.accountId
                 AND b.groupId=%s
                 LIMIT %s,%s"""
        params = (groupId,start,limit)
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        return datas


    def count_accounts(self, groupId):
        sql = """SELECT count(1) AS count
                 FROM auth_account a,auth_account_group b
                 WHERE a.id=b.accountId
                 AND b.groupId=%s"""
        params = (groupId,)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data['count']


    def insert(self, accountId,groupId):
        sql = """INSERT INTO auth_account_group (accountId,groupId)
                 VALUES(%s, %s)"""
        params = (accountId,groupId)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().insert_one(sql, params)
        return rowcount


    def delete(self, accountId,groupId):
        sql = """DELETE FROM auth_account_group
                 WHERE accountId=%s
                 AND groupId=%s"""
        params = (accountId,groupId)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().delete(sql, params)
        return rowcount


    def delete_by_account(self, accountId):
        sql = """DELETE FROM auth_account_group
                 WHERE accountId=%s"""
        params = (accountId,)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().delete(sql, params)
        return rowcount


    def count(self, accountId,groupId):
        sql = """SELECT count(1) AS count
                 FROM auth_account_group
                 WHERE groupId=%s
                 AND accountId=%s"""
        params = (groupId,accountId)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data['count']
