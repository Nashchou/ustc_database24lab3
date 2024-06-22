from itertools import chain
import re
import string
import pymysql

class teacher:
    def __init__(self) -> None:
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='20040501',
                                  database='lab3')

    def check(self, data: dict):
        if not (str.isalnum(data['job_numbers'])
                and len(data['job_numbers']) <= 5):
            raise Exception('error: job_numbers format')
        elif not str.isalpha(data['name']):
            raise Exception('error: name format')
        elif not str.isdigit(data['sex']):
            raise Exception('error: sex format')
        elif not str.isdigit(data['job_title']):
            raise Exception('error: job_title format')
        elif "#" in data['name'] or ";" in data['name']:
            raise Exception('error: name format')

    def insert(self, data: dict):
        self.check(data)
        cursor = self.db.cursor()
        sql = "INSERT INTO teacher VALUES({},{},{},{})".format(str.upper(data['job_numbers']), data['name'], data['sex'], data['job_title'])
        try:
            cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise Exception(e)
        cursor.close()

    def delete(self, id: string):
        cursor = self.db.cursor()
        sql = "DELETE FROM teacher WHERE job_numbers={}".format(str.upper(id))
        try:
            cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            raise Exception('error: job_numbers not exist')
        cursor.close()

    def update(self, data: dict):
        self.check(data)
        cursor = self.db.cursor()
        sql = "UPDATE teacher SET name = {}, sex = {},job_title = {} WHERE job_number = {}".format(data['name'],data['sex'],data['job_title'], str.upper(data['job_number']))
        try:
            cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            raise Exception('error: update job_number format is wrong')
        cursor.close()

    def search_id(self, id: string):
        cursor = self.db.cursor()
        sql = "SELECT * FROM teacher WHERE job_number=%s"
        cursor.execute(sql, (id)) 
        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))

        result_list = list(map(result2dict, cursor.fetchall()))
        cursor.close()
        return result_list

    def search_name(self, name: string):
        cursor = self.db.cursor()
        sql = "SELECT * FROM teacher WHERE name LIKE '%%{}%%'".format(name)
        cursor.execute(sql)

        def result2dict(result):
            return dict(
                zip([x[0] for x in cursor.description], [x for x in result]))

        result_list = list(map(result2dict, cursor.fetchall()))
        cursor.close()
        return result_list



# a = teacher()
# print(a.search_name('a'))
# try:
#     a.delete('C002')
# except Exception as e:
#     print(e)
