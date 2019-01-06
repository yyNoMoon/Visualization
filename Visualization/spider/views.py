from django.http import HttpResponse
from django.shortcuts import render
import threading
import time, datetime
import json
from lxml import etree
import pymysql.cursors
from .utils import NiuKeSpider

threadLock = threading.Lock()
exit_class_dictionary = {}
function_message = {}  # 请使用之前清空

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


def index(request):
    return render(request, "spider/spider_show.html")

# 为线程定义一个函数
def spider_function(threadID, threadName, block_id, __flag, __running):
    # __flag为暂停位
    # __running为终止位
    global function_message
    # while 1:
    if __running.isSet() != True:
        return
    __flag.wait()

    block_dict = {}
    block_dict[0] = ["剑指Offer", 'https://www.nowcoder.com/ta/coding-interviews']
    block_dict[1] = ["计算机考研复试", 'https://www.nowcoder.com/ta/kaoyan']
    block_dict[2] = "pat"  # PAT版块的东西不太一样，后面改一下再加入

    # 数据库中的数量
    sql = "SELECT title,source FROM title_code_total WHERE source LIKE CONCAT('%%','%s','%%')"
    try:
        cursor.execute(sql % block_dict[block_id][0])
    except Exception as e:
        function_message[threadID] = "查找原有该版块数据错误"

    # 原有该版块题目
    db_question_list = []
    for t in cursor.fetchall():
        db_question_list.append(t[1])

    spider = NiuKeSpider(block_dict[block_id][0], block_dict[block_id][1], db_question_list)

    #查找该版块的总页数
    page = spider.Get_NiuKe_Page(block_dict[block_id][1])
    html = etree.HTML(page)
    pageNum_list = html.xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[2]/ul/li/a/@data-page')
    if len(pageNum_list) == 0:
        print("页数寻找不正确")
    else:
        pageNum = int(pageNum_list[-1]) + 1
        # 启动爬虫
        function_message[threadID] = "启动爬虫"
        for i in range(1, pageNum):
            if __running.isSet() != True:
                return
            __flag.wait()

            function_message[threadID] = "解析第{}页".format(i)
            url = block_dict[block_id][1] + "?query=&asc=true&order=&page=" + str(i)
            content_list = spider.Get_question_list(url)
            function_message[threadID] = "解析第{}页结束，存储数据".format(i)

            # 获取锁，用于线程同步
            threadLock.acquire()
            try:
                for content in content_list:
                    title = pymysql.escape_string(content[0])
                    title_describe = pymysql.escape_string(content[1])
                    input_describe = pymysql.escape_string(content[2])
                    output_describe = pymysql.escape_string(content[3])
                    input_numbers = pymysql.escape_string(content[4])
                    output_numbers = pymysql.escape_string(content[5])
                    c_plus_code = pymysql.escape_string(content[6])
                    python_code = pymysql.escape_string(content[7])
                    source = pymysql.escape_string(content[9])

                    # 当前时间
                    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    insert_sql = "INSERT INTO title_code_total(title,title_describe,input_describe,output_describe," \
                                 "input_numbers,output_numbers,c_plus_code,python_code,python_version,source,time_limit," \
                                 "space_limit,time,knowledge_point) VALUES('%s','%s','%s','%s','%s','%s','%s','%s',%d,'%s'," \
                                 "'%s','%s','%s','%s')"
                    insert_data = (
                    title, title_describe, input_describe, output_describe, input_numbers, output_numbers, c_plus_code,
                    python_code, content[8], source, content[10], content[11], dt, content[12])

                    try:
                        cursor.execute(insert_sql % insert_data)
                        connect.commit()
                    except Exception as e:
                        function_message[threadID] = e
                        print("数据插入错误")
                # 放心使用
                # print("对数据库进行操作，需要加锁")
                # function_message = ""
                # function_message = "{}对数据库进行操作，需要加锁".format(time.ctime(time.time()))
                function_message[threadID] = "版块{} 第{}页 题目更新完成{}道".format(block_dict[block_id][0], i, len(content_list))
            finally:
                # 释放锁
                threadLock.release()

        time.sleep(3)
        function_message[threadID] = "OVER"

    print("%s: %s" % (threadName, time.ctime(time.time())))

    time.sleep(1)


class myThread(threading.Thread):
    def __init__(self, threadID, name, block_id):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.block_id = block_id
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__flag_True_or_False = True
        self.__running = threading.Event()
        self.__running.set()  # 设置为True
        function_message[self.threadID] = "启动爬虫{}".format(threadID)

    def run(self):
        print("开始线程：" + self.name)
        spider_function(self.threadID, self.name, self.block_id, self.__flag, self.__running)

        print("退出线程：" + self.name)

    def getFlag(self):
        return self.__flag_True_or_False

    def pause(self):
        self.__flag.clear()  # 设置为False,先线程阻塞
        self.__flag_True_or_False = False
        message = "{}{}已经暂停".format(time.ctime(time.time()), self.name)
        return message

    def resume(self):
        self.__flag.set()  # 设置为True,让线程停止阻塞
        self.__flag_True_or_False = True
        message = "{}{}已经恢复".format(time.ctime(time.time()), self.name)
        return message

    def stop(self):
        self.__flag.set()
        self.__flag_True_or_False = True
        self.__running.clear()
        message = "{}{}已经停止".format(time.ctime(time.time()), self.name)
        return message


def hello(request):
    return render(request, "spider_show.html")


def button_callback(request):
    request.encoding = "utf-8"
    # print(request.GET)
    temp_button_name = ""
    for key, value in request.GET.items():
        # print("key:",key)
        temp_button_name = key
    # print("value:",value)
    # print("button_name:",temp_button_name)
    button_name = int(temp_button_name)
    message = ""
    # 开始11
    # 暂停12
    # 终止13
    choose_id = int(button_name / 10)
    choose_what_button = int(button_name % 10)
    if exit_class_dictionary.get(choose_id, False):
        thread = exit_class_dictionary[choose_id]
    # 开始按钮
    if choose_what_button == 1:
        if exit_class_dictionary.get(choose_id, False) == False:
            thread = myThread(choose_id, "第{}个版块".format(choose_id), choose_id-1)
            exit_class_dictionary[choose_id] = thread
            time.sleep(0.5)
            # Flag=thread.getFlag()

            # print("thread.getFlag():",Flag)
            # if thread.isAlive()==False and thread.getFlag()==True:
            thread.start()
            message = "{}第{}个版块开始爬虫".format(time.ctime(time.time()), choose_id)
        elif thread.getFlag() == False and thread.isAlive() != False:
            message = thread.resume()
            message = "{}第{}个版块恢复爬虫".format(time.ctime(time.time()), choose_id)
        else:
            message = "{}第{}个版块正在爬虫".format(time.ctime(time.time()), choose_id)
    elif choose_what_button == 2:
        if exit_class_dictionary.get(choose_id, False) != False:
            message = thread.pause()
        else:
            message = "请点开始"
    else:
        if exit_class_dictionary.get(choose_id, False) != False:
            message = thread.stop()
            time.sleep(1)
            exit_class_dictionary.pop(choose_id)
            del thread
            message = "{}第{}个版块终止爬虫".format(time.ctime(time.time()), choose_id)
        else:
            message = "请点开始"
    message_dictionary = {"message": message, "function_message": function_message}
    # message_dictionary=message_dictionary
    # print(message)
    # print(function_message)
    # if message=="请点开始":
    # message_dictionary={"message":message}
    # return HttpResponse(json.dumps(message_dictionary))
    # else:
    return HttpResponse(json.dumps(message_dictionary))