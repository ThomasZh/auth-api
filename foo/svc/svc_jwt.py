#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2022 cyber-life.cn
# thomas@cyber-life.cn

import logging
import sys
import os
import requests
from bs4 import BeautifulSoup
import re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from global_const import *
from comm import *

def main():
    # 设置headers，即加密算法的配置
    salt = "asgfdgerher"
    # 随机的salt密钥，只有token生成者（同时也是校验者）自己能有，用于校验生成的token是否合法
    # 设置超时时间：当前时间的100s以后超时
    payload = {
        "id": "800be36b639211ebb61b821700fd42c0",
        "nickname": "admin",
        "exp": int(time.time() + 1000)
    }
    # 配置主体信息，一般是登录成功的用户之类的，因为jwt的主体信息很容易被解码，所以不要放敏感信息
    # 当然也可以将敏感信息加密后再放进payload
    token = jwt_encode(salt, payload)
    # 生成token
    print(token)

    info = jwt_decode(salt, token)
    # 解码token，第二个参数用于校验
    # 第三个参数代表是否校验，如果设置为False，那么只要有token，就能够对其进行解码
    print(info)

    time.sleep(2)
    # 等待2s后再次验证token，因超时将导致验证失败
    try:
        info = jwt_decode(salt, token)
        print(info)
    except Exception as e:
        print(repr(e))

main();
