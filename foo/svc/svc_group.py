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
from foo.dao.auth_group_dao import *


"""
作为第一个 child 被插入
root-lft             parent-lft parent-rgt        root-rgt
|                |--group--|--parent--|               |
|                |------------parent--|               |
|----------------|---------|----------|---------------|
"""
def insert_group_as_first_child(pid, group):
    parentGroup = AuthGroupDao().select(pid)

    # 父节点之后的节点，都需要 +1
    AuthGroupDao().increase_rgt(parentGroup['lft'])
    AuthGroupDao().increase_lft(parentGroup['lft'])

    # 新增加的节点，应放在第一个
    AuthGroupDao().insert(
        group['id'],
        pid,
        group['title'],
        parentGroup['lft']+1,
        parentGroup['lft']+2,
        parentGroup['depth']+1)

    # 父节点 right + 2
    AuthGroupDao().update_rgt(pid, parentGroup['rgt']+2)
    return


"""
作为最后一个 child 被插入
root-lft  parent-lft parent-rgt                  root-rgt
|               |--parent--|--group--|               |
|               |--parent------------|               |
|---------------|----------|---------|---------------|
"""
def insert_group_as_last_child(pid, group):
    parentGroup = AuthGroupDao().select(pid)

    # 父节点之后的节点，都需要 +1
    AuthGroupDao().increase_rgt(parentGroup['rgt'])
    AuthGroupDao().increase_lft(parentGroup['rgt'])

    # 新增加的节点，应放在最后一个
    AuthGroupDao().insert(
        group['id'],
        pid,
        group['title'],
        parentGroup['rgt'],
        parentGroup['rgt']+1,
        parentGroup['depth']+1)

    # 父节点 right + 2
    AuthGroupDao().update_rgt(pid, parentGroup['rgt']+2)
    return


"""
作为前一个兄弟被插入
root-lft            brother-lft brother-rgt        root-rgt
|                |--group--|--brother--|               |
|----------------|---------|-----------|---------------|
"""
def insert_group_before_brother(brotherId, group):
    brotherGroup = AuthGroupDao().select(brotherId)

    # 父节点之后的节点，都需要 +1
    AuthGroupDao().increase_rgt(brotherGroup['lft'])
    AuthGroupDao().increase_lft(brotherGroup['lft']-1)

    # 新增加的节点，应放在前面
    AuthGroupDao().insert(
        group['id'],
        brotherGroup['pid'],
        group['title'],
        brotherGroup['lft'],
        brotherGroup['lft']+1,
        brotherGroup['depth'])
    return


"""
作为后一个兄弟被插入
root-lft  brother-lft brother-rgt                  root-rgt
|                |--brother--|--group--|               |
|----------------|-----------|---------|---------------|
"""
def insert_group_after_brother(brotherId, group):
    brotherGroup = AuthGroupDao().select(brotherId)

    # 兄弟节点之后的节点，都需要 +1
    AuthGroupDao().increase_rgt(brotherGroup['rgt'])
    AuthGroupDao().increase_lft(brotherGroup['rgt'])

    # 新增加的节点，应放在后面
    AuthGroupDao().insert(
        group['id'],
        brotherGroup['pid'],
        group['title'],
        brotherGroup['rgt']+1,
        brotherGroup['rgt']+2,
        brotherGroup['depth'])
    return


"""
删除group以及其子节点
root-lft    lft       rgt       root-rgt
|            |--group--|               |
|------------|---------|---------------|
"""
def delete_group_and_children(groupId):
    group = AuthGroupDao().select(groupId)
    if group:
        # 删除自己以及所有子节点
        AuthGroupDao().delete_by_lft_rgt(group['lft'], group['rgt'])
        delta = group['rgt'] - group['lft'] + 1
        AuthGroupDao().decrease_lft_num(group['lft'], delta)
        AuthGroupDao().decrease_rgt_num(group['rgt'], delta)
    return
