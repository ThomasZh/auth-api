#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2023 cyber-life.cn
# thomas@cyber-life.cn

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
import logging
from foo.toolkit.cy_json import CyJson
from base_handler import *
from global_const import *
from comm import *

from tornado import gen
from concurrent.futures import ProcessPoolExecutor

from foo.svc_config import GlobalConfig
from foo.dao.sys_file_blob_dao import *
from foo.dao.sys_file_dao import *
from foo.dao.redis_queue import RedisQueue
from foo.svc.crypt_base64 import base64_to_str


# /api/sys/files/upload-blob
class SysUploadBlobXHR(AuthorizationHandler):
    # 并发进程数
    # executor = ProcessPoolExecutor(max_workers=3)

    @tornado.web.authenticated  # if no session, redirect to login page
    # @tornado.gen.coroutine
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            blobCurrNum = int(payload["blobCurrNum"])
            blobTotalNum = int(payload["blobTotalNum"])
            size = int(payload["size"])
            filename = payload["filename"]
            filetype = payload["filetype"] # image,video,file,audio
            fileBlob = base64_to_str(payload["data"])
            # 业务ID，业务逻辑配对使用，由业务自己定义和使用，后台只负责传输
            bizid = ""
            if "bizid" in payload:
                bizid = payload['bizid']
        except Exception as e:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        operId = self.get_account_id()

        # 获取后缀（文件扩展名）
        ext = os.path.splitext(filename)[-1]
        fileId = name_to_uuid(operId + bizid) # 使用 bizid 生成 fileId
        if not bizid:
            bizid = fileId # 客户端没有传输 bizid，系统则指定一个

        # 增加了一层路径，防止一个目录下存储文件过多，访问速度变慢
        # 未上传云存储成功前，使用本地URL访问此文件
        localUrl = os.path.join(GlobalConfig().storage_static_domain, filetype, fileId[0], fileId+ext)
        # 修改公网地址
        cloudUrl = os.path.join(GlobalConfig().storage_static_domain, filetype, fileId[0], fileId+ext)

        if blobCurrNum == 0: # 可能是第一次上传，也可能是重新传输同名文件
            # SysFileBlobDao().delete_exclude(fileId, bizid) # 删除不包含 bizid 的记录
            SysFileBlobDao().delete(fileId) # 删除 fileId 的记录

            fileInfo = SysFileDao().select(fileId)
            if fileInfo: # 如果文件已经存在
                SysFileDao().update(fileId,localUrl,filetype,filename,blobTotalNum,size,ext,operId,bizid)
            else:
                SysFileDao().insert(fileId,localUrl,filetype,filename,blobTotalNum,size,ext,operId,bizid)
        SysFileBlobDao().insert(fileId,bizid,blobCurrNum,blobTotalNum,operId) #计数器+1

        # 本地文件的存储路径
        tmp_filepath = os.path.join(GlobalConfig().storage_tmp_path, fileId[0], fileId+ext)
        # 有些文件需要已二进制的形式存储，实际中可以更改
        # 文件每块单独存储，处理完毕时合并成一个，上传到云存储
        with open(tmp_filepath + "-" + str(blobCurrNum), 'ab+') as f:
            f.write(fileBlob)

        completedNum = SysFileBlobDao().count(fileId,bizid)
        # 所有块传输完成
        if completedNum == blobTotalNum:
            if filetype == "template":
                cmd = "UploadTemplateFile"
            elif filetype == "testdata":
                cmd = "UploadTestdataFile"
            elif filetype == "image":
                cmd = "UploadImageFile"
            else:
                cmd = "UploadFile"
            json = JSON.dumps({
                "cmd": cmd,
                "fileId": fileId,
                "filetype": filetype,
                "operId": operId,
            })

            # 向消息队列发送上传文件到云存储的命令
            # 消息队列的另一头完成合并所有块的工作
            rq = RedisQueue('cmd')  # 新建队列名为cmd
            rq.put(json)

            # 回调函数，直到文件上传以及后续处理完毕
            # resp = self.on_after_uploaded()

            # 所有块传输完成
            response = {
                "errCode":200,
                "errMsg":"Created",
                "url":localUrl,
                "cloudUrl": cloudUrl,
                "bizid":bizid,
                "fileId":fileId,
                "filename":filename,
                "completedNum":completedNum,
                "blobTotalNum":blobTotalNum,
            }
            self.write_response(response, logger=True)
            return
        else:
            response = {
                "errCode":201,
                "errMsg":"Success",
                "url":localUrl,
                "bizid":bizid,
                "filename":filename,
                "completedNum":completedNum,
                "blobTotalNum":blobTotalNum
            }
            self.write_response(response, logger=False)
            return


    # 回调函数
    @tornado.web.authenticated  # if no session, redirect to login page
    def on_after_uploaded(self):
        operId = self.get_account_id()
        # 向消息队列发送上传文件到云存储的命令
        # 消息队列的另一头完成合并所有块的工作
        rq = RedisQueue(operId)  # 新建队列名为用户ID
        while 1:
            result = rq.get_wait()
            if result:
                logging.info("|Queue|after_file_uploaded|%r", result)
                if isinstance(result, str):
                    data = JSON.loads(result)
                else:
                    data = JSON.loads(result.decode("utf-8"))
                return data
            time.sleep(1)


# /api/sys/files/download-weblink
class SysDownloadWeblinkXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            url = payload["url"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        operId = DEFAULT_ACCOUNT_ID

        json = JSON.dumps({
            "cmd": "DownloadWeblink",
            "url": url,
            "operId": operId,
        })
        # 向消息队列发送上传文件到云存储的命令
        # 消息队列的另一头完成合并所有块的工作
        rq = RedisQueue('cmd')  # 新建队列名为cmd
        rq.put(json)

        response = {"errCode":201, "errMsg":"Success"}
        self.write_response(response, logger=True)
        return


# /api/sys/files/filter
class SysFilesFilterXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):
        currPage = 1
        pageSize = 20
        orders = []
        searchs = []

        try:
            payload = CyJson.loads(self.request.body)
            if "currPage" in payload:
                currPage = int(payload["currPage"])
                if currPage <= 0:
                    currPage = 1
            if "pageSize" in payload:
                pageSize = int(payload["pageSize"])
                if pageSize < 0:
                    pageSize = 20
            if "orders" in payload:
                orders = payload["orders"]
            if "searchs" in payload:
                searchs = payload["searchs"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        idx = (currPage - 1) * pageSize
        datas = SysFileDao().selectPaginationByFilters(searchs, orders, idx, pageSize)
        for data in datas:
            data['cloudUrl'] = GlobalConfig().storage_cloud_domain + data['localUrl']

        totalNum = SysFileDao().countPaginationByFilters(searchs)
        if totalNum % pageSize == 0:
            totalPage = int(totalNum / pageSize)
        else:
            totalPage = int(totalNum / pageSize) + 1

        response = {
            "errCode": 200,
            "errMsg": "Success",
            "currPage": currPage,
            "pageSize": pageSize,
            "totalNum": totalNum,
            "totalPage": totalPage,
            "datas": datas
        }
        self.write_response(response, logger=False)
        return


# /api/sys/files/{fileId}
class SysFileXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def delete(self, fileId):
        SysFileDao().delete(fileId)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return
