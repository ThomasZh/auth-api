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


def svc_get_profile(accountId):
    account = AuthAccountDao().select(accountId)
    return account
