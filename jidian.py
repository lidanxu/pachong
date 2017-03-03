#-*- coding:utf-8 -*-
'''
1.模拟登录教务处学生成绩管理系统
2.抓取本学期成绩界面
3.计算打印本学期成绩
*4.将课程号，课序号，课程名，英文课程名，学分，课程属性，成绩抓取下来，并存入数据库
'''
import urllib
import urllib2
import cookielib
import sys
import chardet

filename = 'cookie1'
cookie = cookielib.MozillaCookieJar('cookie1')
#cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)

loginURL = 'http://zhjw.scu.edu.cn/loginAction.do'
response = opener.open(loginURL)
postdata =urllib.urlencode({
    'zjh':'2013141452227',
    'mm':'301662'
})
result = opener.open(loginURL,postdata)
if result:
    print '成功模拟登录'
    print result.read().decode('gbk')
else:
    print '模拟登录失败'
cookie.save(ignore_discard=True,ignore_expires=True)

gradeURL = 'http://zhjw.scu.edu.cn/gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=2015-2016%E5%AD%A6%E5%B9%B4%E6%98%A5(%E4%B8%A4%E5%AD%A6%E6%9C%9F)#qb_2015-2016学年春(两学期)'
user_agent = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'
headers = {'User-Agent':user_agent}
req = urllib2.Request(gradeURL,postdata,headers = headers)
res = opener.open(req)
res = opener.open(gradeURL)
print res
print sys.getfilesystemencoding()
#print '爬取网页的编码是:%',chardet.detect(res)
#print '成绩页面抓取源码如下:'
#html = res.read().decode('gbk')
file1 = open('jidian','a')
file1.write(res.read())
file1.close()
