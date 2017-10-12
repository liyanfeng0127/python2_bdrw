#coding:utf-8
from os.path import dirname  #获取文件路径中的目录
from sqlalchemy import create_engine,Column,String,Date,Text,exc, orm
from sqlalchemy.ext.declarative import  declarative_base

Base = declarative_base()
#创建URL访问记录表
class Urls_Seen(Base):
    __tablename__ = 'urls_seen'
    url = Column(String(128),primary_key=True)
    def __str__(self):
        return self.url

class Jobs(Base):
    __tablename__ = 'jobs'
    id = Column(String(32),primary_key=True)
    CompanyName = Column(String(64))
    JobName = Column(String(64))
    Salary = Column(String(32))
    ReleaseDate = Column(Date())
    RecruitingNumbers =Column(String(16))
    WorkExperience = Column(String(32))
    WorkPlace = Column(String(32))
    EducationalRequirements = Column(String(16))
    JobCategory = Column(String(32))
    JobDescription = Column(Text())
    def __str__(self):
        return self.id

#创建URL队列表
class Urls_Queue(Base):
    __tablename__ = 'urls_queue'
    url = Column(String(128),primary_key=True)

    def __str__(self):
        return self.url

#创建HTML页面表
class HTMLS(Base):
    __tablename__ = 'htmls'
    url = Column(String(128),primary_key=True)
    html = Column(Text())


#设置数据库
DBNAME = 'practice'
dsn = 'mysql://root:071659@localhost/%s?charset=utf8'% DBNAME
class SQLCache(object):
    def __init__(self,dsn=dsn):
        try:
            eng = create_engine(dsn)
        except ImportError:
            raise RuntimeError()
        try:
            eng.connect()
        except exc.OperationalError:
            eng = create_engine(dirname(dsn))
            eng.execute('CREATE DATABASE %s' % DBNAME).close()
            eng = create_engine(dsn)

        Session = orm.sessionmaker(bind=eng)
        self.__class__.ses = Session()
        self.__class__.Eng = eng
        '''
        self.urls_seen = Urls_Seen.__table__
        self.url_htmls = HTMLS.__table__
        '''


    def finish(self):
        self.ses.connection().close()






    def __getattr__(self, attr):
        return getattr(self.table, attr)




class SQLQueue(SQLCache):
    def __init__(self):
        self.table=self.urls_queue = Urls_Queue.__table__
        self.eng = self.table.metadata.bind = self.__class__.Eng
        self.ses = self.__class__.ses
        try:
            self.table.create()
        except:
            pass
    def delete_all(self):
        self.ses.query(Urls_Queue).delete()

    def append(self, str):
        try:
            self.ses.add(Urls_Queue(url=str))
            self.ses.commit()
        except Exception,e:
            self.ses.rollback()
            #print "AppendError:",e
            pass


    def pop(self):
        url = self.ses.query(Urls_Queue).first()
        self.ses.delete(url)
        self.ses.commit()
        return url.url
    def __len__(self):
        urls = self.ses.query(Urls_Queue).count()
        return urls

class Seen(SQLCache):
    def __init__(self):
        self.table=self.seen = Urls_Seen.__table__
        self.eng = self.table.metadata.bind = self.__class__.Eng
        self.ses = self.__class__.ses
        try:
            self.table.create()
        except:
            pass

    def delete_all(self):
        self.ses.query(Urls_Seen).delete()

    def append(self, str):
        try:
            self.ses.add(Urls_Seen(url=str))
            self.ses.commit()
        except Exception,e:
            self.ses.rollback()
            #print "AppendError:",e
            pass

    def pop(self):
        url = self.ses.query(Urls_Seen).first()
        self.ses.delete(url)
        self.ses.commit()
        return url.url

    def __contains__(self, url):
        o_urls = self.ses.query(Urls_Seen).all()
        return  url in [o_url.url for o_url in o_urls]


class HTMLCache(SQLCache):
    def __init__(self):
        self.table=self.htmls = HTMLS.__table__
        self.eng = self.table.metadata.bind = self.__class__.Eng
        self.ses = self.__class__.ses
        try:
            self.table.create()
        except:
            pass




class JobsCache(SQLCache):
    def __init__(self):
        self.table=self.jobs = Jobs.__table__
        self.eng = self.table.metadata.bind = self.__class__.Eng
        self.ses = self.__class__.ses
        try:
            self.table.create()
        except:
            pass

    def append(self, id, CompanyName, JobName, Salary, ReleaseDate, WorkExperience,RecruitingNumbers, WorkPlace,
               EducationalRequirements, JobCategory, JobDescription):
        try:
            self.ses.add(Jobs(id=id,CompanyName=CompanyName,JobName=JobName,
                              Salary=Salary,ReleaseDate=ReleaseDate,WorkExperience=WorkExperience,
                              RecruitingNumbers = RecruitingNumbers,
                              WorkPlace=WorkPlace,EducationalRequirements=EducationalRequirements,
                              JobCategory=JobCategory,JobDescription=JobDescription))
            self.ses.commit()
        except Exception,e:
            self.ses.rollback()
            print "JobAppendError:",e

    def delete_all(self):
        self.table.drop()




def main():
    try:
        orm = SQLCache(dsn)
    except RuntimeError:
        print('\n ERROR: %r not supported,exit2' % dsn)
        return
    sqlqueue = SQLQueue()
    #orm.drop(checkfirst=True)
    #orm.create()
    #orm.insert()
    #orm.finish()
if __name__ == '__main__':
    main()