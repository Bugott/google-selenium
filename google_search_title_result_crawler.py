import time

import requests
from urllib.parse import urlparse
import logging
from db_operation import DBOperation
import random
from bs4 import BeautifulSoup
import crawler_constant


class GoogleSearchResultCrawler(object):
    db_operation = DBOperation()
    logger = logging.getLogger()  # 不加名称设置root logger
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    fh = logging.FileHandler('F://log.txt')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    def isElementExistByXpath(self, driver, element):
        flag = True
        try:
            driver.find_element_by_xpath(element)
            return flag

        except:
            flag = False
            return flag

    def isElementExistByClassName(self, driver, element):
        flag = True
        try:
            driver.find_element_by_class_name(element)
            return flag

        except:
            flag = False
            return flag

    # 分析单个公司的搜索结果
    def operate_browser(self, company_web_site, company_id):
        random_ip = random.choice(crawler_constant.PROXIES)
        proxies = {'http': random_ip}
        random_ua = random.choice(crawler_constant.USER_AGENTS)
        headers = {
            'User-Agent': random_ua,
            'Connection': 'close'}
        search_title_link = crawler_constant.SEARCH_TITLE_URL.format(
            company_web_site)
        statistics_result = []
        start = 0
        try:
            response = requests.get(
                search_title_link + str(start), headers=headers, timeout=10,proxies=proxies).text
            # response = requests.get(
            #     search_title_link + str(start), headers=headers, timeout=10).text
            html_result = self.statistics_html(response, company_id, company_web_site)
            logging.info(html_result is None)
            if not html_result:
                statistics_result.append([(company_id, 0, 0, 0, 0, 1)])
            else:
                statistics_result.append(html_result)
                while True:
                    start += crawler_constant.PAGE_SIZE
                    if start / crawler_constant.PAGE_SIZE > 5:
                        sleep_time = 10 + random.random()
                    else:
                        sleep_time = random.randint(0, 20) + random.random()
                    time.sleep(sleep_time)
                    response_str = requests.get(
                        search_title_link + str(start), headers=headers, timeout=10,proxies=proxies).text
                    # response_str = requests.get(
                    #     search_title_link + str(start), headers=headers, timeout=10).text
                    html_result_str = self.statistics_html(response_str, company_id, company_web_site)
                    if not html_result_str:
                        break
                    else:
                        statistics_result.append(html_result_str)
            insert_records = []
            for i in statistics_result:
                for j in i:
                    insert_records.append(j)
            logging.info("start insert company id: " + str(company_id) + "size: " + str(len(insert_records)))
            self.db_operation.batch_insert_records(insert_records)
        except Exception as e:
            logging.info(e)
            logging.info("company_id: " + str(company_id) + " insert records:has exception")

    # 批量获得结果
    def get_statistics_results(self):
        start = 0
        page_size = 20
        return self.db_operation.get_company_info(start, page_size)
        # while True:
        #     result = self.db_operation.get_company_info(start, page_size)
        #     if not result:
        #         break
        #     else:
        #         for r in result:
        #             parsed_uri = urlparse(r.company_web_site)
        #             domain = '{uri.netloc}'.format(uri=parsed_uri)
        #             self.operate_browser(domain, r.company_id)
        #         start += page_size

    def statistics_html(self, html, company_id, company_web_site):
        statistics_result = []
        soup = BeautifulSoup(html, "lxml")
        search_result = soup.find_all(class_="g")
        if not search_result:
            return None
        for result in search_result:
            title_str = str(result.find('h3'))
            article_link = str(result.find('a')['href'])
            st_node = result.find(class_="st")
            try:
                big_data_word_count = title_str.count('大数据')
                ai_word_count = title_str.count('人工智能')
                cloud_compute_word_count = title_str.count('云计算')
                position_count = article_link.split(company_web_site)[1].count("/")
                # 如果有时间参数,则加入统计
                if st_node is not None:
                    for st_str in st_node.strings:
                        try:
                            article_year_time_text = st_str
                            logging.info(article_year_time_text)
                            article_year = int(article_year_time_text[0:4])
                        except Exception as e:
                            article_year = -1
                        break
                    if big_data_word_count != 0:
                        statistics_result.append(
                            (company_id, article_year, position_count, '大数据',
                             big_data_word_count, 1))
                    if ai_word_count != 0:
                        statistics_result.append(
                            (company_id, article_year, position_count, '人工智能',
                             ai_word_count, 1))

                    if cloud_compute_word_count != 0:
                        statistics_result.append(
                            (company_id, article_year, position_count, '云计算',
                             cloud_compute_word_count, 1))
            except Exception as e:
                logging.info("use beautifulsoup get html info has exception")
        return statistics_result


if __name__ == '__main__':
    s = GoogleSearchResultCrawler()
    result = s.get_statistics_results()
    for r in result:
        time.sleep(random.randint(0, 10))
        parsed_uri = urlparse(r.company_web_site)
        domain = '{uri.netloc}'.format(uri=parsed_uri)
        if ('www' in domain):
            search_domain = domain.split("www.")[1]
        else:
            search_domain = domain
        s.operate_browser(search_domain, r.company_id)
