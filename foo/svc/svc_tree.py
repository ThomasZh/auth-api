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
from foo.dao.sys_tree_dao import *



"""
作为第一个 child 被插入
root-lft            parent-lft parent-rgt        root-rgt
|                |--task--|--parent--|               |
|                |-----------parent--|               |
|----------------|--------|----------|---------------|
"""
def insert_node_as_first_child(pid, node):
    parentNode = SysTreeDao().select(pid)
    rootid = node['rootid']

    # 父节点之后的节点，都需要 +1
    SysTreeDao().increase_rgt(rootid, parentNode['lft'])
    SysTreeDao().increase_lft(rootid, parentNode['lft'])

    # 新增加的节点，应放在第一个
    SysTreeDao().insert(
        node['id'],
        pid,
        rootid,
        node['title'],
        node['description'],
        parentNode['lft']+1,
        parentNode['lft']+2,
        parentNode['depth']+1)

    # 父节点 right + 2
    SysTreeDao().update_rgt(pid, parentNode['rgt']+2)
    return


"""
作为最后一个 child 被插入
root-lft  parent-lft parent-rgt                  root-rgt
|               |--parent--|--group--|               |
|               |--parent------------|               |
|---------------|----------|---------|---------------|
"""
def insert_node_as_last_child(pid, node):
    parentNode = SysTreeDao().select(pid)
    rootid = parentNode['rootid']

    # 父节点之后的节点，都需要 +1
    SysTreeDao().increase_rgt(rootid, parentNode['rgt'])
    SysTreeDao().increase_lft(rootid, parentNode['rgt'])

    # 新增加的节点，应放在最后一个
    SysTreeDao().insert(
        node['id'],
        pid,
        rootid,
        node['title'],
        node['description'],
        parentNode['rgt'],
        parentNode['rgt']+1,
        parentNode['depth']+1)

    # 父节点 right + 2
    SysTreeDao().update_rgt(pid, parentNode['rgt']+2)
    return


"""
作为前一个兄弟被插入
root-lft           brother-lft brother-rgt        root-rgt
|                |--task--|--brother--|               |
|----------------|--------|-----------|---------------|
"""
def insert_node_before_brother(brotherId, node):
    brotherNode = SysTreeDao().select(brotherId)
    rootid = brotherNode['rootid']

    # 父节点之后的节点，都需要 +1
    SysTreeDao().increase_rgt(rootid, brotherNode['lft'])
    SysTreeDao().increase_lft(rootid, brotherNode['lft']-1)

    # 新增加的节点，应放在前面
    SysTreeDao().insert(
        node['id'],
        brotherNode['pid'],
        rootid,
        node['title'],
        node['description'],
        brotherNode['lft'],
        brotherNode['lft']+1,
        brotherNode['depth'])
    return


"""
作为后一个兄弟被插入
root-lft  brother-lft brother-rgt                 root-rgt
|                |--brother--|--task--|               |
|----------------|-----------|--------|---------------|
"""
def insert_node_after_brother(brotherId, node):
    brotherNode = SysTreeDao().select(brotherId)
    rootid = brotherNode['rootid']

    # 兄弟节点之后的节点，都需要 +1
    SysTreeDao().increase_rgt(rootid, brotherNode['rgt'])
    SysTreeDao().increase_lft(rootid, brotherNode['rgt'])

    # 新增加的节点，应放在后面
    SysTreeDao().insert(
        node['id'],
        brotherNode['pid'],
        rootid,
        node['title'],
        node['description'],
        brotherNode['rgt']+1,
        brotherNode['rgt']+2,
        brotherNode['depth'])
    return


"""
删除任务以及其子任务
root-lft    lft      rgt       root-rgt
|            |--task--|               |
|------------|--------|---------------|
"""
def delete_node_and_children(nodeId):
    node = SysTreeDao().select(nodeId)
    rootid = node['rootid']
    if node:
        # 删除自己以及所有子任务
        SysTreeDao().delete_by_lft_rgt(rootid, node['lft'], node['rgt'])
        delta = node['rgt'] - node['lft'] + 1
        SysTreeDao().decrease_lft_num(rootid, node['lft'], delta)
        SysTreeDao().decrease_rgt_num(rootid, node['rgt'], delta)
    return


# 遍历列表结构为树的数据为树状结构
def make_tree(data, root, root_field, node_field):
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
