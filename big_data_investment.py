import xlrd
from db_operation import DBOperation

excel = xlrd.open_workbook("F://毕业论文资料//PT_LCRDSpending.xlsx")
table = excel.sheet_by_index(0)
nrows = table.nrows
result = []
word_list = ["大数据", "人工智能", "ai", "云", "区块链", "移动商务", "sas", "saas"]
db_operation = DBOperation()
for index in range(3, nrows):
    company_code = table.cell(index, 0).value
    year = int(table.cell(index, 1).value[0:4])
    detail = table.cell(index, 12).value
    if detail:
        for i in word_list:
            if i in detail:
                result.append((company_code, year))
                break

db_operation.insert_year_info(result)
