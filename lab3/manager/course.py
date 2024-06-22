from itertools import chain
import re
import string
import pymysql
from datetime import datetime, date
# create table course
# (
#    course_number        char(255) not null,
#    course_name          char(255),
#    hours                int,
#    course_nature        int,
#    primary key (course_number)
# );

# create table teach_course
# (
#    job_number           char(5) not null,
#    course_number        char(255) not null,
#    year                 int,
#    term                 int,
#    class_hour           int,
#    primary key (job_number, course_number)
# );c

class course:

    def __init__(self) -> None:
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='20040501',
                                  database='lab3')

    def check_course(self, data: dict):
        if not str.isalnum(data['course_number']):
            raise Exception('error: course_number format')
        elif not str.isalnum(data['course_name']):
            raise Exception('error: course_name format')
        elif not str.isdigit(data['hours']):
            raise Exception('error: hours format')
        elif not str.isdigit(data['course_nature']):
            raise Exception('error: course_nature format')
        elif "#" in data['course_name'] or ";" in data['course_name']:
            raise Exception('error: course_name format')

    def _check_teach_course(self, data: dict):
        if not (str.isalnum(data['job_number']) and len(data['job_number']) <= 5):
            raise Exception('error: job_number format')
        elif not str.isalnum(data['course_number']):
            raise Exception('error: course_number format')
        elif not str.isdigit(data['year']):
            raise Exception('error: year format')
        elif not str.isdigit(data['term']):
            raise Exception('error: term format')
        elif not str.isdigit(data['class_hour']):
            raise Exception('error: class_hour format')

    # 插入课程
    def insert_course(self, data: dict):
        self.check_course(data)
        cursor = self.db.cursor()
        sql = "INSERT INTO course VALUES(%s, %s, %s, %s)"
        try:
            cursor.execute(sql, (data['course_number'], data['course_name'], data['hours'], data['course_nature']))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise Exception(e)
        cursor.close()

    def insert_teach_course(self, data: dict):
        self._check_teach_course(data)
        cursor = self.db.cursor()
        sql = "INSERT INTO teach_course VALUES(%s, %s, %s, %s, %s)"
        try:
            cursor.execute(sql, (data['job_number'], data['course_number'], data['year'], data['term'], data['class_hour']))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise Exception(e)
        cursor.close()

    # 删除课程
    def delete_course(self, course_number):
        cursor = self.db.cursor()
        sql1 = "DELETE FROM course WHERE course_number = %s"
        sql2 = "DELETE FROM teach_course WHERE course_number = %s" 
        try:    
            cursor.execute(sql2, (course_number,))
            cursor.execute(sql1, (course_number,))
            self.db.commit()
        except:
            self.db.rollback()
            raise Exception('error: course_number not exist')
        cursor.close()

    # 更新课程
    def update_course(self, data: dict):
        self.check_course(data)
        cursor = self.db.cursor()

        # 查询是否存在条目的 SQL 语句
        check_sql = "SELECT COUNT(*) FROM course WHERE course_number = %s"

        # 更新或插入的 SQL 语句
        update_sql = "UPDATE course SET course_name = %s, hours = %s, course_nature = %s WHERE course_number = %s"
        insert_sql = "INSERT INTO course (course_number, course_name, hours, course_nature) VALUES (%s, %s, %s, %s)"
    
        try:
            # 检查并插入或更新 course 表
            cursor.execute(check_sql, (data['course_number'],))
            if cursor.fetchone()[0] == 0:
                cursor.execute(insert_sql, (data['course_number'], data['course_name'], data['hours'], data['course_nature']))
            else:
                cursor.execute(update_sql, (data['course_name'], data['hours'], data['course_nature'], data['course_number']))
            
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise Exception('error: update or insert course data failed') from e
        finally:
            cursor.close()

    # 按课程编号查询
    def search_course_number(self, course_number):
        cursor = self.db.cursor()
        sql = "SELECT * FROM course WHERE course_number = %s"
        cursor.execute(sql, (course_number,))
        result = dict(
            zip([x[0] for x in cursor.description],
                [x for x in cursor.fetchone()]))
        cursor.close()
        return result

    # 按课程名称查询
    def search_course_name(self, course_name: string):

        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))
        
        cursor = self.db.cursor()
        sql = "SELECT * FROM course WHERE course_name = %s"
        cursor.execute(sql, (course_name,))
        result = list(map(result2dict, cursor.fetchall()))
        cursor.close()
        return result
    
    # 按教师工号查询教授的课程
    def search_teach_course(self, job_number: string):
        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))
        
        cursor = self.db.cursor()
        sql = "SELECT * FROM teach_course WHERE job_number=%s"
        cursor.execute(sql, (job_number,))
        result = list(map(result2dict, cursor.fetchall()))
        cursor.close()

        for i in range(len(result)):
            result1 = self.search_course_number(result[i]['course_number'])
            result[i]['course_name'] = result1['course_name']
            result[i]['hours'] = result1['hours']
            result[i]['course_nature'] = result1['course_nature']
        return result

    # 按照年份查询课程
    def search_course_year(self, year: string):
        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))
        
        cursor = self.db.cursor()
        sql = "SELECT * FROM teach_course WHERE year = %s"
        cursor.execute(sql, (year,))
        result = list(map(result2dict, cursor.fetchall()))
        cursor.close()
        return result
    
    # 按照课程性质查询
    def search_course_nature(self, course_nature: string):
        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))
        
        cursor = self.db.cursor()
        sql = "SELECT * FROM course WHERE course_nature=%s"
        cursor.execute(sql, (course_nature,))
        result = list(map(result2dict, cursor.fetchall()))
        cursor.close()
        return result
    
    # 按教师工号和课程编号查询课程信息
    def search_teacher_course(self, job_number: string, course_number: string):
        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))
        
        cursor = self.db.cursor()
        sql = "SELECT * FROM teach_course WHERE job_number=%s AND course_number=%s"
        cursor.execute(sql, (job_number, course_number))
        result = list(map(result2dict, cursor.fetchall()))
        cursor.close()
        for i in range(len(result)):
            result1 = self.search_course_number(result[i]['course_number'])
            result[i]['course_name'] = result1['course_name']
            result[i]['hours'] = result1['hours']
            result[i]['course_nature'] = result1['course_nature']
        return result
    
    def search_jobnumber_year(self,job_number,start_year,end_year):
        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))
        
        cursor = self.db.cursor()
        sql = "SELECT * FROM teach_course WHERE job_number=%s"
        cursor.execute(sql, (job_number,))
        result = list(map(result2dict, cursor.fetchall()))
        # result = list(filter(lambda x: x['start_year'] >= start_year and x['end_year'] <= end_year, result))
        # print(result)
        result = list(filter(lambda x: ((compare_date_string(x['year'],start_year,0) == 0 or compare_date_string(x['year'],start_year,0)== 2) or (compare_date_string(x['year'],end_year,1) == 1 or compare_date_string(x['year'],end_year,1) == 2)), result))
        cursor.close()
        for i in range(len(result)):
            result1 = self.search_course_number(result[i]['course_number'])
            result[i]['course_name'] = result1['course_name']
            result[i]['hours'] = result1['hours']
            result[i]['course_nature'] = result1['course_nature']
        return result
    

def compare_date_string(date_obj, date_str,startorend):
    try:
        # print(type(date_str),type(date_obj))
        # 将字符串转换为 datetime.date 对象
        
        date_format = "%Y-%m-%d"  # 假设字符串的日期格式是 'YYYY-MM-DD'
        if startorend == 0:
            date_str = date_str + '-01-01'
            date_obj = str(date_obj) + '-01-01'
        else:
            date_str = date_str + '-12-31'
            date_obj = str(date_obj) + '-12-31'

        # print(date_str)
        # print(date_obj)
        parsed_date = datetime.strptime(date_str, date_format).date()
        date_obj = datetime.strptime(date_obj, date_format).date()
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

