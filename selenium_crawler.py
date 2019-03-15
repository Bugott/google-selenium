import xlrd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import db_operation
import random


class SeleniumCompanyCrawler(object):
    # 获取需要爬取的公司网址
    def get_start_urls(file_path):
        # 打开excel
        excel = xlrd.open_workbook(file_path)
        # 获取工作表
        table = excel.sheet_by_index(1)  # 通过索引顺序获取
        rows = table.nrows
        result = {}
        for row in range(rows):
            company_name = table.cell(row, 0).value
            company_web_site = table.cell(row, 1).value
            result[company_web_site] = company_name

        return result

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
    def operate_browser(self, company_web_site, company_name):
        chrome_options = Options()
        # 设置无头浏览器
        # chrome_options.add_argument('--headless')
        USER_AGENTS = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        ]
        chrome_options.add_argument("user_agent="+random.choice(USER_AGENTS))
        driver = webdriver.Chrome(options=chrome_options)
        # 打开google主页
        driver.get("http://www.google.com")
        # 缓冲2秒
        time.sleep(2)
        # 获取BeautifulSoup,用于后续的html节点分析
        search_box = driver.find_element_by_name('q')  # 取得搜索框,用name去获取DOM
        # 循环网址
        search_box.send_keys('site:' + company_web_site + ' "大数据" OR "人工智能" OR "云计算" ')
        search_box.submit()  # 令 chrome 按下 submit按钮
        time.sleep(5)  # 缓冲3秒
        statistics_result = {}
        while True:
            search_result = driver.find_elements_by_class_name("g")
            for result in search_result:
                # st_node = result.find_element_by_class_name("st")
                st_node = result.find_element_by_css_selector(".g>.st")
                try:
                    word_count = len(st_node.find_elements_by_tag_name('em'))
                    # 如果有时间参数,则加入统计
                    if SeleniumCompanyCrawler.isElementExistByClassName(self, st_node, "f"):
                        article_time_text = st_node.find_element_by_class_name("f")
                        print(article_time_text.text)
                        article_year = int(article_time_text.text[0:4])
                        if article_year in statistics_result.keys():
                            statistics_result[article_year] += word_count
                        else:
                            statistics_result[article_year] = word_count
                    # 没有时间参数，另外统计
                    else:
                        if -1 in statistics_result.keys():
                            statistics_result[-1] += word_count
                        else:
                            statistics_result[-1] = word_count

                except Exception as e:
                    print(e)
                    continue
            # 翻页按钮
            if (SeleniumCompanyCrawler.isElementExistByXpath(self, driver,
                                                             '//*[@id="pnnext"]/span[2]')):
                next_page = driver.find_element_by_xpath('//*[@id="pnnext"]/span[2]')
                next_page.click()
                time.sleep(5)
            else:
                break
        # driver.close()
        return CrawlerCompanyResult(statistics_result, company_web_site, company_name)

    # 批量获得结果
    def get_statistics_results(self, company_info):
        result = []
        for company_web_site, company_name in company_info.items():
            try:
                print("current company" + company_web_site)
                result_of_one_company = SeleniumCompanyCrawler.operate_browser(self, company_web_site, company_name)
            except Exception as e:
                print("current website:" + company_web_site + "has exception"+e)
                continue
            for year, count in result_of_one_company.statistics_result.items():
                current_result = [result_of_one_company.company_name,
                                  result_of_one_company.company_web_site, year, count]
                result.append(current_result)

        return result

    def statistics(self):
        compony_info = SeleniumCompanyCrawler.get_start_urls("F://company.xls")
        print(compony_info)
        statiscitcs_results = SeleniumCompanyCrawler.get_statistics_results(self, compony_info)
        print(statiscitcs_results)
        # db_operation.batch_insert_records(statiscitcs_results)


# 定义每个公司的统计结果
class CrawlerCompanyResult(object):

    def __init__(self, statistics_result, company_web_site, company_name):
        self.statistics_result = statistics_result
        self.company_web_site = company_web_site
        self.company_name = company_name


if __name__ == '__main__':
    s = SeleniumCompanyCrawler()
    s.statistics()
