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
from foo.dao.auth_account_dao import *
from foo.dao.auth_app_secret_dao import *
from foo.dao.auth_policy_dao import *
from foo.dao.auth_account_role_dao import *
from foo.dao.auth_app_role_dao import *


def assert_permission(accountId, path, method):
    account = AuthAccountDao().select(accountId)
    if account:
        if account['status'] != 0:
            response = {"errCode":403, "errMsg":"Forbidden"}
            return response
    else:
        app = AuthAppSecretDao().select(accountId)
        if app:
            if app['status'] != 0:
                response = {"errCode":403, "errMsg":"Forbidden"}
                return response
        else:
            response = {"errCode":403, "errMsg":"Forbidden"}
            return response

    roles = AuthAccountRoleDao().select_roles_pagination(accountId,0,1000) #尽可能多
    if not roles or len(roles) == 0:
        roles = AuthAppRoleDao().select_roles_pagination(accountId,0,1000) #尽可能多
    policies = AuthPolicyDao().select_pagination(0,1000) #尽可能多
    for policy in policies:
        pathFlag = re.match(policy['resPath'], path)
        if pathFlag: #匹配
            if policy['type'] == "account":
                if policy['objId'] == "*" or policy['objId'] == accountId:
                    if policy['action'] == "*" or policy['action'] == method:
                        if policy['access'] == "allow":
                            response = {"errCode":200, "errMsg":"Success"}
                            return response
                        else:
                            response = {"errCode":403, "errMsg":"Forbidden"}
                            return response
            elif policy['type'] == "role":
                if policy['objId'] == "*" or in_roles(policy['objId'], roles):
                    if policy['action'] == "*" or policy['action'] == method:
                        if policy['access'] == "allow":
                            response = {"errCode":200, "errMsg":"Success"}
                            return response
                        else:
                            response = {"errCode":403, "errMsg":"Forbidden"}
                            return response
    response = {"errCode":403, "errMsg":"Forbidden"}
    return response


def in_roles(roleId, roles):
    if roles and len(roles) > 0:
        for role in roles:
            if roleId == role['id']:
                return True
    return False
