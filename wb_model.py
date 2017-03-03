#-*-coding:utf-8 -*-
#微博用户：详细的个人信息数据表

from sqlalchemy import Column,Integer,String,Text,DateTime,Date,Float,Boolean,ForeignKey,Index
from  sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import datetime

Base = declarative_base()
DATABASE_URL = "mysql://root:121186@localhost/weibo1?charset=utf8&use_unicode=0"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind = engine)
session = Session()

#用户详细信息
class Target(Base):
    '''
    用户详细信息
    '''
    __tablename__ = 'weibo_target'
    id = Column(Integer,primary_key=True,autoincrement=True)
    url = Column(String(512))
#    name =Column(u"登录名",String(32)) 
    nickname =Column(u'昵称',String(32))
    realname = Column(u"真实姓名",String(32))
    city = Column(u'所在地',String(32))
    sex = Column(u'性别',String(32))
    #性取向
    sextrend = Column(u"性取向",String(32))
    #感情状况
    love =Column(u"感情状况",String(32))
    #生日
    birth =Column(u"生日",String(32))
    #血型
    blood =Column(u"血型",String(16))
    #博客地址
    blog = Column(u"博客地址",String(32))
    #个性域名
    domain_name = Column(u"个性域名",String(32))
    #简介
    intro = Column(u"简介",Text)
    #注册时间
    regis_time = Column(u"注册时间",String(32))
    #联系信息
    msn = Column(u'MSN',String(32))
    qq = Column(u'QQ',String(32))
    email = Column(u'Email',String(32))

    #工作信息
    company = Column(u'工作信息',String(512))
    #教育信息
    edu = Column(u'教育背景',String(512))
    #标签
    label = Column(u'标签',String(512))




if __name__ == '__main__':
    Base.metadata.create_all(engine)
    print 'Done!'





