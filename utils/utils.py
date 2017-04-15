#! /usr/bin/env python
# coding=utf-8


import hashlib
import json
import random
import string
import uuid
from datetime import datetime

import qrcode
import requests


# Encryption
class Encryption(object):
    """加密工具类"""

    def __init__(self, to_encode, encode_type='md5'):
        self.encode_type = encode_type

        # uniform type of to_encode
        self.to_encode = str(to_encode)

    def encode(self):
        _crypt = hashlib.new(self.encode_type)
        _crypt.update(self.to_encode)
        return _crypt.hexdigest()


# HttpRequest get and post
class BskRequest(object):
    """Http请求类"""

    def __init__(self, method, url, request=None, headers=None, cookies=None,
                 params=None, files=None):
        """
        :param method: 请求方法目前只支持get、post
        :param url: 请求url
        :param headers: 头部
        :param cookies: cookies
        :param params: get：请求参数；post：请求数据
        :param files: post请求时支持上传文件例：files = {'file': open('report.xls', 'rb')}
        """
        self.method = method
        self.url = url
        self.headers = headers or {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Cache-Control': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/53.0.2785.143 Safari/537.36',
        }
        self.params = params
        self.cookies = cookies
        self.files = files
        self.request = request

    def do_request(self):
        r = requests.Response()
        if self.method.lower() == "get":
            r = requests.get(self.url, params=self.params, headers=self.headers,
                             cookies=self.cookies, verify=False)
            return r.content
        elif self.method.lower() == "post":
            self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
            r = requests.post(url=self.url, data=self.params,
                              headers=self.headers, cookies=self.cookies,
                              files=self.files, verify=False)
            return r.json()


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")


def json_encode(value):
    return json.dumps(value, default=json_serial)


def gen_qrcode(data):
    """生成二维码"""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    return img


def gen_random_string(n=32):
    assert n > 0
    choiceString = string.ascii_lowercase + string.digits

    if n <= 36:
        return "".join(random.sample(choiceString, n))

    # TODO: 待优化
    aList = []
    for i in xrange(n):
        aList.append(choiceString[random.randint(0, len(choiceString) - 1)])
    return "".join(aList)


def gen_uuid():
    return str(uuid.uuid1()).replace("-", "")


def gen_verify_code():
    return "".join(random.sample(string.digits, 4))


def get_primary_key():
    timestr = datetime.now().strftime("%Y%m%d%H%M%S%f") + "0000"
    return timestr


def remove_duplicate(dict_list):
    """字典列表去重"""
    seen = set()
    new_dict_list = []
    for dt in dict_list:
        seen.add(tuple(dt.items()))
    for item in seen:
        new_dict_list.append(dict(item))
    return new_dict_list


if __name__ == "__main__":
    print Encryption(u"winlesson").encode()
    print gen_random_string(100)
    print gen_uuid()
    print gen_verify_code()
    print sorted(remove_duplicate([
        {"a": 1, "b": 2}, {"a": 1, "b": 2}, {"a": 3, "b": 5}
    ]), key=lambda x: (x["a"], x["b"]))
    print get_primary_key()
