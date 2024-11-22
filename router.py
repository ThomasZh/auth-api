#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2018 cyber-life.cn
# thomas@cyber-life.cn
# @2018/05/3

import sys
import os
import tornado.web

from foo import comm
from foo import base_handler
from foo.api import auth_login
from foo.api import auth_account
from foo.api import auth_role
from foo.api import auth_menu
from foo.api import auth_policy
from foo.api import auth_permission
from foo.api import auth_group
from foo.api import sys_log
from foo.api import sys_file
from foo.api import sys_profile
from foo.api import sys_invite
from foo.api import sys_tree
from foo.api import sys_dictionary
from foo.api import sys_notices
from foo.api import sys_contact_us
from foo.api import sys_subscribe


def map():

    config = [
        # 用户登录
        (r'/api/auth/v5/login', getattr(auth_login, 'AuthLoginXHR')),
        # 登出（删除access_token）
        (r'/api/auth/v5/logout', getattr(auth_login, 'AuthLogoutXHR')),
        # 发送注册验证码
        (r'/api/auth/v5/signup/verify-code', getattr(auth_login, 'AuthSignupVerifyCodeXHR')),
        # 注册
        (r'/api/auth/v5/signup', getattr(auth_login, 'AuthSignupXHR')),
        # 发送忘记密码验证码
        (r'/api/auth/v5/lostpwd/verify-code', getattr(auth_login, 'AuthLostpwdVerifyCodeXHR')),
        # 忘记密码
        (r'/api/auth/v5/lostpwd', getattr(auth_login, 'AuthLostPwdXHR')),
        # 修改密码
        (r'/api/auth/v5/change-pwd', getattr(auth_login, 'AuthChangePwdXHR')),

        # 系统内部使用，校验是否有权限调用此 http 请求
        (r'/api/auth/v5/assert/permission', getattr(auth_permission, 'AuthAssertPermissionXHR')),

        # 添加角色
        # 修改角色
        (r'/api/auth/v5/roles', getattr(auth_role, 'AuthRolesXHR')),
        # 使用过滤条件查询角色列表
        (r'/api/auth/v5/roles/filter', getattr(auth_role, 'AuthRolesFilterXHR')),
        (r'/api/auth/v5/roles/([A-Za-z0-9]+)/lock', getattr(auth_role, 'AuthRoleLockXHR')),
        (r'/api/auth/v5/roles/([A-Za-z0-9]+)/unlock', getattr(auth_role, 'AuthRoleUnlockXHR')),
        # 删除角色
        (r'/api/auth/v5/roles/([A-Za-z0-9]+)', getattr(auth_role, 'AuthRoleXHR')),
        # 查询角色的用户列表
        (r'/api/auth/v5/roles/([A-Za-z0-9]+)/accounts',getattr(auth_role, 'AuthRoleAccountsXHR')),
        # 查询角色的用户列表
        (r'/api/auth/v5/roles/([A-Za-z0-9]+)/in-accounts',getattr(auth_role, 'AuthRoleInAccountsXHR')),
        # 查询角色的菜单列表
        (r'/api/auth/v5/roles/([A-Za-z0-9]+)/menus',getattr(auth_role, 'AuthRoleMenusXHR')),
        # 角色绑定菜单
        # 角色解绑菜单
        (r'/api/auth/v5/roles/([A-Za-z0-9]+)/menus/([A-Za-z0-9]+)',getattr(auth_role, 'AuthRoleMenuXHR')),

        # 管理员创建帐号, 默认密码: 123456
        (r'/api/auth/v5/accounts', getattr(auth_account, 'AuthAccountsXHR')),
        # 使用过滤条件查询账号列表
        (r'/api/auth/v5/accounts/filter', getattr(auth_account, 'AuthAccountsFilterXHR')),
        # 查询账号信息
        (r'/api/auth/v5/accounts/([A-Za-z0-9]+)', getattr(auth_account, 'AuthAccountXHR')),
        (r'/api/auth/v5/accounts/([A-Za-z0-9]+)/lock', getattr(auth_account, 'AuthAccountLockXHR')),
        (r'/api/auth/v5/accounts/([A-Za-z0-9]+)/unlock', getattr(auth_account, 'AuthAccountUnlockXHR')),
        # 查询账号的登录列表
        (r'/api/auth/v5/accounts/([A-Za-z0-9]+)/logins',getattr(auth_account, 'AuthAccountLoginsXHR')),
        # 账号绑定角色
        # 账号解绑角色
        (r'/api/auth/v5/accounts/([A-Za-z0-9]+)/roles/([A-Za-z0-9]+)',getattr(auth_account, 'AuthAccountRoleXHR')),
        # 查询账号的角色列表
        (r'/api/auth/v5/accounts/([A-Za-z0-9]+)/roles',getattr(auth_account, 'AuthAccountRolesXHR')),
        # 查询账号的组织列表
        (r'/api/auth/v5/accounts/([A-Za-z0-9]+)/groups',getattr(auth_account, 'AuthAccountGroupsXHR')),
        # 账号绑定组织
        # 账号解绑组织
        (r'/api/auth/v5/accounts/([A-Za-z0-9]+)/groups/([A-Za-z0-9]+)',getattr(auth_account, 'AuthAccountGroupXHR')),

        # 添加策略
        (r'/api/auth/v5/policies', getattr(auth_policy, 'PoliciesXHR')),
        # 使用过滤条件查询策略列表
        (r'/api/auth/v5/policies/filter', getattr(auth_policy, 'PoliciesFilterXHR')),
        # 修改策略
        # 删除策略
        (r'/api/auth/v5/policies/([A-Za-z0-9]+)',getattr(auth_policy, 'PolicyXHR')),

        # 菜单列表
        # 添加菜单
        # 修改菜单
        (r'/api/auth/v5/menus', getattr(auth_menu, 'AuthMenusXHR')),
        # 查询我的菜单
        (r'/api/auth/v5/menus/mine', getattr(auth_menu, 'AuthMenusMineXHR')),
        # 删除菜单
        (r'/api/auth/v5/menus/([A-Za-z0-9]+)', getattr(auth_menu, 'AuthMenuXHR')),
        # 查询菜单
        (r'/api/auth/v5/menus/([A-Za-z0-9]+)/tree', getattr(auth_menu, 'AuthMenusTreeXHR')),
        # 查询菜单
        (r'/api/auth/v5/menus/([A-Za-z0-9]+)/table', getattr(auth_menu, 'AuthMenusTableXHR')),
        # 查询菜单
        (r'/api/auth/v5/menus/([A-Za-z0-9]+)/move', getattr(auth_menu, 'AuthMenusMoveXHR')),

        # 添加组织
        (r'/api/auth/v5/groups', getattr(auth_group, 'AuthGroupsXHR')),
        # 查询组织树
        (r'/api/auth/v5/groups/([A-Za-z0-9]+)/tree', getattr(auth_group, 'AuthGroupTreeXHR')),
        # 查询组织表
        (r'/api/auth/v5/groups/([A-Za-z0-9]+)/table', getattr(auth_group, 'AuthGroupTableXHR')),
        # 删除组织
        (r'/api/auth/v5/groups/([A-Za-z0-9]+)', getattr(auth_group, 'AuthGroupXHR')),
        # 查询组织的用户列表
        (r'/api/auth/v5/groups/([A-Za-z0-9]+)/accounts',getattr(auth_group, 'AuthGroupAccountsXHR')),
        # 查询组织的用户列表
        (r'/api/auth/v5/groups/([A-Za-z0-9]+)/in-accounts',getattr(auth_group, 'AuthGroupInAccountsXHR')),
        # 移动组织以及子节点
        (r'/api/auth/v5/groups/([A-Za-z0-9]+)/move',getattr(auth_group, 'AuthGroupMoveXHR')),
        # 查询组织的用户列表
        (r'/api/auth/v5/groups/([A-Za-z0-9]+)/accounts/tree',getattr(auth_group, 'AuthGroupsAccountsTreeXHR')),

        # 修改自己的profile信息
        # 查询自己的profile信息
        (r'/api/sys/profiles/mine', getattr(sys_profile, 'SysMyProfileXHR')),
        # 查询某账号的profile信息
        (r'/api/sys/profiles/([A-Za-z0-9]+)', getattr(sys_profile, 'SysProfileXHR')),

        # 系统内部使用，用户操作写入系统日志
        (r'/api/sys/logs', getattr(sys_log, 'SysLogsXHR')),
        # 按照条件查询系统日志
        (r'/api/sys/logs/filter', getattr(sys_log, 'SysLogsFilterXHR')),

        # 查询系统树根节点列表
        (r'/api/sys/trees/roots-table', getattr(sys_tree, 'SysTreesRootsTableXHR')),
        # 创建根节点
        (r'/api/sys/trees/root', getattr(sys_tree, 'SysTreesRootXHR')),
        # 创建子节点
        (r'/api/sys/trees/node', getattr(sys_tree, 'SysTreesNodeXHR')),
        # 移动子节点
        (r'/api/sys/trees/move', getattr(sys_tree, 'SysTreesMoveXHR')),
        # 删除节点
        (r'/api/sys/trees/([A-Za-z0-9]+)', getattr(sys_tree, 'SysTreeXHR')),
        # 以树型结构查询节点
        (r'/api/sys/trees/([A-Za-z0-9]+)/tree', getattr(sys_tree, 'SysTreeTreeXHR')),
        # 以表型结构查询节点
        (r'/api/sys/trees/([A-Za-z0-9]+)/table', getattr(sys_tree, 'SysTreeTableXHR')),

        # 查询发送给我的系统消息
        (r'/api/sys/notices', getattr(sys_notices, 'SysNoticesXHR')),
        # 查询发送给我的系统消息个数
        (r'/api/sys/notices/count', getattr(sys_notices, 'SysNoticesCountXHR')),
        # 修改系统消息状态
        (r'/api/sys/notices/([A-Za-z0-9]+)/status', getattr(sys_notices, 'SysNoticesStatusXHR')),

        # 上传文件块
        (r'/api/sys/files/upload-blob', getattr(sys_file, 'SysUploadBlobXHR')),
        # cyber服务器直接下载网页链接的文件，不必用户下载网页链接的文件到个人电脑，再上传到cyber服务器
        (r'/api/sys/files/download-weblink', getattr(sys_file, 'SysDownloadWeblinkXHR')),
        # 按照条件查询文件列表
        (r'/api/sys/files/filter', getattr(sys_file, 'SysFilesFilterXHR')),
        # 按照条件查询文件列表
        (r'/api/sys/files/([A-Za-z0-9]+)', getattr(sys_file, 'SysFileXHR')),

        # 创建数据字典
        (r'/api/sys/dictionaries', getattr(sys_dictionary, 'SysDictionarysXHR')),
        # 按照条件查询数据字典列表
        (r'/api/sys/dictionaries/filter', getattr(sys_dictionary, 'SysDictionarysFilterXHR')),
        # 查询数据字典
        # 修改数据字典
        (r'/api/sys/dictionaries/([A-Za-z0-9]+)', getattr(sys_dictionary, 'SysDictionaryXHR')),

        # comm
        (r'.*', getattr(base_handler, 'UrlNotFoundXHR'))
    ]

    return config
