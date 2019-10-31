#!/usr/bin/env python

# encoding: utf-8

'''

@author: JOJ

@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.

@contact: zhouguanjie@qq.com

@software: JOJ

@file: url.py

@time: 2019-09-09 15:29

@desc:



'''

from django.conf.urls import re_path
from blog import views

urlpatterns = [
    re_path(r'backend/add_article/',views.add_article),
    re_path(r'up_down/', views.up_down),  # home(request, username)
    re_path(r'comment/', views.comment),  # home(request, username)
    re_path(r'comment_tree/(\d+)/', views.comment_tree),  # home(request, username)
    re_path(r'(\w+)/article/(\d+)/$', views.article_detail),  # 文章详情  article_detail(request, xiaohei, 1)

    re_path(r'(\w+)', views.home),  # home(request, username)

]
