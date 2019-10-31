#!/usr/bin/env python

# encoding: utf-8

'''

@author: JOJ

@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.

@contact: zhouguanjie@qq.com

@software: JOJ

@file: orm.py

@time: 2019-09-06 9:47

@desc:

'''

import  os

if __name__=='__main__':

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BBS.settings")

    import django

    django.setup()

    from blog import models

    # 基于对象的查询 SQL: 子查询
    # a1=models.Article.objects.first()
    # print(a1)
    # print(a1.user.avatar,type(a1.user))
    # # 基于QuerySet查询, SQL: join连表查询
    # a2 = models.Article.objects.filter(pk=1)
    # print(a2.values("user__avatar"))
    # 查询对应得评论
    # print(models.Article.objects.first().comment_set.all().count())

    #查询某个分类对应的文章
    from django.db.models import Count
    user=models.UserInfo.objects.filter(username='test').first()
    # print(user)
    blog=user.blog
    # print(blog)
    # ret=models.Category.objects.filter(blog=blog)
    # for i in ret:
    #     print(i.title,i.article_set.all().count())
    # ret=models.Category.objects.filter(blog=blog).annotate(c=Count('article')).values('title','c')
    # print(ret)
    # 基于queryset查询不用加set
    # ret=models.Category.objects.filter(blog=blog).values('article__title')
    # print(ret)
    ret=models.Article.objects.filter(user=user).extra(select={"archive_ym": "date_format(create_time,'%%Y-%%m')"}).values("archive_ym").annotate(c=Count('nid')).values('archive_ym','c')
    print(ret)