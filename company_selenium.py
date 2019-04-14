import time
from selenium import webdriver
from db_operation import DBOperation
from selenium.webdriver.chrome.options import Options
import random
from datetime import datetime

from selenium_text_crawler import SeleniumCompanyCrawler

chrome_options = Options()
db_operation = DBOperation()
se = SeleniumCompanyCrawler()
chrome_options.add_argument('lang=zh_CN.UTF-8')
chrome_options.add_argument("--headless")
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"
]
chrome_options.add_argument("user_agent=" + random.choice(USER_AGENTS))
driver = webdriver.Chrome(options=chrome_options)
# 打开google主页
for i in range(35,50):
    driver.get("http://s.askci.com/stock/a/?reportTime=2018-09-30&pageNum=" + str(i) + "#QueryCondition")
    i = 1
    time.sleep(4)
    rtable = driver.find_element_by_xpath('//*[@id="myTable04"]/tbody')
    trlist = rtable.find_elements_by_tag_name("tr")
    result = []
    for row in trlist:
        tdList = row.find_elements_by_tag_name("td")
        company_code = tdList[1].text
        company_name = tdList[3].text
        company_city = tdList[4].text
        company_staff_count = int(tdList[8].text)
        company_public_time = datetime.strptime(tdList[9].text, '%Y-%m-%d')
        result.append((company_code, company_name, company_public_time, company_city, company_staff_count))
    db_operation.batch_insert_company_info(result)
driver.close()
