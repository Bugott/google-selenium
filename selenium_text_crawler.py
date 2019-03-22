import time
from urllib.parse import urlparse
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from db_operation import DBOperation
import random
from bs4 import BeautifulSoup


class SeleniumCompanyCrawler(object):
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
        chrome_options = Options()
        chrome_options.add_argument('lang=zh_CN.UTF-8')
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        USER_AGENTS = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; zh-CN)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; zh-CN) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; zh-CN; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        ]
        chrome_options.add_argument("user_agent=" + random.choice(USER_AGENTS))
        driver = webdriver.Chrome(options=chrome_options)
        # 打开google主页
        driver.get("http://www.google.com")
        # 缓冲2秒
        time.sleep(2)
        # 获取BeautifulSoup,用于后续的html节点分析
        search_box = driver.find_element_by_name('q')  # 取得搜索框,用name去获取DOM
        # 循环网址
        search_box.send_keys('site:' + company_web_site + ' intext:"大数据"|intext:"人工智能"|intext:"云计算" ')
        search_box.submit()  # 令 chrome 按下 submit按钮
        time.sleep(5)  # 缓冲3秒
        statistics_result = []
        while True:
            soup = BeautifulSoup(driver.page_source, "lxml")
            search_result = soup.find_all(class_="g")
            if not search_result:
                statistics_result.append((company_id, 0, 0, 0, 0, 0))
                break
            for result in search_result:
                article_link = str(result.find('a')['href'])
                st_node = result.find(class_="st")
                try:
                    em_result = st_node.find('em').contents
                    big_data_word_count = em_result.count('大数据')
                    ai_word_count = em_result.count('人工智能')
                    cloud_compute_word_count = em_result.count('云计算')
                    position_count = article_link.split(company_web_site)[1].count("/")
                    # 如果有时间参数,则加入统计
                    if st_node.find(class_="f") is not None:
                        article_time_text = st_node.find(class_="f")
                        article_year = int(article_time_text.text[0:4])
                        if big_data_word_count != 0:
                            statistics_result.append(
                                (company_id, article_year, position_count, '大数据',
                                 big_data_word_count, 0))
                        if ai_word_count != 0:
                            statistics_result.append(
                                (company_id, article_year, position_count, '人工智能',
                                 ai_word_count, 0))

                        if cloud_compute_word_count != 0:
                            statistics_result.append(
                                (company_id, article_year, position_count, '云计算',
                                 cloud_compute_word_count, 0))
                    # 没有时间参数，另外统计
                    else:
                        if big_data_word_count != 0:
                            statistics_result.append((company_id, -1, position_count, '大数据',
                                                      big_data_word_count, 1))
                        if ai_word_count != 0:
                            statistics_result.append(
                                (company_id, -1, position_count, '人工智能',
                                 ai_word_count, 0))

                        if cloud_compute_word_count != 0:
                            statistics_result.append(
                                (company_id, -1, position_count, '云计算',
                                 cloud_compute_word_count, 0))

                except Exception as e:
                    logging.info("crawler website: " + company_web_site + " id: " + str(company_id) + "has exception")
                    print(e)
                    continue
            # 翻页按钮
            if (SeleniumCompanyCrawler.isElementExistByXpath(self, driver,
                                                             '//*[@id="pnnext"]/span[2]')):
                next_page = driver.find_element_by_xpath('//*[@id="pnnext"]/span[2]')
                next_page.click()
                time.sleep(5)
            else:
                time.sleep(60)
                break
        # driver.close()
        try:
            self.db_operation.batch_insert_records(statistics_result)
        except Exception as e:
            logging.info(statistics_result)
            logging.info("insert records:has exception")

    # 批量获得结果
    def get_statistics_results(self):
        start = 0
        page_size = 20
        while True:
            result = self.db_operation.get_company_info(start, page_size)
            if not result:
                break
            else:
                for r in result:
                    parsed_uri = urlparse(r.company_web_site)
                    domain = '{uri.netloc}'.format(uri=parsed_uri)
                    self.operate_browser(domain, r.company_id)
                start += page_size


if __name__ == '__main__':
    s = SeleniumCompanyCrawler()
    s.operate_browser("www.dcits.com", 151)
