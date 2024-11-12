#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2016-2017 7x24hs.com
# thomas@7x24hs.com

import tornado.web
import logging
import sys
import os
import string
import json as JSON # 启用别名，不会跟方法里的局部变量混淆

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))

from comm import *
from global_const import *
from foo.svc_config import GlobalConfig
from foo.svc.svc_permission import assert_permission
from foo.dao.sys_log_dao import *


def parse_accessToken_from_headers(headers):
    logging.debug("|got Authorization from headers|%s", headers)
    if "Authorization" in headers:
        authorization = headers['Authorization']
        accessToken = authorization.replace('Bearer','')
        accessToken = accessToken.replace(' ', '')
        return accessToken
    else:
        return None


class UrlNotFoundXHR(tornado.web.RequestHandler):
    def get(self, *args):
        response = {"errCode":404, "errMsg":"Not Found This URL"}
        self.set_status(200)
        self.write(response)
        self.finish()
        return

    def post(self, *args):
        response = {"errCode":404, "errMsg":"Not Found This URL"}
        self.set_status(200)
        self.write(response)
        self.finish()
        return

    def put(self, *args):
        response = {"errCode":404, "errMsg":"Not Found This URL"}
        self.set_status(200)
        self.write(response)
        self.finish()
        return

    def delete(self, *args):
        response = {"errCode":404, "errMsg":"Not Found This URL"}
        self.set_status(200)
        self.write(response)
        self.finish()
        return


class BaseHandler(tornado.web.RequestHandler):
    # 在请求处理结束后调用，即在调用HTTP方法后调用。通常该方法用来进行资源清理释放或处理日志等。
    def write_error(self, status_code, **kwargs):
        # super().write_error(status_code, **kwargs)
        exc_cls, exc_instance, trace = kwargs.get("exc_info")
        logging.error("|Service Error|%d|%s|%s|%r",
            status_code,
            self.request.uri,
            self.request.body,
            exc_instance)

        if status_code == 401:
            response = {"errCode":401, "errMsg":"Unauthorized"}
            self.set_status(200)
            self.write(response)
            self.finish()
            return
        elif status_code == 403:
            response = {"errCode":403, "errMsg":"Forbidden"}
            self.set_status(200)
            self.write(response)
            self.finish()
            return
        elif status_code == 404:
            response = {"errCode":404, "errMsg":"Not Found"}
            self.set_status(200)
            self.write(response)
            self.finish()
            return
        else:
            response = {"errCode":500, "errMsg":"Internal Server Error"}
            self.set_status(200)
            self.write(response)
            self.finish()
            return


    # 解决跨域问题
    def set_default_headers(self):
        # 切记Access-Control-Allow-Origin不能设为通配符“*”
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-Type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, PUT, DELETE, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                        'authorization, Authorization, Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')
        self.set_header("Access-Control-Expose-Headers",
                        'authorization, Authorization, Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')


    def get_account_id(self):
        if "Account-Id" in self.request.headers:
            return self.request.headers['Account-Id']
        else:
            sessionTicket = self.get_session_ticket()
            if sessionTicket:
                return sessionTicket['sub']
            else:
                return None


    def get_username(self):
        if "Username" in self.request.headers:
            return self.request.headers['Username']
        else:
            sessionTicket = self.get_session_ticket()
            if sessionTicket:
                return sessionTicket['name']
            else:
                return None


    def get_access_token(self):
        accessToken = parse_accessToken_from_headers(self.request.headers)
        if accessToken:
            return accessToken
        else:
            accessToken = self.get_secure_cookie("accessToken")
            logging.debug("|got accessToken from cookie|%s", accessToken)
            return accessToken


    def get_session_ticket(self):
        accessToken = self.get_access_token()
        logging.debug("|got accessToken|%r", accessToken)
        if not accessToken:
            return None

        try:
            sessionTicket = jwt_decode(GlobalConfig().jwt_secret, accessToken)
            logging.debug("|decode sessionTicket from accessToken|%r", sessionTicket)
            return sessionTicket
        except Exception as e:
            logging.warn("|decode sessionTicket from accessToken|%r", repr(e))
            return None


    # Aspect-oriented programming
    def write_response(self, response, logger):
        self.set_status(200)
        self.write(make_rs(response))
        self.finish()

        db_body = None
        if self.request.path == "/api/sys/files/upload-blob":
            try:
                # 上传文件的结构体内容太大，删除它，再保存日志
                payload = JSON.loads(self.request.body)
                del payload["data"]
                logging_body = JSON.dumps(payload)
            except:
                pass
        elif self.request.path == "/api/cms/articles":
            try:
                # 编辑文章的结构体 content 太大，删除它，再保存日志
                payload = JSON.loads(self.request.body)
                del payload["content"]
                logging_body = JSON.dumps(payload)
                db_body = self.request.body
            except:
                pass
        else:
            logging_body = self.request.body

        # 集中处理日志
        logging.info("|%s|%s|%s|%s|%s|%s|%s|%s|",
            response['errCode'],
            response['errMsg'],
            self.request.method,
            self.request.path,
            self.request.query,
            logging_body,
            self.get_account_id(),
            self.get_username())

        # 集中处理写入数据库日志
        if logger:
            ipAddr = None
            userAgent = None
            # Squid uses X-Forwarded-For, others use X-Real-Ip
            if "X-Forwarded-For" in self.request.headers:
                ipAddr = self.request.headers["X-Forwarded-For"]
                ipAddr = ipAddr.split(',')[-1].strip()
            elif "X-Real-Ip" in self.request.headers:
                ipAddr = self.request.headers["X-Real-Ip"]
            if "User-Agent" in self.request.headers:
                userAgent = self.request.headers["User-Agent"]
            SysLogDao().insert(
                self.get_account_id(),
                self.get_username(),
                self.request.method,
                self.request.path,
                self.request.query,
                db_body if db_body else logging_body,
                response['errCode'],
                response['errMsg'],
                ipAddr,
                userAgent)


    # 响应客户端发送的OPTIONS域检请求
    def options(self, *args):
        self.set_status(204)
        self.finish()
        return


class AuthorizationHandler(BaseHandler):
    # Aspect-oriented programming
    def get_current_user(self):
        # 包头中含有 Account-Id，一定是 api-gateway 发送过来的数据包
        # 获得 accountId，就不必校验 sessionTicket
        if "Account-Id" in self.request.headers:
            return self.request.headers['Account-Id']

        sessionTicket = self.get_session_ticket()
        if sessionTicket:
            _timestamp = current_timestamp()
            if sessionTicket['exp'] > _timestamp:
                response = assert_permission(sessionTicket['sub'], self.request.path, self.request.method)
                if response['errCode'] == 200:
                    return sessionTicket
                else:
                    logging.warn("|AuthInterceptor|%s|%s|%s", response['errCode'], response['errMsg'], self.request.uri)
                    self.set_status(200)
                    self.write(response)
                    self.finish()
                    return None
            else:
                logging.warn("|AuthInterceptor|401|凭证过期|%s", self.request.uri)
                response = {"errCode":401, "errMsg":"凭证过期"}
                self.set_status(200)
                self.write(response)
                self.finish()
                return None
        else:
            logging.warn("|AuthInterceptor|401|没有凭证|%s", self.request.uri)
            response = {"errCode":401, "errMsg":"没有凭证"}
            self.set_status(200)
            self.write(response)
            self.finish()
            return None
