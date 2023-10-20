
# 修改数据库配置 
from tpf.db import reset_passwd

db_dict = {
                "report.username":"case",
                "report.password":"rootroot",
                "report.url":"192.168.67.220:1521/case",
                "case.username":"case",
                "case.password":"rootroot",
                "case.url":"192.168.67.220:1521/case",
                "ora3.username":"case",
                "ora3.password":"rootroot",
                "ora3.url":"192.168.67.220:1521/case",
                "db1.username":"automng",
                "db1.password":"Automng_123",
                "db1.host":"192.168.56.104",
                "db1.port":13301,
                "db1.database":"db1",
                "db1.charset":"utf8",
                "db2.username":"automng",
                "db2.password":"Automng_123",
                "db2.host":"192.168.56.104",
                "db2.port":13301,
                "db2.database":"db1",
                "db2.charset":"utf8",
    
            }

reset_passwd(db_dict=db_dict)



from tpf.db import DbConnect 
import pandas as pd

class Sql():
    
    create_acc="""
        CREATE TABLE if not exists acc(
            id bigint(11)    NOT NULL AUTO_INCREMENT primary key COMMENT '主键',
            c_acc bigint(19),
            c_datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '提交时间',
            index(c_acc));
        """


class MysqlInit(DbConnect):
    """mysql创库后初始化操作
    """
    def __init__(self) -> None:
        super().__init__()

    def create_fin(self):
        """创建记录表
        """
        with self.mysql() as connection:
            cursor = connection.cursor()
            cursor.execute(Sql.create_acc)
            connection.commit()
            cursor.close()

    
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

    def ora_table_stuct2(self,table_name):
        sql = """
        select column_name,data_type,DATA_LENGTH From all_tab_columns  
        where table_name=upper('{}')
        """.format(table_name)
        print(sql)
        res = ""
        col = []
        
        with self.oradb(name="case") as connection:
            cursor = connection.cursor()
            query = cursor.execute(sql)
            col = [c[0] for c in cursor.description]
            res = query.fetchall()
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

    def show_mysql_version2(self):
        sql = """
        SELECT VERSION()
        """
        print(sql)
        res = ""
        col = []
        with self.mysql(name="db2") as connection:
            cursor = connection.cursor()
            cursor.execute(sql)
             # 使用 fetchone() 方法获取单条数据.
            data = cursor.fetchone()
            print ("数据库连接成功,version =",data[0])
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
    
    def to_mysql(self):
        sql = """
        insert into db1.students(student_id,student_name)values(%s,%s);
        """
        value_list = [(100006,'扁鹊他大哥'),(100007,'扁鹊他二哥')];
        with self.mysql() as connection:
            cursor = connection.cursor()
            insert_row_num = cursor.executemany(sql,value_list)
            connection.commit()
            print ("影响行数=",insert_row_num)
            cursor.close()
            
        return insert_row_num 



mi = MysqlInit()

mi.show_mysql_version()
# mi.ora_table_stuct(table_name="students")
# mi.ora_table_stuct2(table_name="students")
