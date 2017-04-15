#! /usr/bin/env python
# coding=utf-8

"""
生成请求API时必须的sign

"""

import time
import datetime
from winlesson_upload.settings import REQUEST_KEY
import hashlib


def generate_sign(timestamp=int(time.time())):
    m = hashlib.md5()
    m.update(str(timestamp) + REQUEST_KEY)
    return m.hexdigest().upper()


if __name__ == "__main__":
    generate_sign()
