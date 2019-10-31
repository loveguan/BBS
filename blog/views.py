from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from utils import Check_Code
import io
from django.contrib import auth
from . import forms, models
from django.db.models import Count


# Create your views here.

# login

def login(request):
    if request.method == "POST":
        ret = {'status': 0, 'msg': ''}
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        valid_code = request.POST.get('valid_code')
        # 获取带的url
        next = request.POST.get('next')
        if not next:
            next = '/index/'
        print(next)
        print(request.session.get("valid_code", ""))
        if valid_code and valid_code.upper() == request.session.get("valid_code", "").upper():
            user = auth.authenticate(username=username, password=pwd)
            if user:
                auth.login(request, user)
                from django.contrib.sessions.backends.db import SessionStore
                print(request.session.keys())
                print(request.session.values())
                print(request.session.items())
                # 转向访问的url
                ret['msg'] = next
            else:
                ret['status'] = 1
                ret['msg'] = '用户名或者密码错误！！！'
        else:
            ret['status'] = 1
            ret['msg'] = '验证码错误！！！'
        return JsonResponse(ret)
    return render(request, 'login.html')


# logout注销登录
def logout(request):
    print('logout')
    auth.logout(request)
    return redirect('/login/')


# 验证码

def check_code(req):
    """
       获取验证码
       :param request:
       :return:
       """
    stream = io.BytesIO()
    # 创建随机字符 code
    # 创建一张图片格式的字符串，将随机字符串写到图片上
    img, code = Check_Code.create_validate_code()
    img.save(stream, "PNG")
    # 将字符串形式的验证码放在Session中
    req.session["valid_code"] = code
    print('#' * 20)
    print(code)
    return HttpResponse(stream.getvalue())


# index

def index(request):
    article_list = models.Article.objects.all()
    return render(request, 'index.html', {"article_list": article_list})


def register(request):
    if request.method == "POST":
        print('111111')
        ret = {'status': 0, 'msg': ''}
        form_obj = forms.RegForm(request.POST)
        print(request.POST)
        if form_obj.is_valid():
            # 数据校检后再数据库建立新的用户
            form_obj.cleaned_data.pop('re_password')
            #         获取文件
            avatar_img = request.FILES.get('avatar')
            models.UserInfo.objects.create_user(**form_obj.cleaned_data, avatar=avatar_img)
            ret['msg'] = '/login/'
            return JsonResponse(ret)
        else:
            print(form_obj.errors)
            ret['status'] = 1
            ret['msg'] = form_obj.errors
            print(ret)
            print('*' * 200)
            return JsonResponse(ret)
    form_obj = forms.RegForm()
    return render(request, 'register.html', {'form_obj': form_obj})


# 校验用户名是否已经注册
def check_username_exist(request):
    ret = {'status': 0, 'msg': ''}
    user_name = request.GET.get("username")
    is_exist = models.UserInfo.objects.filter(username=user_name)
    if is_exist:
        ret['status'] = 1
        ret['msg'] = '用户已经存在'
    return JsonResponse(ret)


# 校验邮箱是否已经注册
def check_email_exist(request):
    ret = {'status': 0, 'msg': ''}
    email = request.GET.get("email")
    is_exist = models.UserInfo.objects.filter(email=email)
    if is_exist:
        ret['status'] = 1
        ret['msg'] = '邮箱已经存在！！'
    return JsonResponse(ret)


# 定义主页

def home(request, username):
    # 获取用户对象
    user = models.UserInfo.objects.filter(username=username).first()

    if not user:
        return HttpResponse('404')
    # 用户对应的blog
    blog = user.blog
    # 获取自己的文章列表
    article_list = models.Article.objects.filter(user=user)
    print(article_list)
    # 获取分类列表
    category_list = models.Category.objects.filter(blog=blog).annotate(c=Count('article')).values("title", "c")
    print(category_list)
    # 获取标签列表
    tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count('article')).values("title", "c")
    print(tag_list)
    # 按照日期归档
    archive_list = models.Article.objects.filter(user=user).extra(
        select={"archive_ym": "date_format(create_time,'%%Y-%%m')"}
    ).values("archive_ym").annotate(c=Count("nid")).values("archive_ym", "c")
    print(article_list)
    return render(request, 'home.html',
                  {"username": username, "article_list": article_list, "blog": blog, 'category_list': category_list,
                   'tag_list': tag_list,
                   'archive_list': archive_list})


# 文章详细列表
def article_detail(request, username, pk):
    '''

    :param request:
    :param username: 访问的blog的用户名
    :param pk:  主键id
    :return:
    '''
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("404")
    blog = user.blog
    # 找出当前的文章
    article_obj = models.Article.objects.filter(pk=pk).first()
    # 评论表
    comment_list = models.Comment.objects.filter(article_id=pk)
    return render(request, 'article_detail.html', {
        'username': username,
        'article': article_obj,
        'blog': blog,
        'comment_list': comment_list
    })


import json
from django.db.models import F


def up_down(request):
    print(request.POST)
    article_id = request.POST.get('article_id')
    is_up = json.loads(request.POST.get('is_up'))
    user = request.user
    response = {'state': True}
    print('is_up', is_up)

    try:
        models.ArticleUpDown.objects.create(user=user, article_id=article_id, is_up=is_up)
        if is_up:
            models.Article.objects.filter(pk=article_id).update(up_count=F('up_count') + 1)
        else:
            models.Article.objects.filter(pk=article_id).update(down_count=F('down_count') + 1)

    except Exception as e:
        # 如果记录已经存在，会报异常，这里要注意的是在model设置了联合唯一
        response['state'] = False
        response['first_action'] = models.ArticleUpDown.objects.filter(user=user, article_id=article_id).first().is_up

    # return HttpResponse(json.dumps('ok'))
    return JsonResponse(response)


# comment
def comment(request):
    print(request.POST)
    pid = request.POST.get('pid')
    article_id = request.POST.get('article_id')
    content = request.POST.get('content')
    user_pk = request.user.pk
    response = {}
    if not pid:
        comment_obj = models.Comment.objects.create(article_id=article_id, user_id=user_pk, content=content)
    else:
        comment_obj = models.Comment.objects.create(article_id=article_id, user_id=user_pk, content=content,
                                                    parent_comment_id=pid)

    response['create_time'] = comment_obj.create_time.strftime("%Y-%m-%d")
    response['content'] = comment_obj.content
    response['username'] = comment_obj.user.username
    # return HttpResponse(json.dumps('ok'))
    return JsonResponse(response)


# 评论树
def comment_tree(request, article_id):
    ret = list(models.Comment.objects.filter(article_id=article_id).values("pk", "content", 'parent_comment_id'))
    print(ret)
    return JsonResponse(ret, safe=False)


def add_article(request):
    if request.method == "POST":
        print(request.POST)
        title = request.POST.get('title')
        article_content = request.POST.get('article_content')
        user = request.user
        print(user)
        # 将html标签去掉，并截取字符串
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(article_content, "html.parser")
        desc = bs.text[0:150] + "..."
        #     过滤非法标签
        for tag in bs.find_all():
            print(tag.name)
            if tag.name in ["script", "link"]:
                tag.decompose()

        article_obj = models.Article.objects.create(user=user, title=title, desc=desc)
        models.ArticleDetail.objects.create(content=str(bs), article=article_obj)
        return HttpResponse('添加成功')
    return render(request, "add_article.html")


from BBS import settings
import os, json


# 文件上传
def upload(request):
    print(request.FILES)
    obj = request.FILES.get("upload_img")
    print('name', obj.name)

    path = os.path.join(settings.MEDIA_ROOT, "add_article_img", obj.name)
    with open(path, 'wb') as f:
        for line in obj:
            f.write(line)
    res = {
        "error": 0,
        "url": "/media/add_article_img/" + obj.name
    }
    return HttpResponse(json.dumps(res))
