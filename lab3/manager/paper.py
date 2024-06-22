from itertools import chain
import re
import string
import pymysql
from datetime import datetime, date
# create table publish_paper
# (
#    job_number           char(5) not null,
#    serial_number        int not null,
#    ranking                 int,
#    corresponding_author bool,
#    primary key (job_number, serial_number)
# );

# create table paper
# (
#    serial_number        int not null,
#    paper_name           char(255),
#    publish_source       char(255),
#    publish_year         date,
#    type                 int,
#    level                int,
#    primary key (serial_number)
# );
def is_number(s):
    try: 
        float(s)  
        return True
    except ValueError:
        pass
    try:
        import unicodedata 
        unicodedata.numeric(s)    
        return True
    except (TypeError, ValueError):
        pass
    return False

class paper:

    def __init__(self) -> None:
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='20040501',
                                  database='lab3')

    def check_paper(self, data: dict):
        if not str.isdigit(data['serial_number']):
            raise Exception('error: serial_number format')
        elif not str.isalnum(data['paper_name']):
            raise Exception('error: paper_name format')
        elif not str.isalnum(data['publish_source']):
            raise Exception('error: publish_source format')
        elif re.match("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", data['publish_year']) is None:
            raise Exception('error: publish_year format')
        elif not str.isdigit(data['type']):
            raise Exception('error: type format')
        elif not str.isdigit(data['level']):
            raise Exception('error: level format')
        elif "#" in data['paper_name'] or ";" in data['paper_name']:
            raise Exception('error: paper_name format')
        elif "#" in data['publish_source'] or ";" in data['publish_source']:
            raise Exception('error: publish_source format')

    def _check(self, data: dict):
        if not (str.isalnum(data['job_number']) and len(data['job_number']) <= 5):
            raise Exception('error: job_number format')
        elif not str.isdigit(data['serial_number']):
            raise Exception('error: serial_number format')
        elif not str.isdigit(data['ranking']):
            raise Exception('error: ranking format')
        elif not isinstance(data['corresponding_author'], bool):
            raise Exception('error: corresponding_author format')

    # 插入论文
    def insert(self, data: dict):
        self.check_paper(data)
        cursor = self.db.cursor()
        sql1 = "INSERT INTO paper VALUES(%s, %s, %s, %s, %s, %s)"
        try:
            cursor.execute(sql1, (data['serial_number'], data['paper_name'], data['publish_source'], data['publish_year'], data['type'], data['level']))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise Exception(e)
        cursor.close()

    def insert_publish_paper(self, data: dict):
        self._check(data)
        cursor = self.db.cursor()
        sql2 = "INSERT INTO publish_paper VALUES(%s, %s, %s, %s)"
        try:
            cursor.execute(sql2, (data['job_number'], data['serial_number'], data['ranking'], data['corresponding_author']))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise Exception(e)
        cursor.close()

    # 删除论文
    def delete(self, serial_number):
        cursor = self.db.cursor()
        sql1 = "DELETE FROM paper WHERE serial_number = %s"
        sql2 = "DELETE FROM publish_paper WHERE serial_number = %s" 
        try:    
            cursor.execute(sql2, (serial_number))
            cursor.execute(sql1, (serial_number))
            self.db.commit()
        except:
            self.db.rollback()
            raise Exception('error: serial_number not exist')
        cursor.close()

    # 更新论文
    def update_paperself(self, data: dict):
        self.check_paper(data)
        cursor = self.db.cursor()
        print(data)

        # 查询是否存在条目的 SQL 语句
        check_sql1 = "SELECT COUNT(*) FROM paper WHERE serial_number = %s"
        check_sql2 = "SELECT COUNT(*) FROM publish_paper WHERE job_number = %s AND serial_number = %s"

        # 更新或插入的 SQL 语句
        update_sql1 = "UPDATE paper SET paper_name = %s, publish_source = %s, publish_year = %s, type = %s, level = %s WHERE serial_number = %s"
        insert_sql1 = "INSERT INTO paper (serial_number, paper_name, publish_source, publish_year, type, level) VALUES (%s, %s, %s, %s, %s, %s)"
        
        update_sql2 = "UPDATE publish_paper SET ranking = %s, corresponding_author = %s WHERE job_number = %s AND serial_number = %s"
        insert_sql2 = "INSERT INTO publish_paper (job_number, serial_number, ranking, corresponding_author) VALUES (%s, %s, %s, %s)"
    
        try:
            # 检查并插入或更新 paper 表
            cursor.execute(check_sql1, (data['serial_number'],))
            if cursor.fetchone()[0] == 0:
                cursor.execute(insert_sql1, (data['serial_number'], data['paper_name'], data['publish_source'], data['publish_year'], data['type'], data['level']))
            else:
                cursor.execute(update_sql1, (data['paper_name'], data['publish_source'], data['publish_year'], data['type'], data['level'], data['serial_number']))
            
            # 检查并插入或更新 publish_paper 表
            cursor.execute(check_sql2, (data['job_number'], data['serial_number']))
            if cursor.fetchone()[0] == 0:
                cursor.execute(insert_sql2, (data['job_number'], data['serial_number'], data['ranking'], data['corresponding_author']))
            else:
                cursor.execute(update_sql2, (data['ranking'], data['corresponding_author'], data['job_number'], data['serial_number']))
            
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise Exception('error: update or insert paper data failed') from e
        finally:
            cursor.close()

    # 按论文编号查询
    def search_serial_number(self, serial_number):
        cursor = self.db.cursor()
        sql = "SELECT * FROM paper WHERE serial_number = %s"
        cursor.execute(sql, (serial_number))
        result = dict(
            zip([x[0] for x in cursor.description],
                [x for x in cursor.fetchone()]))
        cursor.close()
        return result

    # 按论文名称查询
    def search_paper_name(self, paper_name: string):

        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))
        
        cursor = self.db.cursor()
        sql = "SELECT * FROM paper WHERE paper_name = %s"
        cursor.execute(sql, (paper_name,))
        result = list(map(result2dict, cursor.fetchall()))
        cursor.close()
        return result
    
    # 按教师工号查询发表的论文
    def search_job_number(self, job_number: string):
        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))
        
        cursor = self.db.cursor()
        sql = "SELECT * FROM publish_paper WHERE job_number=%s"
        cursor.execute(sql, (job_number,))
        result = list(map(result2dict, cursor.fetchall()))
        cursor.close()

        for i in range(len(result)):
            result1 = self.search_serial_number(result[i]['serial_number'])
            result[i]['paper_name'] = result1['paper_name']
            result[i]['publish_source'] = result1['publish_source']
            result[i]['publish_year'] = result1['publish_year']
            result[i]['type'] = result1['type']
            result[i]['level'] = result1['level']
        return result
    
    def search_jobnumber_year(self,job_number,start_year,end_year):

        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))

        cursor = self.db.cursor()
        sql = "SELECT * FROM paper,publish_paper WHERE paper.serial_number = publish_paper.serial_number  and publish_paper.job_number = %s"
        cursor.execute(sql, (job_number,))
        result = list(map(result2dict, cursor.fetchall()))
        # print(result)
        result = list(filter(lambda x: ((compare_date_string(x['publish_year'],start_year,0) == 0 or compare_date_string(x['publish_year'],start_year,0)== 2) or (compare_date_string(x['publish_year'],end_year,1) == 1 or compare_date_string(x['publish_year'],end_year,1) == 2)), result))
        cursor.close()
        # print(result)
        return result
    

        

    # 按照年份查询
    def search_year(self, year: string):
        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))
        
        cursor = self.db.cursor()
        sql = "SELECT * FROM paper WHERE publish_year = %s"
        cursor.execute(sql, (year,))
        result = list(map(result2dict, cursor.fetchall()))
        cursor.close()
        return result
    
    # 按照论文类型查询
    def search_type(self, type: string):
        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))
        
        cursor = self.db.cursor()
        sql = "SELECT * FROM paper WHERE type=%s"
        cursor.execute(sql, (type,))
        result = list(map(result2dict, cursor.fetchall()))
        cursor.close()
        return result
    
    # 按照论文来源查询
    def search_source(self, publish_source: string):
        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))
        
        cursor = self.db.cursor()
        sql = "SELECT * FROM paper WHERE publish_source=%s"
        cursor.execute(sql, (publish_source,))
        result = list(map(result2dict, cursor.fetchall()))
        cursor.close()
        return result
    
    # 按论文编号查找教师信息
    def search_teacher(self, serial_number: string):
        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))
        
        def search_id(id: string):
            cursor = self.db.cursor()
            sql = "SELECT * FROM teacher WHERE job_number=%s"
            cursor.execute(sql, (id,))
            result = dict(
                zip([x[0] for x in cursor.description],
                    [x for x in cursor.fetchone()]))
            cursor.close()
            return result
    
        cursor = self.db.cursor()
        sql = "SELECT * FROM publish_paper WHERE serial_number=%s"
        cursor.execute(sql, (serial_number,))
        result = list(map(result2dict, cursor.fetchall()))
        cursor.close()
        for i in range(len(result)):
            result1 = search_id(result[i]['job_number'])
            result[i]['name'] = result1['name']
            result[i]['sex'] = result1['sex']
            result[i]['job_title'] = result1['job_title']
        return result

def compare_date_string(date_obj, date_str,startorend):
    try:
        # print(type(date_str),type(date_obj))
        # 将字符串转换为 datetime.date 对象
        date_format = "%Y-%m-%d"  # 假设字符串的日期格式是 'YYYY-MM-DD'
        if startorend == 0:
            date_str = date_str + '-01-01'
        else:
            date_str = date_str + '-12-31'

        # print(date_str)
        # print(date_obj)
        parsed_date = datetime.strptime(date_str, date_format).date()
        # print('parsed_date',parsed_date)
        # 比较两个日期
        if date_obj > parsed_date:
            # print(date_obj,parsed_date,'0')
            return 0
        elif date_obj < parsed_date:
            # print(date_obj,parsed_date,'1')
            return 1
        else:
            return 2
    except ValueError:
        return "Invalid date string format. Please use 'YYYY'."