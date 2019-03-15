import pymysql


class DBOperation(object):
    def connect_db(self):
        return pymysql.connect(host='47.106.199.194',
                               port=3306,
                               user='root',
                               password='090448',
                               database='graduation_project',
                               charset='utf-8')

    def batch_insert_records(self, record):
        con = DBOperation.connect_db()
        cur = con.cursor()
        try:
            cur.executemany("INSERT INTO t_company_statistics (c_company_name, c_web_site, c_year,c_word_count"
                            + " VALUES (%s, %s,%s,%s)", record)
            con.commit()
        except Exception as e:
            print("write to db has exception")
            con.rollback()
        finally:
            cur.close()
            con.close()
