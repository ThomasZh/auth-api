#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2018 cyber-life.cn
# thomas@cyber-life.cn
# @20323/05/30

import os.path
import ssl
import signal
import sys
import logging
import tornado.ioloop
from tornado.options import define, options
import tornado.web

from foo.svc_config import GlobalConfig
from foo.svc_logging import init_logging
import router

define("debug", default=True, help="run in debug mode")


def sig_handler(sig, frame):
    logging.debug('|API service|Caught signal|%s', sig)
    logging.warning('|API service|Shutdown')
    sys.exit(0)


def main():
    # check config path from environment first:
    config_from_env = os.environ['FORMAS_AUTH_CFG_PATH']
    # 加载配置信息
    cfg_file = "/opt/formas/conf/auth-api.cfg"
    GlobalConfig().load(config_from_env or cfg_file)

    # 设置日志格式
    init_logging(GlobalConfig().svc_name, GlobalConfig().svc_port)
    logging.info('|API service|Starting......')

    # router_ajax放在列表前面，保证优先获取规则
    app = tornado.web.Application(
        router.map(),
        # __TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__
        cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=False,
        debug=options.debug,
        login_url="/web/home/login",
        # ssl_options={
        #    "certfile": os.path.join(os.path.abspath("."), "bike-forever.com.crt"),
        #    "keyfile": os.path.join(os.path.abspath("."), "bike-forever.com.key"),
        # }
    )
    # tornado.locale.load_gettext_translations(os.path.join(os.path.dirname(__file__), "locale"), "aplan")
    tornado.locale.set_default_locale("en_US")
    tornado.options.parse_command_line()

    ##############set signal handler#######################
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    logging.info('|API service|Started|%s:%d', GlobalConfig().svc_host, GlobalConfig().svc_port)

    port_number = GlobalConfig().svc_port
    print("=== FORMAS AUTH_API SERVER STARTED AT: ", port_number, " ===")
    app.listen(port_number)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
