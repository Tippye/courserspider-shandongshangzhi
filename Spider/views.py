import time

from django.http import JsonResponse
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
import re


# Create your views here.

def isExist(browser, xpath):
    """
    判断页面中是否存在此元素
    :param browser:     浏览器对象
    :param xpath:   要判断的元素的xpath
    :return:bool
    """
    try:
        browser.find_element_by_xpath(xpath)
        return True
    except:
        return False


def getTerm():
    """
    获取当前学期，按时间计算，2-7月为第一学期，8-1月为第二学期
    :return: Number 学期数
    """
    month = time.localtime(time.time())[1]
    if (month > 1 and month < 8):
        return 2
    return 1


def getCourse(request):
    # 返回数据的格式
    response = {
        'data': '',
        'state': 0
    }

    # 不传week时默认为第一周
    weeks = '1'

    # 周一到周五
    week = 5

    # 一天的课程数
    class_num = 10

    # 获取传入参数
    try:
        weeks = str(request.GET['week'])
    except:
        pass
    try:
        username = request.GET['username']
        password = request.GET['password']
    except:
        print('用户信息缺失')
        response['data'] = "Please input username or password"
        return JsonResponse(response, safe=False)

    option = webdriver.ChromeOptions()
    # 隐藏浏览器窗口
    option.add_argument('headless')
    # 启动浏览器
    bro = webdriver.Chrome(options=option)
    # 访问学校官网
    bro.get("http://szyjxgl.sict.edu.cn:9000/eams/login.action")
    # 输入用户名和密码
    username_ipt = bro.find_element_by_id("username")
    password_ipt = bro.find_element_by_id("password")
    username_ipt.send_keys(username)
    password_ipt.send_keys(password)

    # 等待0.2秒后登录，点击登录太快会提示错误
    sleep(0.2)
    bro.find_element_by_name("submitBtn").click()

    # 查找页面上是否有密码错误的提示，如果有就返回密码错误
    if isExist(bro, '//*[@id="messages16741228231"]/div/div/span[2]'):
        print('密码错误')
        response['data'] = "Password Error"
        bro.quit()
        return JsonResponse(response, safe=False)

    # 密码正确进入管理页面，选择我的课表
    syllabus = bro.find_elements_by_class_name("p_1")
    for s in syllabus:
        if s.text == "我的课表":
            s.click()

    # 判断是否被加载出来
    courseTableTypeExist = False
    while courseTableTypeExist == False:
        sleep(0.001)
        courseTableTypeExist = isExist(bro, '//*[@id="courseTableType"]')
    # 课表类型为学生课表
    Select(bro.find_element_by_id("courseTableType")).select_by_value("std")
    # 更换为当前周的课表
    Select(bro.find_element_by_id("startWeek")).select_by_value(str(weeks))
    # 更换学期  142是第一学期，143是第二学期
    bro.execute_script(
        'document.getElementById("semesterCalendar_target").value = ' + str(141 + getTerm()))
    # 点击切换学期按钮
    bro.find_element_by_xpath('//*[@id="courseTableForm"]/div[2]/input[2]').click()

    # 等待刷新
    sleep(0.2)
    # 用来存放结果的数组
    result = []
    for i in range(0, week):
        for j in range(0, class_num):
            # 利用 i 和 j 拼接出单元格的id
            if i == 0:
                n = str(j)
            else:
                n = str(i) + str(j)
            if isExist(bro, '// *[ @ id = "TD' + n + '_0"]'):
                c = bro.find_element_by_id("TD" + n + "_0")
                try:
                    if c.get_attribute("title"):
                        # 获取到单元格显示的内容
                        course_title = c.get_attribute("title")
                        # 从单元格显示内容中提取出来课程名称
                        course_name = course_title.split('(', 1)[0]
                        # 从单元格显示内容中提取出来讲课老师
                        course_teacher = \
                            re.search(r'\(\D{2,5}\);;;\(', course_title).group().split('(', 1)[1].split(')', 1)[0]
                        # 从单元格显示内容中提取出上课教室
                        course_classroom = \
                            re.search(r';;;\(.*?,.*?\)', course_title).group().split(',', 1)[1].split(')')[0]
                        # 将获取到的数据封装成一个字典放到结果数组中
                        # continued时指这节课会讲几节课，也就是这节课在课表中竖着占了几个空
                        result.append({
                            "courseName": course_name,
                            "teacher": course_teacher,
                            "classroom": course_classroom,
                            "day": i + 1,
                            "num": j + 1,
                            "continued": c.get_attribute("rowspan")
                        })
                except:
                    pass

    # 将课表结果放到返回的数据中
    response['data'] = result
    response['state'] = 1
    bro.quit()
    return JsonResponse(response, safe=False)
