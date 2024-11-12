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


class AuthAccountRoleDao():
    def select_roles_pagination(self, accountId, start, limit):
        sql = """SELECT a.id,a.name,a.status,a.ctime
                 FROM auth_role a,auth_account_role b
                 WHERE a.id=b.roleId AND b.accountId=%s
                 ORDER BY a.ctime DESC
                 LIMIT %s,%s"""
        params = (accountId,start,limit)
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        return datas


    def count_roles(self, accountId):
        sql = """SELECT count(1) AS count
                 FROM auth_role a,auth_account_role b
                 WHERE a.id=b.roleId
                 AND b.accountId=%s"""
        params = (accountId,)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data['count']


    def select_accounts_pagination(self, roleId, start, limit):
        sql = """SELECT a.id AS accountId,a.username,a.status,a.ctime
                 FROM auth_account a,auth_account_role b
                 WHERE a.id=b.accountId
                 AND b.roleId=%s
                 ORDER BY a.ctime DESC
                 LIMIT %s,%s"""
        params = (roleId,start,limit)
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        return datas


    def count_accounts(self, roleId):
        sql = """SELECT count(1) AS count
                 FROM auth_account a,auth_account_role b
                 WHERE a.id=b.accountId
                 AND b.roleId=%s"""
        params = (roleId,)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data['count']


    def insert(self, accountId,roleId):
        sql = """INSERT INTO auth_account_role (accountId,roleId)
                 VALUES(%s, %s)"""
        params = (accountId, roleId)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().insert_one(sql, params)
        return rowcount


    def delete(self, accountId,roleId):
        sql = """DELETE FROM auth_account_role
                 WHERE accountId=%s
                 AND roleId=%s"""
        params = (accountId, roleId)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().delete(sql, params)
        return rowcount


    def count(self, accountId,roleId):
        sql = """SELECT count(1) AS count
                 FROM auth_account_role
                 WHERE roleId=%s
                 AND accountId=%s"""
        params = (roleId, accountId)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data['count']
