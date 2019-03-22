# 从数据库中读取a股上市公司的信息
class CompanyInfo(object):

    def __init__(self, company_id, company_web_site):
        self.company_web_site = company_web_site
        self.company_id = company_id

    def __str__(self):
        return "company_id: " + str(self.company_id) + \
               " company_web_site: " + str(self.company_web_site)

    __repr__ = __str__


# 定义每个公司的统计结果
class CrawlerCompanyResult(object):

    def __init__(self, company_id, year, position_count, word, word_count, is_title):
        self.company_id = company_id
        self.year = year
        self.position_count = position_count
        self.word = word
        self.word_count = word_count
        self.is_title = is_title

    def __str__(self):
        return "company_id: " + str(self.company_id) + \
               " year: " + str(self.year) + " position_count: " + str(self.position_count) \
               + " word: " + self.word + " word_count: " + str(self.word_count) + " is_title: " + str(self.is_title)

    __repr__ = __str__
