import os
from win32com.client import DispatchEx

excel = DispatchEx('Excel.Application')
wb = excel.Workbooks.Open(os.path.join(os.getcwd(),'vendas-combustiveis-m3.xls'))
ws = wb.Worksheets('Plan1')

#ws.PivotTables(1).PivotFields().ClearAllFilters()
#ws.PivotTables(1).PivotFilters.Add2(15, None, "ACRE")
for pv in ws.PivotTables():

    print(pv)

excel.Workbooks.Close()

#ws.PivotTables(1).PivotFields("Quarters").PivotFilters('Add2', 'xlBefore', '10/10/2017')