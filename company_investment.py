import xlrd
from db_operation import DBOperation

excel = xlrd.open_workbook("F://毕业论文资料//固定资产-IT.xlsx")
table = excel.sheet_by_index(0)
nrows = table.nrows

result = {}
db_operation = DBOperation()
for index in range(3, nrows):
    company_code = table.cell(index, 0).value
    year = int(table.cell(index, 1).value[0:4])
    increase = table.cell(index, 6).value
    if increase:
        increase = round(float(table.cell(index, 6).value), 2)
    else:
        increase = float(0)
    if (company_code, year) in result.keys():
        result[(company_code, year)] += increase
    else:
        result[(company_code, year)] = increase

insert_records = []
for key, value in result.items():
    company_code = key[0]
    year = key[1]
    increase = value
    insert_records.append((company_code, year, increase))

db_operation.batch_insert_investment(insert_records)
