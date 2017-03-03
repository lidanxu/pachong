#-*- coding:utf-8 -*-
#编写新浪微博爬虫，使用selenium
import  urllib2
#selenium
from selenium import webdriver

from selenium.webdriver.common.keys import Keys

#微博
class WEIBO:
    def __init__(self,baseurl):
        self.baseurl = baseurl
        #模拟登陆
        headers = {
            'Cookie':'''SINAGLOBAL=3253832672301.4224.1482396752769; wb_g_upvideo_3908997599=1; wvr=6; _s_tentry=cuiqingcai.com; Apache=7392139671314.04.1488244126024; ULV=1488244127004:40:14:2:7392139671314.04.1488244126024:1488161369995; YF-Ugrow-G0=5b31332af1361e117ff29bb32e4d8439; SCF=Am05lptShqkK3MMVkJcLyOZ45vdIxK7UFXfWFB2Drp3DZYH8cofpmrNb6BgTZ1u_wWiL9HrhHvF1qauj9dkZOpk.; SUB=_2A251sIdKDeRxGeVH61oY-SnJwjWIHXVWx_-CrDV8PUJbmtBeLXOmkW-LI6bC4hTvPnr9N9AkYL7N6DO2aQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFXLbEAJr5qV4qykPbKgxU95JpX5o2p5NHD95Q01K5R1K.NSK.4Ws4Dqcj_i--fi-zNi-zXi--fi-zNi-zXi--NiKnRiKnci--NiKnEi-zRi--fi-2Xi-zX; SUHB=0TPV8MnBckTXUx; ALF=1519789308; SSOLoginState=1488254746; UOR=cuiqingcai.com,widget.weibo.com,login.sina.com.cn; YF-V5-G0=d45b2deaf680307fa1ec077ca90627d1; YF-Page-G0=f0e89c46e7ea678e9f91d029ec552e92''',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        }
        req = urllib2.Request(url)

        res = urllib2.urlopen(req)
        
        self.page = res.read()

        self.driver = webdriver.Chrome()
        

    def shouye(self):
        driver = self.driver
        driver.get("http://www.weibo.com")
        #登录
        elem1 = driver.find_element_by_name('username')
        elem2 = driver.find_element_by_name('password')
        elem3 = driver.find_element_by_class_name('login_btn')
        elem1.clear()  #一定要先清除原输入框中的内容
        elem2.clear()
        elem1.send_keys("18200181027")
        elem2.send_keys("121186xld")
        elem3.click()





        print self.driver.page_source
        
        self.driver.close()

        



    

url = 'http://www.weibo.com'
wb = WEIBO(url)
print wb.page
#wb.shouye()
