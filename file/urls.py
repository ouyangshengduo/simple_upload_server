#! /usr/bin/env python
# coding: utf-8


from django.conf.urls import url
from .views import upload_file
from utils.utils import Encryption


app_name = "file"
urlpatterns = [
    url(r"^upload/$", upload_file, name="upload_file"),
]
