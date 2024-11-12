#!/usr/bin/env python
# _*_ coding: utf-8_*_
import jwt


def jwt_decode(secret_key, jwt_token):
    info = jwt.decode(jwt_token, secret_key, True, algorithm='HS256')
    return info


def jwt_encode(secret_key, payload):
    headers = {"alg": "HS256", "typ": "JWT"}
    jwt_token = jwt.encode(payload=payload, key=secret_key, algorithm='HS256', headers=headers).decode('utf-8')
    return jwt_token
