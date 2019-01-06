# -*- coding: utf-8 -*-
"""
__author__ = 'Gao yue'
__mtime__ = '2018/10/24'
# code is far away from bugs with the god animal protecting
┏┓ ┏┓
┏┛┻━━━┛┻┓
┃ ☃ ┃
┃ ┳┛ ┗┳ ┃
┃ ┻ ┃
┗━┓ ┏━┛
┃ ┗━━━┓
┃ 神兽保佑 ┣┓
┃　永无BUG！ ┏┛
┗┓┓┏━┳┓┏┛
┃┫┫ ┃┫┫
┗┻┛ ┗┻┛
"""
from django.urls import path
from . import views


urlpatterns = [
    path("done_question/", views.done_question, name="done_question"),
    path("logout/", views.logout, name="account_logout"),
    path("register/", views.register, name="account_register"),
    path("login/", views.login, name="account_login"),
    path("index/", views.index, name="index"),
]