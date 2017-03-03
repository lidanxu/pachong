#-*- coding:utf-8 -*-
#编写新浪微博爬虫，使用selenium
import  urllib2
#selenium
from selenium import webdriver

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By

#等待
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

#pyquery
from pyquery import PyQuery as pq

import re

from wb_model import *
#微博
class WEIBO:
    def __init__(self):
        #模拟登陆
        self.keyword =[u'nickname',u'realname',u'city',u'sex',u'sextrend',u'love',u'birth',u'blood',u'blog',u'domain_name',u'intro',u'regis_time',u'msn',u'qq',u'email',u'company',u'edu',u'label']
        self.driver = webdriver.Chrome()      
        driver = self.driver
        driver.maximize_window()
        driver.get("http://www.weibo.com")
        #登录
        #driver.implicitly_wait(10)  隐式等待
        #elem1 =  driver.find_element_by_name("username")
        #显式等待
        elem1 = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.NAME,"username")))
        elem1.send_keys("18200181027")
        #elem1 = driver.find_element_by_name('username')
        #elem2 = driver.find_element_by_name('password')
        elem2 = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.NAME,"password")))
        elem2.send_keys("121186xld")
        elem3 = driver.find_element_by_class_name('login_btn')
        #elem1.clear()  #一定要先清除原输入框中的内容
        elem3.click()

        self.driver = driver

    def target(self,url):
        driver = self.driver
        driver.get(url)
        #进入详细信息页面
        #
        driver.implicitly_wait(10)
        elem4 = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CLASS_NAME,'more_txt')))
        elem4.click()

        more_url = driver.current_url

        print more_url

        elem5 = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,'WB_frame_c')))

        #elem5 = driver.find_elements_by_class_name('WB_frame_c')

        print elem5

        driver.implicitly_wait(10)

        elem6 = elem5.find_elements_by_css_selector('li.li_1.clearfix')

        

        print elem6

        tool = Tool()

        dict1 = {}

        for elem in elem6: 
            name = elem.find_element_by_css_selector("span.pt_title.S_txt2").text
            print 'title:',name
            value = elem.find_element_by_css_selector("span.pt_detail").text
            print 'value:',value 
            key = tool.replace(name)
            print 'key:',key

            dict2 = {key:value}

            if dict2.keys()[0] in self.keyword:
                dict1.update(dict2)
        
        self.person = dict1


class Tool:
    nickname = re.compile(u'昵称：')
    realname = re.compile(u'真实姓名：')
    city = re.compile(u'所在地：')
    sex = re.compile(u'性别：')
    sextrend = re.compile(u'性取向：')
    love = re.compile(u'感情状况：')
    birth = re.compile(u'生日：')
    blood = re.compile(u'血型：')
    blog = re.compile(u'博客地址：')
    domain_name = re.compile(u'个性域名：')
    intro = re.compile(u'简介：')
    regis_time = re.compile(u'注册时间：')
    msn = re.compile(u'MSN：')
    qq = re.compile(u'QQ：')
    email = re.compile(u'邮箱：')
    company = re.compile(u'公司：')
    edu = re.compile(u'大学：')
    label = re.compile(u'标签：')
    def replace(self,x):
        x = re.sub(self.nickname,u'nickname',x)
        x = re.sub(self.realname,u'realname',x)
        x = re.sub(self.city,u'city',x)
        x = re.sub(self.sex,u'sex',x)
        x = re.sub(self.sextrend,u'sextrend',x)
        x = re.sub(self.love,u'love',x)
        x = re.sub(self.birth,u'birth',x)
        x = re.sub(self.blood,u'blood',x)
        x = re.sub(self.blog,u'blog',x)
        x = re.sub(self.domain_name,u'domain_name',x)
        x = re.sub(self.intro,u'intro',x)
        x = re.sub(self.regis_time,u'regis_time',x)
        x = re.sub(self.msn,u'msn',x)
        x = re.sub(self.qq,u'qq',x)
        x = re.sub(self.email,u'email',x)
        x = re.sub(self.company,u'company',x)
        x = re.sub(self.edu,u'edu',x)
        x = re.sub(self.label,u'label',x)
        return x


        
        #self.driver.close()

        


if __name__ == '__main__':

    wb = WEIBO()
    wb.target("http://weibo.com/520820326")
