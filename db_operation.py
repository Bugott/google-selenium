import pymysql
from entity_info import CompanyInfo


class DBOperation(object):
    def connect_db(self):
        return pymysql.connect(host='47.106.199.194',
                               port=3306,
                               user='root',
                               password='090448',
                               database='graduation_project',
                               charset='utf8')

    def get_company_info(self, start_index, page_size):
        con = self.connect_db()
        cur = con.cursor()
        company_infos = []
        sql_str = '''SELECT c_id,c_company_web_site FROM t_company_info a WHERE a.c_company_industry IN("计算机设备-","通信设备-","互联网信息-","信息服务-","电子商务-","软件-","游戏动漫-") AND c_id NOT IN (SELECT DISTINCT b.c_company_id FROM t_company_statistics b where c_is_title=0) AND c_company_web_site!=""'''
        try:
            cur.execute(
                sql_str + ' ORDER BY c_id  LIMIT ' + str(
                    start_index) + ',' + str(page_size))
            for row in cur.fetchall():
                company_infos.append(CompanyInfo(row[0], row[1]))
            return company_infos
        except Exception as e:
            print(e)
            print("read from db has exception")
        finally:
            cur.close()
            con.close()

    def batch_insert_records(self, record):
        con = self.connect_db()
        cur = con.cursor()
        try:
            cur.executemany(
                "INSERT INTO t_company_statistics (c_company_id,c_year,c_position_count,c_word,c_word_count,c_is_title)"
                + " VALUES(%s,%s,%s,%s,%s,%s)", record)
            con.commit()
        except Exception as e:
            print(e)
            print("write to db has exception")
            con.rollback()
        finally:
            cur.close()
            con.close()

    def batch_insert_investment(self, record):
        con = self.connect_db()
        cur = con.cursor()
        try:
            cur.executemany(
                "INSERT INTO t_company_it_investment (c_company_code,c_year,c_hardware_investment)"
                + " VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE c_hardware_investment=VALUES(c_hardware_investment)",
                record)
            con.commit()
        except Exception as e:
            print(e)
            print("write to db has exception")
            con.rollback()
        finally:
            cur.close()
            con.close()

    def batch_insert_company_info(self, record):
        con = self.connect_db()
        cur = con.cursor()
        try:
            cur.executemany(
                "INSERT INTO t_company_info(c_company_code,c_company_name,c_public_time,c_company_city,c_staff_count)"
                + " VALUES(%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE c_company_name=VALUES(c_company_name),"
                  "c_public_time=values(c_public_time),c_company_city=values(c_company_city),c_staff_count=values(c_staff_count)",
                record)
            con.commit()
        except Exception as e:
            print(e)
            print("write to db has exception")
            con.rollback()
        finally:
            cur.close()
            con.close()

    def insert_year_info(self, record):
        con = self.connect_db()
        cur = con.cursor()
        try:
            cur.executemany(
                "INSERT INTO t_year_info(c_company_code,c_year)"
                + " VALUES(%s,%s) ON DUPLICATE KEY UPDATE c_year =VALUES(c_year)",
                record)
            con.commit()
        except Exception as e:
            print(e)
            print("write to db has exception")
            con.rollback()
        finally:
            cur.close()
            con.close()
