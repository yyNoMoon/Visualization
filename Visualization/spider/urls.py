# -*- coding: utf-8 -*-
"""
__author__ = 'Gao yue'
__mtime__ = '2018/11/1'
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
    path("spider/", views.index, name="done_question"),
    path('button_callback', views.button_callback),
]