'''
功能：提供服务端的所有数据库操作
'''
import pymysql
import hashlib

SALT = '#&AID'  # 盐


class Database:
    def __init__(self, host='localhost',
                 port=3306, user='uroot',
                 password='123456',
                 charset='utf8',
                 database='dict'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.charset = charset
        self.database = database
        self.connect_db()  # 连接数据库

    def connect_db(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  password=self.password,
                                  charset=self.charset,
                                  database=self.database)

    def create_cursor(self):
        self.cur = self.db.cursor()

    # 关闭数据库
    def close_db(self):
        self.db.closse()
    # 注册操作
    def register(self, name, password):
        sql = 'select * from user where name="%s"' % (name)
        self.cur.execute(sql)
        r = self.cur.fetchone()  # 如果有查询结果则name
        if r:
            return False
        # 密码加密处理
        hash = hashlib.md5((name + SALT).encode())
        hash.update(password.encode())  # 算法加密
        password = hash.hexdigest()
        sql = "insert into user (name,password) values (%s,%s)"
        try:
            self.cur.execute(sql, [name, password])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False
    def login(self,name,password):
        hash = hashlib.md5((name + SALT).encode())
        hash.update(password.encode())  # 算法加密
        password = hash.hexdigest()
        # 数据库查找
        sql = 'select * from user where name="%s" and password="%s"' % (name,password)
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return True
        else:
            return False
    def query(self,word):
        sql = 'select mean from words where word="%s"'% (word)
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return r[0]
    def insert_history(self,name,word):
        sql="insert into hist (name,word) values (%s,%s)"
        try:
            self.cur.execute(sql,[name,word])
            self.db.commit()
        except Exception:
            self.db.rollback()

    def history(self,name):
        sql="select name,word,time from hist\
        where name = '%s' order by time desc limit 10"%name
        self.cur.execute(sql)
        return self.cur.fetchall()


