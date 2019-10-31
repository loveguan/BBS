#!/usr/bin/env python

# encoding: utf-8

'''

@author: JOJ

@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.

@contact: zhouguanjie@qq.com

@software: JOJ

@file: middleware.py.py

@time: 2019-08-27 10:07

@desc:自定义中间件,登录认证的中间件！！！

'''

from django.utils.deprecation import MiddlewareMixin


class AuthMD(MiddlewareMixin):
    white_list = ['/login/', '/check_code/','/register/','/index/','/admin/login/']  # 白名单
    balck_list = ['/black/', ]  # 黑名单

    def process_request(self, request):
        from django.shortcuts import redirect, HttpResponse

        next_url = request.path_info
        print(request.path_info, request.get_full_path())
        # if next_url in self.white_list or request.user:
        if next_url in self.white_list or request.session.get("_auth_user_id"):
            return
        elif next_url in self.balck_list:
            return HttpResponse('This is an illegal URL')
        else:
            return redirect("/login/?next={}".format(next_url))
