#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2022 cyber-life.cn
# thomas@cyber-life.cn

import logging
import sys
import os
import requests
import re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from comm import *
from global_const import *
from foo.dao.auth_menu_dao import *


"""
作为第一个 child 被插入
root-lft             parent-lft parent-rgt        root-rgt
|                |--menu--|--parent--|               |
|                |------------parent--|               |
|----------------|---------|----------|---------------|
"""
def insert_menu_as_first_child(pid, menu):
    parentmenu = AuthMenuDao().select(pid)

    # 父节点之后的节点，都需要 +1
    AuthMenuDao().increase_rgt(parentmenu['lft'])
    AuthMenuDao().increase_lft(parentmenu['lft'])

    # 新增加的节点，应放在第一个
    AuthMenuDao().insert(
        menu['id'],
        pid,
        parentmenu['lft']+1,
        parentmenu['lft']+2,
        parentmenu['depth']+1,
        menu['name'],
        menu['path'],
        menu['icon'],
        menu['hideInMenu'])

    # 父节点 right + 2
    AuthMenuDao().update_rgt(pid, parentmenu['rgt']+2)
    return


"""
作为最后一个 child 被插入
root-lft  parent-lft parent-rgt                  root-rgt
|               |--parent--|--menu--|               |
|               |--parent------------|               |
|---------------|----------|---------|---------------|
"""
def insert_menu_as_last_child(pid, menu):
    parentmenu = AuthMenuDao().select(pid)

    # 父节点之后的节点，都需要 +1
    AuthMenuDao().increase_rgt(parentmenu['rgt'])
    AuthMenuDao().increase_lft(parentmenu['rgt'])

    # 新增加的节点，应放在最后一个
    AuthMenuDao().insert(
        menu['id'],
        pid,
        parentmenu['rgt'],
        parentmenu['rgt']+1,
        parentmenu['depth']+1,
        menu['name'],
        menu['path'],
        menu['icon'],
        menu['hideInMenu'])

    # 父节点 right + 2
    AuthMenuDao().update_rgt(pid, parentmenu['rgt']+2)
    return


"""
作为前一个兄弟被插入
root-lft            brother-lft brother-rgt        root-rgt
|                |--menu--|--brother--|               |
|----------------|---------|-----------|---------------|
"""
def insert_menu_before_brother(brotherId, menu):
    brothermenu = AuthMenuDao().select(brotherId)

    # 父节点之后的节点，都需要 +1
    AuthMenuDao().increase_rgt(brothermenu['lft'])
    AuthMenuDao().increase_lft(brothermenu['lft']-1)
    logging.info(menu)
    logging.info(brothermenu)
    # 新增加的节点，应放在前面
    AuthMenuDao().insert(
        menu['id'],
        brothermenu['pid'],
        brothermenu['lft'],
        brothermenu['lft']+1,
        brothermenu['depth'],
        menu['name'],
        menu['path'],
        menu['icon'],
        menu['hideInMenu'])
    return


"""
作为后一个兄弟被插入
root-lft  brother-lft brother-rgt                  root-rgt
|                |--brother--|--menu--|               |
|----------------|-----------|---------|---------------|
"""
def insert_menu_after_brother(brotherId, menu):
    brothermenu = AuthMenuDao().select(brotherId)

    # 兄弟节点之后的节点，都需要 +1
    AuthMenuDao().increase_rgt(brothermenu['rgt'])
    AuthMenuDao().increase_lft(brothermenu['rgt'])

    # 新增加的节点，应放在后面
    AuthMenuDao().insert(
        menu['id'],
        brothermenu['pid'],
        brothermenu['rgt']+1,
        brothermenu['rgt']+2,
        brothermenu['depth'],
        menu['name'],
        menu['path'],
        menu['icon'],
        menu['hideInMenu'])
    return


"""
删除menu以及其子节点
root-lft    lft       rgt       root-rgt
|            |--menu--|               |
|------------|---------|---------------|
"""
def delete_menu_and_children(menuId):
    menu = AuthMenuDao().select(menuId)
    if menu:
        # 删除自己以及所有子节点
        AuthMenuDao().delete_by_lft_rgt(menu['lft'], menu['rgt'])
        delta = menu['rgt'] - menu['lft'] + 1
        AuthMenuDao().decrease_lft_num(menu['lft'], delta)
        AuthMenuDao().decrease_rgt_num(menu['rgt'], delta)
    return


# 遍历列表结构为树的数据为树状结构
def make_menu_tree(data, root, root_field, node_field):
    """
    解析list数据为树结构
    :param data:  被解析的数据
    :param root: 根节点值
    :param root_field: 根节点字段
    :param node_field: 节点字段
    :return: list
    """
    l = []
    expandedKeys = []
    for i in data:
        if i.get(root_field) == root:
            i['key'] = i['id']
            l.append(i)
            expandedKeys.append(i['id'])
    for i in data:
        node = i.get(node_field)
        children = []
        for j in data:
            parent = j.get(root_field)
            if node == parent:
                j['key'] = j['id']
                children.append(j)
        if len(children) > 0:
            i['children'] = children
            expandedKeys.append(i['id'])
    return {"tree":l, "expandedKeys":expandedKeys}
