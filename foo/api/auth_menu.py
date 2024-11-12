#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2016 7x24hs.com
# thomas@7x24hs.com
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
import logging
from foo.toolkit.cy_json import CyJson
from comm import *
from global_const import *
from base_handler import *
from foo.svc_config import GlobalConfig
from foo.dao.auth_menu_dao import *
from foo.dao.sys_log_dao import *
from foo.svc.svc_tree import *
from foo.svc.svc_menu import *
from foo.dao.auth_account_role_dao import *
from foo.dao.auth_role_menu_dao import *


# /api/auth/v5/menus/{menuId}/tree
class AuthMenusTreeXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, menuId):
        menu = AuthMenuDao().select(menuId)
        if menu:
            datas = AuthMenuDao().select_tree(menu['lft'], menu['rgt'])
            rs = make_tree(datas, menu['pid'], 'pid', 'id')
            response = {"errCode": 200, "errMsg": "Success", "datas":rs['tree'], "expandedKeys":rs['expandedKeys']}
        else:
            response = {"errCode": 200, "errMsg": "Success", "datas":[], "expandedKeys":[]}

        self.write_response(response, logger=False)
        return


# /api/auth/v5/menus/{menuId}/table
class AuthMenusTableXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, menuId):
        menu = AuthMenuDao().select(menuId)
        if menu:
            datas = AuthMenuDao().select_tree(menu['lft'], menu['rgt'])

            response = {"errCode": 200, "errMsg": "Success", "datas":datas}
        else:
            response = {"errCode": 200, "errMsg": "Success", "datas":[]}

        self.write_response(response, logger=False)
        return


# /auth/api/v5/menus
class AuthMenusXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            if "pid" in payload:
                pid = payload['pid']
            if "name" in payload:
                name = payload['name']
            if "path" in payload:
                path = payload['path']
            if "icon" in payload:
                icon = payload['icon']
            if "hideInMenu" in payload:
                hideInMenu = payload['hideInMenu']
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        menu = {
            "id": generate_uuid_str(),
            "name": name,
            "path": path,
            "icon": icon,
            "hideInMenu": hideInMenu,
        }
        insert_menu_as_last_child(pid, menu)

        response = {
            "errCode": 200,
            "errMsg": "Success",
            "data": menu['id'],
        }
        self.write_response(response, logger=True)
        return


# /auth/api/v5/menus/{menuId}
class AuthMenuXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, menuId):
        try:
            payload = CyJson.loads(self.request.body)
            if "name" in payload:
                name = payload['name']
            if "path" in payload:
                path = payload['path']
            if "icon" in payload:
                icon = payload['icon']
            if "hideInMenu" in payload:
                hideInMenu = payload['hideInMenu']
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        AuthMenuDao().update(menuId,name,path,icon,hideInMenu)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def delete(self, menuId):
        AuthMenuDao().delete(menuId)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


# /api/auth/v5/menus/{menuId}/move
class AuthMenusMoveXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, menuId):
        try:
            payload = CyJson.loads(self.request.body)
            objId = payload["objId"]
            place = payload["place"]
            relation = payload["relation"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        # 0. 获取原始 task 与子 task 信息
        menu = AuthMenuDao().select(menuId)
        datas = AuthMenuDao().select_tree(menu['lft'], menu['rgt'])

        # 1. 删除任务以及其子任务
        delete_menu_and_children(menuId)

        # 2. 插入原始 task 与子 task 到新位置
        for data in datas:
            if menuId == data['id']: # 原始task, 第一条记录
                if relation == "brother":
                    if place == "after":
                        insert_menu_after_brother(objId, data)
                    elif place == "before":
                        insert_menu_before_brother(objId, data)
                elif relation == "child":
                    insert_menu_as_first_child(objId, data)
            else:
                insert_menu_as_last_child(data['pid'], data)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


# /api/auth/v5/menus/mine
class AuthMenusMineXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        operId = self.get_account_id()

        menu = AuthMenuDao().select(AUTH_ROOT_MENU_ID)
        if menu:
            datas = AuthMenuDao().select_tree(menu['lft'], menu['rgt'])
            rs = make_menu_tree(datas, menu['pid'], 'pid', 'id')
            # 去除根节点，客户端不需要
            if "children" in rs['tree'][0]:
                res = rs['tree'][0]['children']
            else:
                res = []
        else:
            res = []

        arr = []
        for data in res:
            roles = AuthAccountRoleDao().select_roles_pagination(operId, 0, 100)
            for role in roles:
                count = AuthRoleMenuDao().count(role['id'], data['id'])
                if count > 0:
                    arr.append(data) #此菜单与此角色绑定
                    break

        response = {"errCode": 200, "errMsg": "Success", "datas":arr}
        self.write_response(response, logger=False)
        return
