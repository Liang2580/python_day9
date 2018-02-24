#!/usr/bin/env python
#_*_coding:utf-8_*_


import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_LEVEL=logging.INFO

LOG_TYPES={
    'system':'system.log'
}
msg_dic = {
    "group1":{    #分组1
        "h1":{"IP":"192.168.57.128", "username":"root", "password":"123456", "port":22},
        "h2":{"IP":"192.168.57.129", "username":"root", "password":"123456", "port":22},
    },
    "group2":{    #分组2
        "h1":{"IP":"192.168.57.129", "username":"root", "password":"123456", "port":22},
        "h2":{"IP":"192.168.57.129", "username":"root", "password":"123456", "port":22},
        "h3":{"IP":"192.168.57.129", "username":"root", "password":"123456", "port":22},
    },
}
