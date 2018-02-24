#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: liang 


import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print(BASE_DIR)

from core import server

if __name__ == '__main__':
    server.run()