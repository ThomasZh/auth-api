#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2023 cyber-life.cn
# thomas@cyber-life.cn

import logging
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "./"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
from foo.comm import *
from foo.global_const import *
from foo.dao.mysql_util import *


'''
预排序遍历树算法(modified preorder tree traversal algorithm)

参考：https://www.cnblogs.com/analyzer/articles/1029395.html

注意：由于"left"和"right"在 SQL中有特殊的意义，所以我们需要用"lft"和"rgt"来表示左右字段。
另外这种结构中不再需要"parent"字段来表示树状结构。也就是说下面这样的表结构就足够了。

+------------+-----+-----+
| name | lft | rgt |
+------------+-----+-----+
| Food | 1 | 18 |
| Fruit | 2 | 11 |
| Red | 3 | 6 |
| Cherry | 4 | 5 |
| Yellow | 7 | 10 |
| Banana | 8 | 9 |
| Meat | 12 | 17 |
| Beef | 13 | 14 |
| Pork | 15 | 16 |
+------------+-----+-----+

但是，我们仍然保留"parent"字段。
从数据库拿出数组后，通过python函数将其转换为为树状结构。
然后，提供给界面程序使用
+-----------------------+-----+-----+
| parent | title | lft | rgt |
+-----------------------+-----+-----+
| | Food | 1 | 18 |
| Food | Fruit | 2 | 11 |
| Fruit | Red | 3 | 6 |
| Red | Cherry | 4 | 5 |
| Fruit | Yellow | 7 | 10 |
| Yellow | Banana | 8 | 9 |
| Food | Meat | 12 | 17 |
| Meat | Beef | 13 | 14 |
| Meat | Pork | 15 | 16 |
+-----------------------+-----+-----+
'''

class SysTreeDao():
    def insert(self, id,pid,rootid,title,description,lft,rgt,depth):
        sql = """INSERT INTO sys_tree
                 (id,pid,rootid,title,description,lft,rgt,depth)
                 VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (id,pid,rootid,title,description,lft,rgt,depth)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().insert_one(sql, params)
        return rowcount


    def update(self, id, title, description):
        sql = """UPDATE sys_tree
                 SET title=%s,description=%s
                 WHERE id=%s"""
        params = (title, description, id)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def increase_lft(self, rootid,lft):
        sql = """UPDATE sys_tree
                 SET lft=lft+2
                 WHERE rootid=%s
                 AND lft>%s"""
        params = (rootid,lft)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def increase_lft_num(self, rootid,lft,num):
        sql = """UPDATE sys_tree
                 SET lft=lft+%s
                 WHERE rootid=%s
                 AND lft>%s"""
        params = (num,rootid,lft)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def increase_lft_num_between(self, rootid,lft,rgt,num):
        sql = """UPDATE sys_tree
                 SET lft=lft+%s
                 WHERE rootid=%s
                 AND lft>=%s
                 AND rgt<=%s"""
        params = (num,rootid,lft,rgt)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def increase_rgt(self, rootid,rgt):
        sql = """UPDATE sys_tree
                 SET rgt=rgt+2
                 WHERE rootid=%s
                 AND rgt>%s"""
        params = (rootid,rgt)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def increase_rgt_num(self, rootid,rgt,num):
        sql = """UPDATE sys_tree
                 SET rgt=rgt+%s
                 WHERE rootid=%s
                 AND rgt>%s"""
        params = (num,rootid,rgt)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def increase_rgt_num_between(self, rootid,lft,rgt,num):
        sql = """UPDATE sys_tree
                 SET rgt=rgt+%s
                 WHERE rootid=%s
                 AND lft>=%s
                 AND rgt<=%s"""
        params = (num,rootid,lft,rgt)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def decrease_lft(self, rootid,lft):
        sql = """UPDATE sys_tree
                 SET lft=lft-2
                 WHERE rootid=%s
                 AND lft>%s"""
        params = (rootid,lft)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def decrease_lft_num(self, rootid,lft,num):
        sql = """UPDATE sys_tree
                 SET lft=lft-%s
                 WHERE rootid=%s
                 AND lft>%s"""
        params = (num,rootid,lft)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def decrease_lft_num_between(self, rootid,lft,rgt,num):
        sql = """UPDATE sys_tree
                 SET lft=lft-%s
                 WHERE rootid=%s
                 AND lft>=%s
                 AND rgt<=%s"""
        params = (num,rootid,lft,rgt)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def decrease_rgt(self, rootid,rgt):
        sql = """UPDATE sys_tree
                 SET rgt=rgt-2
                 WHERE rootid=%s
                 AND rgt>%s"""
        params = (rootid,rgt)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def decrease_rgt_num(self, rootid,rgt,num):
        sql = """UPDATE sys_tree
                 SET rgt=rgt-%s
                 WHERE rootid=%s
                 AND rgt>%s"""
        params = (num,rootid,rgt)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def decrease_rgt_num_between(self, rootid,lft,rgt,num):
        sql = """UPDATE sys_tree
                 SET rgt=rgt-%s
                 WHERE rootid=%s
                 AND lft>=%s
                 AND rgt<=%s"""
        params = (num,rootid,lft,rgt)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def update_rgt(self, id, rgt):
        sql = """UPDATE sys_tree
                 SET rgt=%s
                 WHERE id=%s"""
        params = (rgt, id)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def update_pid(self, rootid, id, pid):
        sql = """UPDATE sys_tree
                 SET pid=%s
                 WHERE rootid=%s
                 AND id=%s"""
        params = (pid, rootid, id)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def update_depth(self, rootid, id, depth):
        sql = """UPDATE sys_tree
                 SET depth=%s
                 WHERE rootid=%s
                 AND id=%s"""
        params = (depth, rootid, id)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def update_lft_rgt(self, rootid, id, lft, rgt):
        sql = """UPDATE sys_tree
                 SET lft=%s,rgt=%s
                 WHERE rootid=%s
                 AND id=%s"""
        params = (lft,rgt, rootid, id)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def update_status(self, rootid, id, status):
        sql = """UPDATE sys_tree
                 SET status=%s
                 WHERE rootid=%s
                 AND id=%s"""
        params = (status, rootid, id)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def select(self, id):
        sql = """SELECT id,pid,rootid,title,description,lft,rgt,depth,status,num
                 FROM sys_tree
                 WHERE id=%s"""
        params = (id,)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data


    def select_tree(self, rootid, lft, rgt):
        sql = """SELECT id,pid,rootid,title,description,lft,rgt,depth,status,num
                 FROM sys_tree
                 WHERE rootid=%s
                 AND lft BETWEEN %s AND %s
                 ORDER BY lft ASC"""
        params = (rootid, lft, rgt)
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        return datas


    def select_roots_table(self, idx, limit):
        # SYS_TREE_ROOT_PID = "00000000000000000000000000000000"
        sql = """SELECT id,pid,rootid,title,description,lft,rgt,depth,status,num
                 FROM sys_tree
                 WHERE pid=%s
                 LIMIT %s,%s
              """
        params = (SYS_TREE_ROOT_PID, idx, limit)
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        return datas


    def count_roots_table(self):
        # SYS_TREE_ROOT_PID = "00000000000000000000000000000000"
        sql = """SELECT count(1) AS count
                 FROM sys_tree
                 WHERE pid=%s
              """
        params = (SYS_TREE_ROOT_PID)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        if data:
            return data['count']
        else:
            return 0


    def delete(self, id):
        sql = """DELETE FROM sys_tree
                 WHERE id=%s"""
        params = (id)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().delete(sql, params)
        return rowcount


    def delete_by_lft_rgt(self, rootid, lft, rgt):
        sql = """DELETE FROM sys_tree
                 WHERE rootid=%s
                 AND lft>=%s
                 AND rgt<=%s"""
        params = (rootid, lft, rgt)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().delete(sql, params)
        return rowcount


    def update_num(self, id, num):
        sql = """UPDATE sys_tree
                 SET num=%s
                 WHERE id=%s"""
        params = (num, id)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data
