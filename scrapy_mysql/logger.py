#encoding:utf8
#auth: mavarick
#date: {DATETIME}

import logging

sm_log = logging.getLogger("scrapy_mysql")
sm_log.setLevel(logging.INFO)
sm_log.propagate = True
