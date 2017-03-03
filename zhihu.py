#-*-coding: utf-8 -*-

import urllib2
import re
import cookielib
import MySQLdb
import sys

#f_handler= open('zhihuout','w')
#sys.stdout = f_handler

class Tool:
    removeImg = re.compile('<img.*?>')
    removeAddr = re.compile('<a.*?>|</a>')
    removeLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,'',x)
        x = re.sub(self.removeAddr,'',x)
        x = re.sub(self.removeLine,'\n',x)
        x = re.sub(self.replaceTD,'\t',x)
        x = re.sub(self.replacePara,'\n',x)
        x = re.sub(self.replaceBR,'\n',x)
        x = re.sub(self.removeExtraTag,'',x)
        return x.strip()


class ZH:
    def __init__(self):
        self.baseurl = None
        self.tool =Tool()

    #实现模拟登录并抓取网页源代码
    def Login(self,url):
        loginURL ='https://www.zhihu.com/topic/19550517/hot'
       # cookie = cookielib.MozillaCookieJar()
       # cookie.load('cookie2',ignore_discard=True,ignore_expires=True)
       # handler = urllib2.HTTPCookieProcessor(cookie)
       # opener = urllib2.build_opener(handler)
        headers={'cookie':'d_c0="ADCC2oyhCQuPTlpTLmzIFbQ9Fj_00ZiF470=|1482404890"; q_c1=f18ec1605ca34d3fbadb0abc6def089d|1482404890000|1482404890000; _zap=2931f801-b65f-4ceb-954e-2d7e6fe666bf; _xsrf=97e0388130d156ef2e9ec719803db9b4; l_cap_id="ZjA3NDdjOWU4NGJhNGZkZTllNjY4ZWRkNDdkMTkyMzc=|1483695359|c40a8a870188a1aa577952f583f5a7ceede824b0"; cap_id="MjQzODAyYWRhZTZmNDc4OGJjMmU4ODZjYzk0NmE5YzQ=|1483695359|36a6e64ff3eaf027f2b699aa202a22cfeefedc34"; r_cap_id="YWQ3ZTAwZDhkZGUxNDNlOGIwODRkYTM4ZDEwZmZjMjI=|1483695361|53554aa58e18e9c075e3b19938556fcdfe557d1c"; login="NWFmNmVhMmJmMDAzNDNmOWJlNGE1MDJkOGFjYWZiNzY=|1483695385|4d6b5e769ea9de7aebb774ef0cd4a370920cef69"; aliyungf_tc=AQAAAKhaSXBK4gwANshwduKRIfe5wTt3; __utma=51854390.1929025690.1484647653.1484647653.1484749553.2; __utmb=51854390.0.10.1484749553; __utmc=51854390; __utmz=51854390.1484749553.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=51854390.100--|2=registration_date=20160930=1^3=entry_date=20160930=1; z_c0=Mi4wQUFCQW1LaHFuZ29BTUlMYWpLRUpDeGNBQUFCaEFsVk5HZktXV0FBX1REbVY4WTU4Z3puWDF0SHkwRXR4TmlLTmdn|1484749556|1ac3e44226fa45f0d5a41401a4d5f16faeb04a85',
                 'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'
                }

        req = urllib2.Request(url,headers=headers)

        res = urllib2.urlopen(req)
        #self.page表示的是问题页面首页的源代码
        self.page = res.read()
   #     if '爆炸头芭芭' in self.page:
    #        print "登录成功"
           # with open('zhihu1','w+') as file1:
            #    file1.write(self.page)
     #   else:
      #      print "登录失败"

    #没有登录的情况下获取页面源代码
    def getPage(self,url):
        user_agent = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'
        header = {'User-Agent':user_agent}
        req = urllib2.Request(url,headers = header)
        res = urllib2.urlopen(req)
        self.page =  res.read()
    #获取问题页面首页的问题标题及网址
    def getQuestionTitle(self):
        pattern = re.compile('<h2><a class="question_link" href="(.*?)".*?>(.*?)</a></h2>',re.S)

        result = re.findall(pattern,self.page)
        if not result:
            print '出错，返回空'
        else:
            self.questionURL = []
            self.title = []
            for res in result:
                self.questionURL.append('http://www.zhihu.com'+ res[0])
                self.title.append(res[1])
    #进入问题页，抓取问题页的源代码
    def getQuestionURL(self):
        #如果抓取到问题的链接非空
        if self.questionURL:
            self.q_page = []
            for q_url in self.questionURL:
                #根据Login()方法获取问题页面的源代码
                self.Login(q_url)
                #定义self.q_page为具体问题页面的源代码
                self.q_page.append(self.page)
                #filename = 'zhihu' + str(i)
                #with open(filename,'w+') as file1:
                #    file1.write(q_page)
               # i += 1
        else:
            print'问题网址出错'
    
    #抓取具体问题页面内有的信息，包括发表人，发表内容，发表时间，评论数，赞同数
    def getcontent(self,x):
        #以下还有一个问题是没有抓取发问人的信息，而且注意和问题首页一样还不能抓取动态的信息
        if x==0:
            #(选择0,则表示抓取的信息是发表人)
            #发表人信息有几个要注意的地方
            #1.发表人非匿名，但是可能没有那个介绍短句
            #2.发布人可能是匿名的
            pattern1 =re.compile('<div class="answer-head">(.*?)</span>.</div>',re.S)

           # pattern = re.compile('（<span class="author-link-line">..<a class="author-link".*?" href="(.*?)".>(.*?)</a></span>(<span title="(.*?)" class="bio">)?|',re.S)
            self.personurl = []
            self.person =[]
            self.personbio =[]
            for qp in self.q_page:
                result1 = re.findall(pattern1,qp)
                if result1:
                    for res in result1:
                        if '匿名用户' not in res:
                        #存在部分用户有personbio属性，部分没有这个属性
                 #       print res[0]
                  #      print res[1]
                            pattern = re.compile('<span class="author-link-line">..<a class="author-link".*?" href="(.*?)".>(.*?)</a></span>(<span title="(.*?)" class="bio">)?',re.S)
                            res1 = re.search(pattern,res)
                            self.personurl.append('http://www.zhihu.com'+res1.group(1))
                            self.person.append(res1.group(2))
                            if res1.group(4):
                                self.personbio.append(res1.group(4))
                            else:
                                self.personbio.append('None')
                        else:
                            self.personbio.append('None')
                            self.person.append('匿名用户')
                            self.personurl.append('None')
                else:
                    print '查找用户信息出错'
                

        if x==1:
            #(选择1,则表示抓取的信息是发布时间)
            pattern =re.compile('发布于(.*?)(<|")',re.S)
            self.time =[]
            for qp in self.q_page:
               # print '第 %d 页发布时间：'%i
                result = re.findall(pattern,qp)
                if result:
                    for res in result:
                        #print res
                        self.time.append(res[0].strip())
                else:
                    print '问题页码匹配出错'

        
        if x==2:
            #(选择2,则表示抓取信息是发表内容)
            pattern = re.compile('div class="zm-editable-content clearfix".*?>(.*?)</div>',re.S)
            i = 1
            self.content =[]
            for qp in self.q_page:
               # print "这是第 %d 个问题页面抓取的问题内容"%i
                result = re.findall(pattern,qp)
                if result:
                    for res in result:
                        #print res
                        self.content.append(self.tool.replace(res))
                else:
                    print '问题页面匹配出错'
                i += 1
        if x==3:
            #(选择3,则表示抓取信息是评论数)
            # 考虑如果没有评论则代码不是0条评论！同理可推赞数
            pattern = re.compile('<i class="z-icon-comment"></i>(\d+) 条评论</a>',re.S)
            i = 1
            self.comment =[]
            for qp in self.q_page:
               # print "这是第 %d 个问题页面抓取的问题评论数"%i
                result = re.findall(pattern,qp)
                if result:
                    for res in result:
                #        print res
                        self.comment.append(res.strip())
                else:
                    print '问题页面匹配出错'
                i += 1
        if x==4:
            #(选择4,则表示抓取信息是赞同数)        
            pattern = re.compile('<span class="js-voteCount">(.*?)</span>&nbsp;人赞同</a></span>',re.S)
            i = 1
            self.zan =[]
            for qp in self.q_page:
               # print "这是第 %d 个问题页面抓取的问题赞数"%i
                result = re.findall(pattern,qp)
                if result:
                    for res in result:
                #        print res
                        self.zan.append(res.strip())
                else:
                    print '问题页面匹配出错'
                i += 1

#将抓取的信息存放到数据库中，建立一个数据库类
class MYSQL:
    def __init__(self,content):
    #    try:
        self.conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='121186',charset='utf8')
        print '成功连接'
        self.cursor = self.conn.cursor()
        self.cursor.execute("drop database if exists zhihu")
        self.cursor.execute("create database zhihu default charset utf8")
        self.conn.select_db('zhihu')
        print '成功与数据库zhihu相连接'
        self.cursor.execute("create table log(person text,personurl text,personbio text,time varchar(50),content text,comment int,zan int)")
        print'建立表格'
        self.cursor.executemany("insert into log values(%s,%s,%s,%s,%s,%s,%s)",content)
        print '执行插入操作'
        self.conn.commit()
        print '成功插入'
        print '完成存入数据库的操作'
#        except:
 #           self.conn.rollback()
  #          print '出错，回滚'
   #     finally:
        self.cursor.close()
        self.conn.close()
    def mysqlSelect(self):
        self.conn = MySQLdb.Connection(host='127.0.0.1',user='root',passwd='121186')
        self.cursor = self.conn.cursor()
        self.conn.select_db('zhihu')
        self.count = self.cursor.execute('select * from log')
        print '总有 %d 条记录'%self.count

        self.cursor.scroll(0,mode='absolute')
        results = self.cursor.fetchall()
        for res in results:
            print'person:%s\npersonurl:%s\npersonbio:%s\ntime:%s\ncontent:%s\ncomment:%s\nzan:%s\n'%res

        self.cursor.close()
        self.conn.close()


url='https://www.zhihu.com/topic/19550517/hot'
#baseURL = raw_input('请输入网址：')
zh = ZH()
zh.Login(url)
zh.getQuestionTitle()
zh.getQuestionURL()
zh.getcontent(0)
zh.getcontent(1)
zh.getcontent(2)
zh.getcontent(3)
zh.getcontent(4)
contents =[]
i = 0
for i in range(41):
    contents.append((zh.person[i],zh.personurl[i],zh.personbio[i],zh.time[i],zh.content[i],zh.comment[i],zh.zan[i]))
    i += 1

mysql1 = MYSQL(contents)
mysql1.mysqlSelect()
print 'person:'+str(len(zh.person))
print 'personurl:'+str(len(zh.personurl))
print 'personbio:'+str(len(zh.personbio))
print 'time:'+str(len(zh.time))
print 'content:'+str(len(zh.content))
print 'comment:'+str(len(zh.comment))
print 'zan:'+str(len(zh.zan))
#f_handler.close()

