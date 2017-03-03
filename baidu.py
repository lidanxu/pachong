#-*-coding:utf-8 -*-                                                        
import urllib2
import re
 
import MySQLdb

import chardet
  
#处理页面标签类
class Tool:
    #去除img标签，7位长空格
    removeImg = re.compile('<img.*?>')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换成\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换成\t
    replaceTD = re.compile('<td>')
    #把段落开头换成\n加两个空格
    replacePara = re.compile('<p.*?>')
    #将换行符或双行符替换成\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其他的标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,'',x)
        x = re.sub(self.removeAddr,'',x)
        x = re.sub(self.replaceLine,'\n',x)
        x = re.sub(self.replaceTD,'\t',x)
        x = re.sub(self.replacePara,'\n  ',x)
        x = re.sub(self.replaceBR,'\n',x)
        x = re.sub(self.removeExtraTag,'',x)
        return x.strip()              
    
class BDTB:
    def __init__(self,baseUrl,seeLZ,floorTag):
        #base链接地址
        self.baseURL = baseUrl
        #是否只看楼主
        self.seeLZ = '?see_lz=' + str(seeLZ)
        #HTML标签剔除工具类对象
        self.tool = Tool()
        #楼层标号，初始为1
        self.floor = 1
        #默认的标题，如果没有成功获取到标题的话则用这个标题
        self.defaultTitle = "百度贴吧"
        #是否写入楼分隔符
        self.floorTag = floorTag
    def getPage(self,pageNum): 
        try:
            url = self.baseURL+self.seeLZ+'&pn='+str(pageNum)
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
            headers = {'User-Agent':user_agent}
            request =urllib2.Request(url,headers=headers)
            response = urllib2.urlopen(request)


            #检查编码方式
      #      print '检查编码方式' 
       #     print chardet.detect(response.read())

            return response.read()
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print '错误reason',e.reason
                return None

    #获取百度贴吧的标题
    def getTitle(self,pageNum):
        page = self.getPage(pageNum)
        pattern =re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
        result =re.search(pattern,page)
        if result:
            return result.group(1)
        else:
            return None
    #获取该贴的总页数
    def getPageNum(self):
        page = self.getPage(1) 
            
        pattern = re.compile('pn=(\d+)">\xe5\xb0\xbe\xe9\xa1\xb5</a>')
        result = re.search(pattern,page)
        if result:
            return result.group(1)
        else:
            return None
    #获取评论    
    def getContent(self,pageNum):
        page = self.getPage(pageNum)
        pattern = re.compile('class="d_post_content j_d_post_content.*?>(.*?)</div>',re.S)
        contents = []
        resultlist = re.findall(pattern,page)
        print '匹配条数：'
        print len(resultlist)
        if resultlist:
            for i in resultlist:
                content = '\n'+self.tool.replace(i)+'\n'
                print content +'*******', len(content)
                contents.append(content) 
            return contents
        else:
            return None
            
    def save(self,contents):
        filename = 'baidutieba'
        with open(filename,'a') as f1: 
            for i in contents:
                if self.floorTag:
                    b = '\n'+str(self.floor)+u"---------------------\n"
                    f1.write(b)
                    f1.write(i)
                    self.floor += 1
        
    def start(self,pageNum):
        title =  self.getTitle(pageNum)
        pagesum=  self.getPageNum()
        result = self.getContent(pageNum)
        if result is None:
            print '抓取内容为空'
        if pageNum ==None:
            print "URL已失效，请重试"
            return
        try:
            print '该帖子一共' +str(pageNum) +'页'
            self.floor = 1
            for i in result:
                print str(self.floor) +u"楼-----------------------------------"
                print i
                self.floor += 1
                self.save(result)
        except IOError,e:
            print "写入异常，原因:",e.message
        finally:
            print "任务完成"
class Mysql1:
    def __init__(self,contents):
        #try:
        self.conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='121186')
        print '成功连接'
        self.cursor = self.conn.cursor()
        print '游标对象成功返回'
        self.cursor.execute("drop database if exists baidutb")
        self.cursor.execute("create database baidutb default charset utf8")
        print '成功创建数据库'
        self.conn.select_db('baidutb')
        print '成功与数据库baidutb相连接'
        self.cursor.execute("create table log(id int,content text) default charset utf8")
        print '建立表格'
        values = []
        self.num = 1
        for i in contents:
        #    print '评论的编码方式:'
      #      print chardet.detect(i)
            values.append((self.num , i))
            self.num += 1
        self.cursor.execute("insert into log values(%s,%s)",(1,'测试'))
        print '编码方式:'
        print chardet.detect('测试')
        
        print '执行插入操作'
        self.conn.commit()
        print '提交'
        print '数据库已建好'
                #self.cursor.close()
                #self.conn.close()
        #except:
         #   self.conn.rollback()
          #  print '出错，发生回滚'
        #finally:
        self.cursor.close()
        self.conn.close()
    
    def mysqlSelect(self,databaseName):
        self.conn = MySQLdb.Connection(host='127.0.0.1',user='root',    passwd = '121186')
        self.cursor = self.conn.cursor()
        self.conn.select_db(databaseName)
        self.count = self.cursor.execute('select * from log')
        print '\n总共有 %s 条帖子\n' %self.count
        self.cursor.scroll(0,mode='absolute')
        results = self.cursor.fetchall()
        for res in results:
            print 'ID:%s Log Info:%s'% res
        self.cursor.close()
        self.conn.close()
        
baseURL = 'http://tieba.baidu.com/p/3138733512'
seeLZ = int(raw_input('请输入是否只看楼主:(1表示只看楼主;0均看):'))
floorTag =int(raw_input("请输入是否加入楼层分隔符：（1表示加入;0表示不加)"))
bdtb = BDTB(baseURL,seeLZ,floorTag)
pageNum = int(raw_input('请输入要查看的网页页码'))
bdtb.start(pageNum)
contents = bdtb.getContent(pageNum)
bdtb.save(contents)
mysql1 = Mysql1(contents)
#mysql1.mysqlSelect('baidutb')
