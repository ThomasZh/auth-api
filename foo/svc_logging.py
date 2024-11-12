# coding=utf-8
import os
import os.path
import logging
from logging.handlers import TimedRotatingFileHandler
from svc_config import GlobalConfig


# Init logging
def init_logging(svc_name, port):
    log_file = svc_name + "_" + str(port) + ".log"

    # logging初始化工作
    # logging.basicConfig()

    # logger的初始化工作
    logger = logging.getLogger()
    logger.setLevel(GlobalConfig().log_level)

    # 添加TimedRotatingFileHandler到logger
    # 定义一个1天换一次log文件的handler
    fh = logging.handlers.TimedRotatingFileHandler(
        os.path.join(GlobalConfig().log_path, log_file), when='D', backupCount=10)
    # fh = logging.FileHandler(os.path.join(GlobalConfig().log_path, log_file))
    # 设置后缀名称，跟strftime的格式一样
    fh.suffix = "%Y%m%d"

    # ###########This set the logging level that show on the screen#############
    sh = logging.StreamHandler()
    sh.setLevel(GlobalConfig().log_level)

    formatter = logging.Formatter('%(asctime)s --%(filename)s[%(lineno)d] %(levelname)s: %(message)s')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)

    logger.addHandler(fh)
    # logger.addHandler(sh)
    logging.info("|Setup logging level|%s", logging.getLevelName(logger.getEffectiveLevel()))
