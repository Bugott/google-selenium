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
        try:
            cur.execute(
                'SELECT c_id,c_company_web_site FROM t_company_info WHERE c_company_web_site !="" AND `c_company_industry` IN ("软件-") AND c_id =789 ORDER BY c_id LIMIT ' + str(
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
