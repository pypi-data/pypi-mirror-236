import os 
import cx_Oracle as ora
import pymysql
import pandas as pd 

class DbConnect():
    def __init__(self) -> None:
        """数据库连接初始化,
        每次生产一个新的游标,游标是复用还是关闭由使用者决定
        """
        # 读取配置并加载完成连接初始化，外定方法返回句柄 
        # self.oradb = self.oracle()

        local_file_path=os.path.abspath(__file__)
        father_path=os.path.abspath(os.path.dirname(local_file_path)+os.path.sep+".")
        file_path = os.path.join(father_path,"db.db")
        self.db_file = file_path
        # self.db_file = "db.db"
        self._db_dict = {}
        if os.path.exists(self.db_file):
            with open(self.db_file,'r',encoding="utf-8") as f:
                db_dict = eval(f.read())
                self._db_dict = db_dict
        if len(self._db_dict)==0:
            print("没有配置数据库连接信息")
            
    def __enter__(self):
        # self.openedFile = open(self.filename, self.mode)
        # return self.openedFile
        pass 

    def __exit__(self, *unused):
        # self.openedFile.close()
        pass 
            
    def oradb(self, name="ora3"):
        """每次创建一个新游标,是复用还是关闭请自行判断 
        """
        db_dict = self._db_dict
        _casedb = None
        if len(db_dict) > 0 :
            if db_dict["case.username"]:
                try:
                    _casedb = ora.connect(db_dict["{}.username".format(name)],db_dict["{}.password".format(name)],db_dict["{}.url".format(name)])
                except:
               
               
                    error_msg = "{} db connect error".format(db_dict["{}.url".format(name)])
                    print(error_msg)
                    
            else:
                print("{} 连接信息不存在".format(name))

        return _casedb 

    def casedb(self):
        """每次创建一个新游标,是复用还是关闭请自行判断 
        """
        db_dict = self._db_dict
        _casedb = None
        if len(db_dict) > 0 :
            if db_dict["case.username"]:
                try:
                    _casedb = ora.connect(db_dict["case.username"],db_dict["case.password"],db_dict["case.url"])
                except:
               
               
                    error_msg = "{} case db connect error".format(db_dict["case.url"])
                    print(error_msg)
                    
            else:
                print("case 连接信息不存在")

        return _casedb 

    def reportdb(self):
        """每次创建一个新游标,是复用还是关闭请自行判断 
        """
        db_dict = self._db_dict
        _reportdb = None
        if len(db_dict) > 0 :
            if db_dict["report.username"]:
                try:
                    _reportdb = ora.connect(db_dict["report.username"],db_dict["report.password"],db_dict["report.url"])
                except:
                    error_msg = "{} report db connect error".format(db_dict["report.url"])
                    print(error_msg)
            else:
                print("report 连接信息不存在")
        

        return _reportdb 

    def mysql(self,name=None):
        """每次创建一个新游标,是复用还是关闭请自行判断 
        """
        db_dict = self._db_dict
        _mysql = None 
        if len(db_dict) > 0 :
            if name:
                if db_dict["{}.host".format(name)]:
                    try:
                        _mysql = pymysql.connect(host=db_dict["{}.host".format(name)],
                                    port=db_dict["{}.port".format(name)],
                                    user=db_dict["{}.username".format(name)],
                                    password=db_dict["{}.password".format(name)],
                                    database=db_dict["{}.database".format(name)],
                                    charset=db_dict["{}.charset".format(name)])

                    except  Exception as e:
                        error_msg = "{} {} mysql db connect error".format(db_dict["{}.host".format(name)],db_dict["{}.port".format(name)])
                        print(error_msg)
                        print(e)
                        
                else:
                    print("mysql {} 连接信息不存在".format(name))
                    
            else:
                if db_dict["db1.host"]:
                    try:
                        _mysql = pymysql.connect(host=db_dict["db1.host"],
                                    port=db_dict["db1.port"],
                                    user=db_dict["db1.username"],
                                    password=db_dict["db1.password"],
                                    database=db_dict["db1.database"],
                                    charset=db_dict["db1.charset"])

                    except:
                        error_msg = "{} mysql db connect error".format(db_dict["db1.host"])
                        print(error_msg)
                        
                else:
                    print("mysql 连接信息不存在")
                
        return _mysql
        
    def write(self,obj):
        ss = str(obj)
        with open(self.db_file,"w",encoding="utf-8") as f:
            f.write(ss)

class DbTools(DbConnect):
    def __init__(self) -> None:
        
        super().__init__()
        # self.resetPwd()
        # super().__init__() # 重置密码后再初始化一次 

    def resetPwd(self, db_dict=None):

        if db_dict :
            self.write(db_dict)
        else:
            db_dict = {
                "report.username":"case",
                "report.password":"rootroot",
                "report.url":"192.168.111.220:1521/case",
                "case.username":"case",
                "case.password":"rootroot",
                "case.url":"192.168.111.220:1521/case",
                "ora3.username":"case",
                "ora3.password":"rootroot",
                "ora3.url":"192.168.111.220:1521/case",
                "db1.username":"automng",
                "db1.password":"Automng_123",
                "db1.host":"192.168.56.104",
                "db1.port":13301,
                "db1.database":"db1",
                "db1.charset":"utf8",
            }
            self.write(db_dict)
    
    def ora_table_stuct(self,table_name):
        sql = """
        select column_name,data_type,DATA_LENGTH From all_tab_columns  
        where table_name=upper('{}')
        """.format(table_name)
        print(sql)
        res = ""
        col = []
        with self.reportdb() as connection:
            cursor = connection.cursor()
            query = cursor.execute(sql)
            col = [c[0] for c in cursor.description]
            res = query.fetchall()
            data = pd.DataFrame(res,columns=col) 
            cursor.close()
            # connection.commit()
        return data 
    
    def mysql_select(self, sql):
        res = ""
        col = []
        with self.mysql() as connection:
            cursor = connection.cursor()
            cursor.execute(sql)
            col = [c[0] for c in cursor.description]
            
            # res type list
            # res[0] type tuple 
            res = cursor.fetchall()   
            data = pd.DataFrame(res,columns=col) 
            cursor.close()
            # connection.commit()
        return data 

    def show_mysql_version(self):
        sql = """
        SELECT VERSION()
        """
        print(sql)
        res = ""
        col = []
        with self.mysql() as connection:
            cursor = connection.cursor()
            cursor.execute(sql)
             # 使用 fetchone() 方法获取单条数据.
            data = cursor.fetchone()
            print ("数据库连接成功,version =",data[0])
            cursor.close()
            # connection.commit()
        return data 

def reset_passwd(db_dict):
    dt = DbTools()
    dt.resetPwd(db_dict=db_dict)
        
        
if __name__=="__main__":
    print("----------big table -------")

