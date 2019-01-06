from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Max,Min
from province.models import DataProvince, AttributeData
import pymysql.cursors
import json

# Create your views here.
#数据库连接
# connect = pymysql.Connect(
#     host='localhost',
#     port=3306,
#     user='root',
#     passwd='09181024',
#     db='visualize_data',
#     charset='utf8'
# )
# cursor = connect.cursor()

area_dict = {
    "安徽": "华东",
    "北京": "华北",
    "福建": "华东",
    "甘肃": "西北",
    "广东": "华南",
    "广西": "华南",
    "贵州": "西南",
    "海南": "华南",
    "河北": "华北",
    "河南": "华中",
    "黑龙江": "东北",
    "湖北": "华中",
    "湖南": "华中",
    "吉林": "东北",
    "江苏": "华东",
    "江西": "华东",
    "辽宁": "东北",
    "内蒙古": "华北",
    "宁夏": "西北",
    "青海": "西北",
    "山东": "华东",
    "山西": "华北",
    "陕西": "西北",
    "上海": "华东",
    "四川": "西南",
    "天津": "华北",
    "西藏": "西南",
    "新疆": "西北",
    "云南": "西南",
    "浙江": "华东",
    "重庆": "西南",
}

def index(request):
    return render(request, "province/chengpin.html")


def getAllProvinceData(request):
    """
    :param request: request parameter
    :return: 主视图构建————每年所有省份的金融机构数量
    """
    if request.method == "GET":
        data = {}
        data["yearList"] = []
        data["FI_NUM"] = []
        data["GDP"] = []
        data["PI_VAI"] = []
        data["SI_VAI"] = []
        data["TI_VAI"] = []
        data["FI_VAI"] = []
        for year in range(2010, 2017):
            data["yearList"].append(str(year)+"年")
            provinces = []
            gdps = []
            pis = []
            sis = []
            tis = []
            fis = []

            dataList = DataProvince.objects.filter(year=year)
            attributeList = AttributeData.objects.filter(year=year)

            for dl in dataList:
                provinces.append({"name": dl.province, "value": dl.num})
            for al in attributeList:
                gdps.append({"name": al.province, "value": al.AVG_GDP})
                pis.append({"name": al.province, "value": al.PI_VAI})
                sis.append({"name": al.province, "value": al.SI_VAI})
                tis.append({"name": al.province, "value": al.TI_VAI})
                fis.append({"name": al.province, "value": al.FI_VAI})

            data["FI_NUM"].append(provinces)
            data["GDP"].append(gdps)
            data["PI_VAI"].append(pis)
            data["SI_VAI"].append(sis)
            data["TI_VAI"].append(tis)
            data["FI_VAI"].append(fis)

        response = HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"

        return response
    else:
        return HttpResponse("error post!")


def getIndustryIndexData(request, province):
    """
    IndustryIndexData: 该省份2010-2016第一第二第三产业的指数————分视图C: 某省产业占比;
    :param request:
    :param year: year
    :param province: province name
    :return: IndustryIndexData
    """
    PI_dataList = AttributeData.objects.filter(province__icontains=province, year__gte=2010).values('PI_VAI').order_by('year')
    SI_dataList = AttributeData.objects.filter(province__icontains=province, year__gte=2010).values('SI_VAI').order_by('year')
    TI_dataList = AttributeData.objects.filter(province__icontains=province, year__gte=2010).values('TI_VAI').order_by('year')

    returnData = []
    PI = []
    SI = []
    TI = []
    for i in range(len(PI_dataList)):
        PI.append(round(PI_dataList[i]['PI_VAI']-100, 2))
        SI.append(round(SI_dataList[i]['SI_VAI']-100, 2))
        TI.append(round(TI_dataList[i]['TI_VAI']-100, 2))
    returnData.append(PI)
    returnData.append(SI)
    returnData.append(TI)

    response = HttpResponse(json.dumps(returnData, ensure_ascii=False), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"

    return response


def getLegalEntityNumData(request, province):
    """
    LegalEntityNumData: 某一年的该省份各个产业法人单位个数————分视图D: 某年某省法人单位个数;
    :param request:
    :param year: year
    :param province: province name
    :return: LegalEntityNumData
    """
    if request.method == "GET":

        data = {}
        data["FI_CR"] = []
        data["REI_CR"] = []
        data["STG_CR"] = []
        data["ICS_CR"] = []
        for year in range(2012, 2017):
            dataList = AttributeData.objects.get(province__icontains=province, year=year)

            data["FI_CR"].append(round(dataList.FI_CR-100, 2))
            data["REI_CR"].append(round(dataList.REI_CR-100, 2))
            data["STG_CR"].append(round(dataList.STG_CR-100, 2))
            data["ICS_CR"].append(round(dataList.ICS_CR-100, 2))

        print(data)

        response = HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"

        return response
    else:
        return HttpResponse("error post")


def getThirdIndustryData(request, province, year):
    """
    ThirdIndustryData: 某一年的该省份第三产业各个分产业的占比————分视图E: 某年某省第三产业情况;
    :param request:
    :param year: year
    :param province: province name
    :return: ThirdIndustryData
    """
    if request.method == "GET":
        dataList = AttributeData.objects.filter(province__icontains=province, year=year)
        returnData = {}
        returnData['Indexdata'] = []
        returnData['TIdata'] = []

        if len(dataList) != 0:
            returnData['Indexdata'].append({"name": "第一产业", "value": dataList[0].PI_VA})
            returnData['Indexdata'].append({"name": "第二产业", "value": dataList[0].SI_VA})
            returnData['Indexdata'].append({"name": "第三产业", "value": dataList[0].TI_VA})
            returnData['TIdata'].append({"name": "金融业增加值", "value": dataList[0].FI_VA})
            returnData['TIdata'].append({"name": "房地产业增加值", "value": dataList[0].REI_VA})
            returnData['TIdata'].append({"name": "住宿和餐饮业增加值", "value": dataList[0].ACI_VA})
            returnData['TIdata'].append({"name": "批发和零售业增加值", "value": dataList[0].WR_VA})
            returnData['TIdata'].append({"name": "其他行业增加值", "value": dataList[0].OI_VA})

        response = HttpResponse(json.dumps(returnData, ensure_ascii=False), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"

        return response
    else:
        return HttpResponse("error post")


def getRCData(request, province):
    """
    RCData: 某一年的该省份城市农村的消费水平数据（平均消费及消费指数）————分视图F: 某年某省城市农村发展情况;
    :param request:
    :param year: year
    :param province: province name
    :return: RCData
    """
    if request.method == "GET":
        dataList = AttributeData.objects.filter(province__icontains=province, year__gte=2010).order_by('year')

        returnData = {}
        returnData['R_RCL'] = []
        returnData['U_RCL'] = []
        returnData['R_RCLI'] = []
        returnData['U_RCLI'] = []

        for data in dataList:
            returnData['R_RCL'].append(data.R_RCL)
            returnData['U_RCL'].append(data.U_RCL)
            returnData['R_RCLI'].append(data.R_RCLI)
            returnData['U_RCLI'].append(data.U_RCLI)

        response = HttpResponse(json.dumps(returnData, ensure_ascii=False), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"

        return response
    else:
        return HttpResponse("error post")


def getIndustryDataByChosenProvinces(request):
    """
    RCData: 某一年的用户选择的省份分产业数据
    :param request:POST
    :param chosenYear: chosenYear
    :param chosenProvinces: chosenProvinces name
    :return:
    """
    if request.method == "POST":
        chosenProvinces = request.POST.get('provinces')
        chosenProvinces = json.loads(chosenProvinces)
        chosenYear = request.POST.get('year')

        # print(str(chosenYear)+str(chosenProvinces))

        returnData = []

        for province in chosenProvinces:
            dataList = AttributeData.objects.filter(province__icontains=province, year=chosenYear)
            FI_NUM = DataProvince.objects.get(province=province, year=chosenYear)

            line_dict = {}
            line_list = []
            line_list.append(province)
            line_list.append(dataList[0].PI_VAI-100)
            line_list.append(dataList[0].SI_VAI-100)
            line_list.append(dataList[0].TI_VAI-100)
            line_list.append(dataList[0].FI_VAI-100)
            line_list.append(dataList[0].REI_VAI-100)
            line_list.append(FI_NUM.num)
            line_list.append(area_dict[province])

            line_dict['name'] = province
            line_dict['value'] = line_list

            returnData.append(line_dict)

        # print(returnData)
        # print(returnData)

        response = HttpResponse(json.dumps(returnData, ensure_ascii=False), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"

        return response
    else:
        return HttpResponse("error get")


def getIndustryByYearsData(request, province):
    """
    IndustryData: 所有年份该省第一第二产业第三产业的数据，按年份排序————分视图B: 历年某省各个产业变化情况;
    :param request:
    :param province: province name
    :return: IndustryData
    """
    if request.method == "GET":

        data = {}
        data["PI_VAI"] = []
        data["SI_VAI"] = []
        data["TI_VAI"] = []
        data["FI_VAI"] = []
        data["REI_VAI"] = []
        data["ACI_VAI"] = []
        data["OI_VAI"] = []
        for year in range(2010, 2017):
            dataList = AttributeData.objects.get(province__icontains=province, year=year)

            data["PI_VAI"].append(round(dataList.PI_VAI-100, 2))
            data["SI_VAI"].append(round(dataList.SI_VAI-100, 2))
            data["TI_VAI"].append(round(dataList.TI_VAI-100, 2))
            data["FI_VAI"].append(round(dataList.FI_VAI-100, 2))
            data["REI_VAI"].append(round(dataList.REI_VAI-100, 2))
            data["ACI_VAI"].append(round(dataList.ACI_VAI-100, 2))
            data["OI_VAI"].append(round(dataList.OI_VAI-100, 2))

        # print(data)

        response = HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"

        return response
    else:
        return HttpResponse("error post")
