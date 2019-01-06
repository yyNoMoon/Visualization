# -*- coding: utf-8 -*-
"""
__author__ = 'Gao yue'
__mtime__ = '2018/11/27'
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
    path("dataIndex/", views.index, name="index"),
    path("getAllData/", views.getAllProvinceData, name="getAllProvinceData"),
    path("getIndustryIndexData/<str:province>/", views.getIndustryIndexData, name="getIndustryIndexData"),
    path("getLegalEntityNumData/<str:province>/", views.getLegalEntityNumData, name="getLegalEntityNumData"),
    path("getThirdIndustryData/<str:province>/<int:year>/", views.getThirdIndustryData, name="getThirdIndustryData"),
    path("getRCData/<str:province>/", views.getRCData, name="getRCData"),
    path("getIndustryDataByChosenProvinces/", views.getIndustryDataByChosenProvinces, name="getIndustryDataByChosenProvinces"),
    path("getIndustryByYearsData/<str:province>/", views.getIndustryByYearsData, name="getIndustryByYearsData"),
]