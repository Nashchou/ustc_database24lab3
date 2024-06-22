from itertools import chain
import re
import string
import pymysql
from datetime import datetime, date

# create table charge_project
# (
#    job_number           char(5) not null,
#    project_number       char(255) not null,
#    ranking                 int,
#    own_money            float,
#    primary key (job_number, project_number)
# );
# create table project
# (
#    project_number       char(255) not null,
#    project_name         char(255),
#    project_source       char(255),
#    project_type         int,
#    total_budget         float,
#    start_year           date,
#    end_year             date,
#    primary key (project_number)
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
    
class project:

    def __init__(self) -> None:
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='20040501',
                                  database='lab3')
    def check_project(self, data: dict):
        if not str.isalnum(data['project_number']):
            raise Exception('error: project_number format')
        elif not str.isdigit(data['project_type']):
            raise Exception('error: project_type format')
        elif not str.isalnum(data['project_name']):
            raise Exception('error: project_name format')
        elif not str.isalnum(data['project_source']):
            raise Exception('error: project_source format')        
        elif re.match("^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
                        data['start_year']) == None:
                raise Exception('error: start_year format')
        elif re.match("^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
                        data['end_year']) == None:
                raise Exception('error: end_year format')
        elif "#" in data['project_name'] or ";" in data['project_name']:
            raise Exception('error: project_name format')
        elif "#" in data['project_source'] or ";" in data['project_source']:
            raise Exception('error: project_source format')

    def _check(self, data: dict):
        if not (str.isalnum(data['job_number'])
                and len(data['job_number'])  <= 5):
            raise Exception('error: job_number format')
        elif not str.isalnum(data['project_number']):
            raise Exception('error: project_number format')
        elif not str.isdigit(data['ranking']):
            raise Exception('error: ranking format')
        elif not is_number(data['own_money']):
            raise Exception('error: own_money format')
        elif not is_number(data['total_budget']):
            raise Exception('error: total_budget format')
        elif not str.isdigit(data['project_type']):
            raise Exception('error: project_type format')
        elif not str.isalnum(data['project_name']):
            raise Exception('error: project_name format')
        elif not str.isalnum(data['project_source']):
            raise Exception('error: project_source format')        
        elif re.match("^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
                        data['start_year']) == None:
                raise Exception('error: start_year format')
        elif re.match("^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
                        data['end_year']) == None:
                raise Exception('error: end_year format')
        elif "#" in data['project_name'] or ";" in data['project_name']:
            raise Exception('error: project_name format')
        elif "#" in data['project_source'] or ";" in data['project_source']:
            raise Exception('error: project_source format')
        
    # 插入项目
    def insert(self, data: dict):
        self.check_project(data)
        cursor = self.db.cursor()
        sql1 = "INSERT INTO project VALUES(%s,%s,%s,%s,%s,%s,%s)"
        # sql2 = "INSERT INTO charge_project VALUES(%s,%s,%s,%s)"
        try:
            cursor.execute(sql1,(data['project_number'], data['project_name'], data['project_source'], data['project_type'], data['total_budget'], data['start_year'], data['end_year']))
            # cursor.execute(sql2,(data['job_number'], data['project_number'], data['ranking'], data['own_money']))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise Exception(e)
        cursor.close()


    def insert_charge_project(self,data: dict):
        self._check(data)
        cursor = self.db.cursor()
        sql2 = "INSERT INTO charge_project VALUES(%s,%s,%s,%s)"
        try:
            cursor.execute(sql2,(data['job_number'], data['project_number'], data['ranking'], data['own_money']))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise Exception(e)
        cursor.close()

    # 删除项目
    def delete(self, project_number: string):
        
        print(type(project_number),len(project_number))
        cursor = self.db.cursor()
        sql1 = "DELETE FROM project WHERE project_number = %s"
        sql2 = "DELETE FROM charge_project WHERE project_number = %s" 
        try:    
            cursor.execute(sql2,(project_number))
            cursor.execute(sql1,(project_number))
            self.db.commit()
        except:
            self.db.rollback()
            raise Exception('error: project_number not exist')
        cursor.close()

    # 更新项目
    def update_projectself(self, data: dict):
        self.check_project(data)
        cursor = self.db.cursor()
        print(data)

        # 查询是否存在条目的 SQL 语句
        check_sql1 = "SELECT COUNT(*) FROM project WHERE project_number = %s"
        check_sql2 = "SELECT COUNT(*) FROM charge_project WHERE job_number = %s AND project_number = %s"

        # 更新或插入的 SQL 语句
        update_sql1 = "UPDATE project SET project_name = %s, project_source = %s, project_type = %s, start_year = %s, end_year = %s,total_budget = %s WHERE project_number = %s"
        insert_sql1 = "INSERT INTO project VALUES(%s,%s,%s,%s,%s,%s,%s)"
        
        update_sql2 = "UPDATE charge_project SET ranking = %s, own_money = %s WHERE job_number = %s AND project_number = %s"
        insert_sql2 = "INSERT INTO charge_project (ranking, own_money, job_number, project_number) VALUES (%s, %s, %s, %s)"

        print(data['project_type'])
        try:
            # 检查并插入或更新 project 表
            cursor.execute(check_sql1, (data['project_number'],))
            if cursor.fetchone()[0] == 0:
                cursor.execute(insert_sql1,(data['project_number'], data['project_name'], data['project_source'], data['project_type'], data['total_budget'], data['start_year'], data['end_year']))
            else:
                cursor.execute(update_sql1, (data['project_name'], data['project_source'], data['project_type'], data['start_year'], data['end_year'] ,data['total_budget'],data['project_number']))
            
            # 检查并插入或更新 charge_project 表
            cursor.execute(check_sql2, (data['job_number'], data['project_number']))
            if cursor.fetchone()[0] == 0:
                cursor.execute(insert_sql2, (data['ranking'], data['own_money'], data['job_number'], data['project_number']))
            else:
                cursor.execute(update_sql2, (data['ranking'], data['own_money'], data['job_number'], data['project_number']))
            
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise Exception('error: update or insert project data failed') from e
        finally:
            cursor.close()

    def update(self, data: dict):
        self._check(data)
        cursor = self.db.cursor()
        print(data)
        sql1 = "UPDATE project SET project_name = %s, project_source = %s, project_type = %s, total_budget = %s, start_year = %s, end_year = %s WHERE project_number = %s"
        sql2 = "UPDATE charge_project SET ranking = %s, own_money = %s WHERE job_number = %s AND project_number = %s"
        try:
            cursor.execute(sql1,(data['project_name'], data['project_source'], data['project_type'], data['total_budget'], data['start_year'], data['end_year'], data['project_number']))
            cursor.execute(sql2,(data['ranking'], data['own_money'], data['job_number'], data['project_number']))
            self.db.commit()
        except:
            self.db.rollback()
            raise Exception('error: update project_number format is wrong')
        cursor.close()
    # 按项目编号查询
    def search_project_number(self, project_number: string):
        cursor = self.db.cursor()
        sql = "SELECT * FROM project WHERE project_number = %s"
        cursor.execute(sql, (project_number)) 
        result = dict(
            zip([x[0] for x in cursor.description],
                [x for x in cursor.fetchone()]))
        cursor.close()
        return result
    

    # 按项目名称查询

    def search_project_name(self, project_name: string):

        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))
        
        cursor = self.db.cursor()
        sql = "SELECT * FROM project WHERE project_name = %s"
        cursor.execute(sql, (project_name))
        result = list(map(result2dict, cursor.fetchall()))
        cursor.close()
        return result
    
    # 按教师工号查询负责了那些project
    def search_job_number(self, job_number: string):
        # 一个教师可能负责了多个project
                
            
        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))
        
        cursor = self.db.cursor()
        sql = "SELECT * FROM charge_project WHERE job_number=%s"
        cursor.execute(sql, (job_number))
        result = list(map(result2dict, cursor.fetchall()))
        cursor.close()
  

        for i in range(len(result)):
            result1 = self.search_project_number(result[i]['project_number'])
            result[i]['project_name'] = result1['project_name']
            result[i]['project_source'] = result1['project_source']
            result[i]['project_type'] = result1['project_type']
            result[i]['total_budget'] = result1['total_budget']
            result[i]['start_year'] = result1['start_year']
            result[i]['end_year'] = result1['end_year']
        return result

        

    # 按照年份查询
    def search_year(self, year: string):
        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))
        
        cursor = self.db.cursor()
        sql = "SELECT * FROM project WHERE start_year = %s OR end_year = %s"
        cursor.execute(sql, (year, year))
        result = list(map(result2dict, cursor.fetchall()))
        cursor.close()
        return result
    
    # 按照项目类型查询
    def search_type(self, project_type: string):
        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))
        
        cursor = self.db.cursor()
        sql = "SELECT * FROM project WHERE project_type=%s"
        cursor.execute(sql, (project_type))
        result = list(map(result2dict, cursor.fetchall()))
        cursor.close()
        return result
    
    # 按照项目来源查询
    def search_source(self, project_source: string):
        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))
        
        cursor = self.db.cursor()
        sql = "SELECT * FROM project WHERE project_source=%s"
        cursor.execute(sql, (project_source))
        result = list(map(result2dict, cursor.fetchall()))
        cursor.close()
        return result
    
    # 按照项目号来找老师信息
    def search_teacher(self, project_number: string):
        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))
        

        def search_id(id: string):
            cursor = self.db.cursor()
            sql = "SELECT * FROM teacher WHERE job_number=%s"
            cursor.execute(sql, (id)) 
            result = dict(
                zip([x[0] for x in cursor.description],
                    [x for x in cursor.fetchone()]))
            cursor.close()
            return result
    
        cursor = self.db.cursor()
        sql = "SELECT * FROM charge_project WHERE project_number=%s"
        cursor.execute(sql, (project_number))
        result = list(map(result2dict, cursor.fetchall()))
        cursor.close()
        for i in range(len(result)):
            result1 = search_id(result[i]['job_number'])
            result[i]['name'] = result1['name']
            result[i]['sex'] = result1['sex']
            result[i]['job_title'] = result1['job_title']
        return result
    
    
    def search_jobnumber_year(self,job_number,start_year,end_year):
        result = self.search_job_number(job_number)
        # result = list(filter(lambda x: x['start_year'] >= start_year and x['end_year'] <= end_year, result))
        # print(result)
        result = list(filter(lambda x: ((compare_date_string(x['start_year'],start_year,0) == 0 or compare_date_string(x['start_year'],start_year,0)== 2) or (compare_date_string(x['end_year'],end_year,1) == 1 or compare_date_string(x['end_year'],end_year,1) == 2)), result))
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

    

    