#! /usr/bin/env python
# coding: utf-8


from django.shortcuts import HttpResponse
import logging
import os
from django.conf import settings
from utils.utils import json_encode
from utils.utils import Encryption
from django.views.decorators.csrf import csrf_exempt
import json

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)

# Create your views here.
ALLOW_IMG_EXT = (".png", ".jpg", ".jpeg")
ALLOW_FILE_EXT = (".txt", ".doc", ".docx", ".pdf", ".xls", ".xlsx")


@csrf_exempt
def upload_file(request):
    logger.info("request: %s" % request)
    # if request.method == "GET":
    #     return HttpResponse("You need to use post method!")
    # if request.method == "POST":
    ret = {}
    try:
        ufile = request.FILES["files"]
    except Exception as e:
        logger.error("Errors: %s" % str(e), exc_info=True)
        ret.update({
            "code": 400,
            "msg": u"参数错误",
            "result": ""
        })
        return
    else:
        try:
            fpath = ""
            if ufile:
                fname = ufile.name
                save_file(ufile,
                          settings.SOURCE_PATH + fname.encode("utf-8"))
                _name, _ext = os.path.splitext(fname)
                logger.info(
                    "Receive file filename:%s, fileext: %s" % (_name, _ext))
                if _ext not in ALLOW_FILE_EXT + ALLOW_IMG_EXT:
                    ret.update({
                        "code": "0",
                        "msg": u"上传不支持的文件格式",
                        "result": "",
                    })
                    return

                cname = Encryption(_name).encode() + _ext
                fpath = settings.FILE_PATH + cname
                if _ext in ALLOW_IMG_EXT:
                    fpath = settings.IMG_PATH + cname
                save_file(ufile, fpath)
            ret.update({
                "code": 200,
                "msg": u"请求成功",
                "result": {
                    "filePath": settings.API_HOST + fpath.replace(
                        "/data/static", ""),
                }
            })
        except Exception as e:
            print str(e)
            logger.error("Errors: %s" % str(e), exc_info=True)
            ret.update({
                "code": 500,
                "msg": u"服务器处理错误",
            })
    finally:
        return HttpResponse(json_encode(ret))


def save_file(f, fpath):
    if not os.path.exists(fpath):
        fp = open(fpath, "wb+")
        for chunk in f.chunks():
            fp.write(chunk)
