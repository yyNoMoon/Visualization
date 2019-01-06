# -*- coding: utf-8 -*-
"""
__author__ = 'Gao yue'
__mtime__ = '2018/8/28'
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

# 仅对牛客网剑指offer版块开发的增量爬虫
# 若检测到剑指offer版块的题目数量增加，则进入其中进行爬取
# 与数据库中题目链接进行比对，若题目链接不一致则看作新增题目爬取

import re, sys, time, datetime
import lxml
from lxml import etree
import chardet
import pymysql.cursors
from urllib import request
from bs4 import BeautifulSoup
from http import cookiejar
import http.cookiejar as cookielib


#数据库连接
connect = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='09181024',
    db='lab_project_spider',
    charset='utf8'
)
cursor = connect.cursor()

class NiuKeSpider:

    def __init__(self, block_name, block_site, db_question_list):
        self.block_name = block_name
        self.block_site = block_site
        self.db_question_list = db_question_list


    #利用cookie登录牛客网爬取
    def Get_NiuKe_Page(self, url):
        headers = {
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Cookie': 'NOWCODERUID=A02136A506E2381CDDBCB37B1F566992; callBack=https://www.nowcoder.com/profile/4668279; t=2A6C61A945F4DA01B63DBA36D709168E; NOWCODERCLINETID=1F19A8017AECF77A3A479A4CFFAA053B; Hm_lvt_a808a1326b6c06c437de769d1b85b870=1538814490,1540864999,1540884177,1540948021; Hm_lpvt_a808a1326b6c06c437de769d1b85b870=1541068173; SERVERID=547d00d82311952605c62ceac64f21fd|1541068267|1540864995',
                    'Referer': 'https://www.nowcoder.com/ta/coding-interviews/question-ranking?uuid=abc3fe2ce8e146608e868a70efebf62e&rp=1&lang=2',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
                   }
        time.sleep(3)
        try:
            page = request.Request(url, headers=headers)
        except:
            print("网页打开失败，等待一分钟后进行重连尝试....")
            time.sleep(60)
            page = request.Request(url, headers=headers)
        page_info = str(request.urlopen(page).read(), 'utf-8')  # 打开Url,获取HttpResponse返回对象并读取其ResponseBody
        return page_info

    #首先得到题目列表
    def Get_question_list(self, url):
        page = self.Get_NiuKe_Page(url)
        html = etree.HTML(page)

        #取出数据库中问题的链接
        db_question_link_list = []
        for source in self.db_question_list:
            l = source.split("***")
            db_question_link_list.append(l[2])

        # 得到不在数据库链接中的问题链接列表
        question_link_list = []
        question_title_list = []

        problem_link_list = html.xpath('/html/body/div[1]/div[3]/div[2]/div/div/table/tbody/tr/td[2]/a/@href')
        title_list = html.xpath('/html/body/div[1]/div[3]/div[2]/div/div/table/tbody/tr/td[2]/a/text()')

        for i in range(len(problem_link_list)):
            link = "https://www.nowcoder.com"+problem_link_list[i].replace("&amp;", "&")
            # print("judge the site exists in database or not...")
            if link not in db_question_link_list:
                question_link_list.append(link)
                question_title_list.append(title_list[i].strip())
                print("problem {} needs to update...".format(title_list[i].strip()))
            else:
                pass
                # print("{} don't need to update...".format(title_list[i].strip()))

        update_content_list = []
        # 对不在问题列表中的新问题进行爬取
        for i in range(len(question_link_list)):
            print("update new problem {}".format(question_title_list[i]))
            content = self.Parse_step1(question_link_list[i], question_title_list[i])
            if len(content)!=0:
                update_content_list.append(content)
            time.sleep(5)

        return update_content_list


    #解析在线编程界面中存在的题目，输入输出解释，示例，并得到“查看通过代码的链接”
    def Parse_step1(self, url, title):

        detail_list = []

        page = self.Get_NiuKe_Page(url)
        html = etree.HTML(page)
        title_describe_list = html.xpath('/html/body/div[1]/div/div[1]/div[2]/div[3]/div[1]/text()')
        time_limit_list = html.xpath('/html/body/div[1]/div/div[1]/div[2]/div[1]/div/span[1]/text()')
        space_limit_list = html.xpath('/html/body/div[1]/div/div[1]/div[2]/div[1]/div/span[2]/text()')
        know_point_list = html.xpath('/html/body/div/div/div[1]/div[2]/div[1]/div[2]/a/text()')
        input_describe_list = html.xpath('/html/body/div[1]/div/div[1]/div[2]/div[3]/pre[1]/text()')
        output_describe_list = html.xpath('/html/body/div[1]/div/div[1]/div[2]/div[3]/pre[2]/text()')
        input_sample_list = html.xpath('/html/body/div[1]/div/div[1]/div[2]/div[3]/div[2]/div[2]/div[1]/div/pre/text()')
        output_sample_list = html.xpath('/html/body/div[1]/div/div[1]/div[2]/div[3]/div[2]/div[2]/div[2]/div/pre/text()')

        title_describe = ""
        time_limit = ""
        space_limit = ""
        know_point = ""
        input_describe = ""
        output_describe = ""
        input_sample = ""
        output_sample = ""


        if len(title_describe_list)!=0:
            title_describe += title_describe_list[0]
        if len(time_limit_list)!=0:
            time_limit += time_limit_list[0]
            time_limit = time_limit.replace('时间限制：', '')
        if len(space_limit_list)!=0:
            space_limit += space_limit_list[0]
            space_limit = space_limit.replace('空间限制：', '')
        if len(know_point_list)!=0:
            know_point += " ".join(know_point_list)
        if len(input_describe_list)!=0:
            input_describe += input_describe_list[0]
        if len(output_describe_list)!=0:
            output_describe += output_describe_list[0]
        if len(input_sample_list)!=0:
            input_sample += input_sample_list[0]
        if len(output_sample_list)!=0:
            output_sample += output_sample_list[0]

        help_code_link = "https://www.nowcoder.com"+html.xpath('/html/body/div[1]/div/div[2]/div[4]/div[1]/div/div[2]/a[1]/@href')[0]

        help_c_plus_code_link = help_code_link.replace("&amp;", "&")+"&lang=2"
        help_python3_code_link = help_code_link.replace("&amp;", "&")+"&lang=11"
        help_python2_code_link = help_code_link.replace("&amp;", "&")+"&lang=5"

        c_plus_code, c_plus_answer_source = self.Parse_step2(help_c_plus_code_link)
        if(c_plus_code is None):
            c_plus_code = ""
            c_plus_answer_source = ""
        python3_code, python3_answer_source = self.Parse_step2(help_python3_code_link)
        if(python3_code is None and python3_answer_source is None):
            print("没有Python 3答案！！！")
            python2_code, python2_answer_source = self.Parse_step2(help_python2_code_link)
            if(python2_code is None and python2_answer_source is None):
                python2_code = ""
                source = "牛客***"+self.block_name+"***" + url + "***C_plus_link:" + c_plus_answer_source + "***Python_link:"
                detail_list = [title, title_describe, input_describe, output_describe, input_sample, output_sample, c_plus_code, python2_code, 0, source, time_limit, space_limit, know_point]
                #self.Save_information(title, title_describe, input_describe, output_describe, input_sample, output_sample, c_plus_code, python2_code, 0, source, time_limit, space_limit, know_point)
            else:
                source = "牛客***"+self.block_name+"***"+url+"***C_plus_link:"+c_plus_answer_source+"***Python_link:"+python2_answer_source
                detail_list = [title, title_describe, input_describe, output_describe, input_sample, output_sample, c_plus_code, python2_code, 2, source, time_limit, space_limit, know_point]
                #self.Save_information(title, title_describe, input_describe, output_describe, input_sample, output_sample, c_plus_code, python2_code, 2, source, time_limit, space_limit, know_point)
        else:
            source = "牛客***"+self.block_name+"***" + url + "***C_plus_link:" + c_plus_answer_source + "***Python_link:" + python3_answer_source
            detail_list = [title, title_describe, input_describe, output_describe, input_sample, output_sample, c_plus_code, python3_code, 3, source, time_limit, space_limit, know_point]
            #self.Save_information(title, title_describe, input_describe, output_describe, input_sample, output_sample, c_plus_code, python3_code, 3, source, time_limit, space_limit, know_point)

        return detail_list

    #通过查看可能的代码链接去解析其他页面的存在解答代码的链接
    def Parse_step2(self, url):
        page = self.Get_NiuKe_Page(url)
        html = etree.HTML(page)
        answer_link_list = html.xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/table/tbody/tr[2]/td[7]/a/@href')

        if(len(answer_link_list) != 0):
            answer_link = "https://www.nowcoder.com"+answer_link_list[0].replace("&amp;", "&")
            answer = self.Parse_step3(answer_link)

            return answer, answer_link
        else:
            #print("没有答案！")
            return None, None

    def Parse_step3(self, url):
        page = self.Get_NiuKe_Page(url)
        html = etree.HTML(page)
        answer_list = html.xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/pre/text()')

        problem_answer = ""
        if (len(answer_list) != 0):
            problem_answer += answer_list[0]
        else:
            return None
        problem_answer = problem_answer.replace("&lt;", '<').replace("&gt", '>').replace("&quot;", '"').replace("&amp;", "&")

        return problem_answer



    #将题目和答案等信息存入数据库
    # def Save_information(self, title, title_describe, input_describe, output_describe, input_numbers, output_numbers, c_plus_code, python_code, python_version, source, time_limit, space_limit, knowledge_point):
    #
    #     title = pymysql.escape_string(title)
    #     title_describe = pymysql.escape_string(title_describe)
    #     input_describe = pymysql.escape_string(input_describe)
    #     output_describe = pymysql.escape_string(output_describe)
    #     input_numbers = pymysql.escape_string(input_numbers)
    #     output_numbers = pymysql.escape_string(output_numbers)
    #     c_plus_code = pymysql.escape_string(c_plus_code)
    #     python_code = pymysql.escape_string(python_code)
    #     source = pymysql.escape_string(source)
    #
    #     #当前时间
    #     dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #
    #     insert_sql = "INSERT INTO title_code_total(title,title_describe,input_describe,output_describe,input_numbers,output_numbers,c_plus_code,python_code,python_version,source,time_limit,space_limit,time,knowledge_point) VALUES('%s','%s','%s','%s','%s','%s','%s','%s',%d,'%s','%s','%s','%s','%s')"
    #     insert_data = (title, title_describe, input_describe, output_describe, input_numbers, output_numbers, c_plus_code, python_code, python_version, source, time_limit, space_limit, dt, knowledge_point)
    #
    #     cursor.execute(insert_sql % insert_data)
    #     connect.commit()

# main
# def StartSpider(block_id):
#     Block_dict = {}
#     Block_dict[0] = ["剑指Offer", 'https://www.nowcoder.com/ta/coding-interviews']
#     Block_dict[1] = ["计算机考研复试", 'https://www.nowcoder.com/ta/kaoyan']
#     Block_dict[2] = "pat"         # PAT版块的东西不太一样，后面改一下再加入
#
#     #Module_num = 0
#
#     # 数据库中的数量
#     sql = "SELECT title,source FROM title_code_total WHERE source LIKE CONCAT('%%','%s','%%')"
#     cursor.execute(sql % Block_dict[block_id][0])
#     db_question_list = []
#     for t in cursor.fetchall():
#         db_question_list.append(t[1])
#
#     spider = NiuKeSpider(Block_dict[block_id][0], Block_dict[block_id][1], db_question_list)
#
#     page = spider.Get_NiuKe_Page(Block_dict[block_id][1])
#     html = etree.HTML(page)
#     pageNum_list = html.xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[2]/ul/li/a/@data-page')
#
#     if len(pageNum_list)==0:
#         print("页数寻找不正确")
#     else:
#         pageNum = int(pageNum_list[-1])+1
#         update_num = 0
#         for i in range(1, pageNum):
#             url = Block_dict[block_id][1]+"?query=&asc=true&order=&page="+str(i)
#             update_num += spider.Get_question_list(url)
#
#         print("此次更新了"+str(update_num)+"题")

