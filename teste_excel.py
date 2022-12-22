import os, time, requests,pythoncom
import pandas as pd
import numpy as np
import multiprocessing as mp
from joblib import Parallel, delayed
import asyncio
import threading
from datetime import datetime, date, timedelta
from win32com.client import DispatchEx
        
def processa_xls():
    s = time.time() # Contador de tempo
    now_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Timestamp do inicio da rotina
    
    
    # Criando objeto Excel Application -----------------
    excel = DispatchEx('Excel.Application')
    #excel.Visible = True
    
    # Initialize
    pythoncom.CoInitialize()
    
    # Excel COMO ID
    xl_id = pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, excel)
    
    xlfile    = os.path.join(os.getcwd(),'vendas-combustiveis-m3.xls')
    sheetname = "Plan1"
    
    wb   = excel.Workbooks.Open(xlfile) # Workbook
    ws   = wb.Worksheets('Plan1')       # Sheet referente aos dados
    
    deriv  = "Vendas, pelas distribuidoras¹, dos derivados combustíveis de petróleo por Unidade da Federação e produto"
    diesel = "Vendas, pelas distribuidoras¹, de óleo diesel por tipo e Unidade da Federação"
    
    mes_dict = dict(Janeiro = 1, Fevereiro=2, Março=3, Abril=4, Maio=5, Junho=6, Julho=7, Agosto=8, Setembro=9, Outubro=10, Novembro=11, Dezembro=12)
    
    # Encontra Dados -------------------------------------
    
    # Encontrando cada tabela pela linha
    for i in range(42,ws.UsedRange.Rows.count):
        if str(ws.Cells(i,2).Value).find(deriv) != -1:
            val_der = i
        elif str(ws.Cells(i,2).Value).find(diesel) != -1:
            val_die = i
    
    # Encontrando numero da tabela dinamica
    for i,pvt in enumerate(ws.PivotTables(),1):
        
        nrow = ws.PivotTables(i).TableRange2.Row
        if nrow == val_der+5:
            der_pvt = i
        elif nrow == val_die+5:
            die_pvt = i
    #----------------------------------------------
    
    
    # Lendo dados ---------------------------------
    
    unit = str(ws.Cells(val_der,2).Value)[-3:-1]
    
    # Derivados do Petroleo-------------
    
    # Encontrando coluna maxima de dados
    for c in range(3,100):
        
        if str(ws.Cells(val_der+9,c).Value).find("NO ANO") !=  -1:
            col_der = c-1
            break
    
    # Encontrando linha maxima de dados
    for r in range(val_der+8,100):
        
        if str(ws.Cells(r,2).Value).find("Total do Ano") !=  -1:
            row_der = r-1
            break
    
    der_pivot = ws.PivotTables(der_pvt)
    filter_uf = der_pivot.PivotFields("UN. DA FEDERAÇÃO")
    items_uf = filter_uf.PivotItems()
    filter_pd = der_pivot.PivotFields("PRODUTO")
    items_pd = filter_pd.PivotItems()
    
    vDer = list()
    
    #async def append_data(row,col,nuf,npd):
    def append_data(row, col, nuf, npd, xl_id):
        # Initialize
        pythoncom.CoInitialize()
        
        # Getting Excel Obj
        excel = DispatchEx(
            pythoncom.CoGetInterfaceAndReleaseStream(xl_id, pythoncom.IID_IDispatch)
        )
        
        # Meses ainda nao disponiveis
        volume = ws.Cells(row,col).Value
        if not volume.isalpha():
            volume = 0
        
        vDer.append(dict(
                    year_month = date(int(ws.Cells(val_der+9,col).Value),mes_dict[ws.Cells(row,2).Value],1),
                    uf = nuf,
                    product = npd,
                    unit = unit,
                    volume = volume,
                    created_at = now_timestamp,
                    )
                )
        
        #await asyncio.sleep(0)
                
    for nuf in items_uf:
        ws.Cells(val_der+5,3).Value = nuf
        
        for npd in items_pd:
    
            ws.cells(val_der+6,3).Value = npd 
            print(f"Iterando: {nuf} e {npd} - {(time.time()-s):.02f}")
            threads = list()
            for row in np.arange(val_der+10, row_der+1):
                
                #processes = [mp.Pool().imap(append_data, (row,col,f'{nuf}',f'{npd}',)) for col in np.arange(3,col_der+1)]
                #Parallel(n_jobs=2)(delayed(append_data)(row,col,f'{nuf}',f'{npd}') for col in np.arange(3,col_der+1))
                for col in np.arange(3,col_der+1):
                #cores = [append_data(row,col,f'{nuf}',f'{npd}') for col in np.arange(3,col_der+1)]
                    process = threading.Thread(target=append_data,args=(row,col,f'{nuf}',f'{npd}',xl_id,))
                    threads.append(process)
                    process.start()
                
                
                for idx,process in enumerate(threads):
                    process.join()
                #await asyncio.gather(*cores)
                #loop = asyncio.get_event_loop()
                #loop.run_until_complete(asyncio.gather(*cores))
            
                #for col in np.arange(3,col_der+1):
                #    
                #    
                #    
                #    Meses ainda nao disponiveis
                #    volume = ws.Cells(row,col).Value
                #    if volume == "":
                #        volume = 0
                #        
                #    vDer.append(dict(
                #                    year_month = date(int(ws.Cells(val_der+9,col).Value),mes_dict[ws.Cells(row,2).Value],1),
                #                    uf = nuf,
                #                    product = npd,
                #                    unit = unit,
                #                    volume = volume,
                #                    created_at = now_timestamp,
                #                    )
                #                )
    
    df_der = pd.DataFrame(vDer)
    df_der.to_csv("dados_der.csv",sep=";",decimal=",",index=False)
    
    print(f"Tempo: {(time.time()-s)/60:.02f}")
    
    wb.Close(False)
    excel.Quit()


if __name__ == '__main__':
    
    processa_xls()
    
