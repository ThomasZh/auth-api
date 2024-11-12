#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2016 7x24hs.com
# thomas@7x24hs.com
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../dao"))
import logging
from foo.toolkit.cy_json import CyJson
from comm import *
from global_const import *
from base_handler import *
from foo.svc_config import GlobalConfig
from foo.dao.sys_tree_dao import *
from foo.svc.svc_tree import *


# /api/sys/trees/root
# 创建根节点
class SysTreesRootXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            rootid = payload['rootid']
            title = payload['title']
            if "description" in payload:
                description = payload['description']
            else:
                description = None
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        # uuid = generate_uuid_str()
        id = rootid
        pid = SYS_TREE_ROOT_PID
        lft = 1
        rgt = 2
        depth = 0
        SysTreeDao().insert(id,pid,rootid,title,description,lft,rgt,depth)

        response = {
            "errCode": 200,
            "errMsg": "Success",
            "data": id
        }
        self.write_response(response, logger=True)
        return


# /api/sys/trees/node
# 创建子节点
class SysTreesNodeXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            pid = payload['pid']
            title = payload['title']
            if "description" in payload:
                description = payload['description']
            else:
                description = None
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        pnode = SysTreeDao().select(pid)
        if pnode:
            node = {
                "id": generate_uuid_str(),
                "title": title,
                "description": description,
            }
            insert_node_as_last_child(pid, node)

        response = {
            "errCode": 200,
            "errMsg": "Success",
            "data": node['id']
        }
        self.write_response(response, logger=True)
        return


# /api/sys/trees/roots-table
class SysTreesRootsTableXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        currPage = int(self.get_argument('currPage', 1))
        pageSize = int(self.get_argument('pageSize', 20))

        limit = pageSize
        idx = (currPage - 1) * limit
        totalNum = 0
        totalPage = 0

        idx = (currPage - 1) * pageSize
        datas = SysTreeDao().select_roots_table(idx, pageSize)
        totalNum = SysTreeDao().count_roots_table()
        if totalNum % pageSize == 0:
            totalPage = int(totalNum / pageSize)
        else:
            totalPage = int(totalNum / pageSize) + 1

        response = {
            "errCode": 200,
            "errMsg": "Success",
            "currPage": currPage,
            "pageSize": pageSize,
            "totalNum": totalNum,
            "totalPage": totalPage,
            "datas": datas
        }
        self.write_response(response, logger=False)
        return


# /api/sys/trees/{id}
class SysTreeXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def delete(self, id):
        delete_node_and_children(id)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, id):
        try:
            payload = CyJson.loads(self.request.body)
            title = payload['title']
            if "description" in payload:
                description = payload['description']
            else:
                description = None
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        SysTreeDao().update(id, title, description)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


# /api/sys/trees/{rootid}/tree
class SysTreeTreeXHR(BaseHandler):
    # @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, rootid):
        node = SysTreeDao().select(rootid)
        if node:
            datas = SysTreeDao().select_tree(rootid, node['lft'], node['rgt'])
            rs = make_tree(datas, node['pid'], 'pid', 'id')
            # 去除根节点，客户端不需要
            if "children" in rs['tree'][0]:
                res = rs['tree'][0]['children']
            else:
                res = []
            response = {"errCode": 200, "errMsg": "Success", "datas":res, "expandedKeys":rs['expandedKeys']}
        else:
            response = {"errCode": 200, "errMsg": "Success", "datas":[], "expandedKeys":[]}

        self.write_response(response, logger=False)
        return


# /api/sys/trees/{rootid}/table
class SysTreeTableXHR(BaseHandler):
    # @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, rootid):
        node = SysTreeDao().select(rootid)
        if node:
            datas = SysTreeDao().select_tree(rootid, node['lft'], node['rgt'])
            # 去除根节点，客户端不需要
            del datas[0]

            response = {"errCode": 200, "errMsg": "Success", "datas":datas}
        else:
            response = {"errCode": 200, "errMsg": "Success", "datas":[]}

        self.write_response(response, logger=False)
        return


# /api/sys/trees/move
class SysTreesMoveXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self):
        try:
            payload = CyJson.loads(self.request.body)
            srcId = payload["srcId"]
            destId = payload["destId"]
            place = payload["place"]
            relation = payload["relation"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        # 0. 获取原始 node 与子 node 信息
        node = SysTreeDao().select(srcId)
        datas = SysTreeDao().select_tree(node['rootid'], node['lft'], node['rgt'])

        # 1. 删除节点以及其子节点
        delete_node_and_children(srcId)

        # 2. 插入原始 node 与子 node 到新位置
        for data in datas:
            if srcId == data['id']: # 原始node, 第一条记录
                if relation == "brother":
                    if place == "after":
                        insert_node_after_brother(destId, data)
                    elif place == "before":
                        insert_node_before_brother(destId, data)
                elif relation == "child":
                    insert_node_as_first_child(destId, data)
            else:
                insert_node_as_last_child(data['pid'], data)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return
