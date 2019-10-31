"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from blog import views
from django.conf import settings
from django.views.static import serve
from django.conf.urls import  include
from blog import  urls as blog_urls

urlpatterns = [
    path('upload/', views.upload),
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('check_code/', views.check_code),
    path('index/', views.index),
    path('logout/', views.logout),
    path('register/', views.register),
    re_path(r'^blog/', include(blog_urls)),
    # 校验用户名
    path('check_username_exist/', views.check_username_exist),
    # 校检邮箱
    path('check_email_exist/', views.check_email_exist),
    # midea相关路由设置,设置后图片存储到media目录中去
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
]
