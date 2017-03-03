#-*- coding:utf-8 -*-
#导入相关模块  
import MySQLdb  
  
#建立和mysql数据库的连接  
dbconn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='121186')  
#获取游标  
cursor = dbconn.cursor()  
#执行SQL,创建一个数据库  
cursor.execute("drop database if exists test")  
cursor.execute("create database test")  
#选择连接哪个数据库  
dbconn.select_db('test')  
#引入异常处理  
try:  
    #执行SQL,创建一个表  
    cursor.execute("create table log(id int,message varchar(50))")  
    #插入一条记录  
    value = [0,"Log Information ID is:0"]  
    cursor.execute("insert into log values(%s,%s)",value)  
    #插入多条记录  
    values = []  
    for i in range(1,11):  
        values.append((i,'Log Information ID is:' + str(i)))  
    cursor.executemany("insert into log values(%s,%s)",values)  
    #提交修改                                 
    dbconn.commit()  
except:  
    #如果执行SQL语句有错，则回滚!  (回滚：如果仅执行了execute()而没有执行commit()，则回滚到事务未执行的初始状态）
    dbconn.rollback()  
#关闭游标连接,释放资源  
cursor.close()  
#关闭连接 
dbconn.close()  
