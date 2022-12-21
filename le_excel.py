import os, time, requests
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from win32com.client import DispatchEx
from config import *

class Rotinas()
    def __init__(self):
        
        self.config = Config()
        
        pass
        
    def download_data(self):
        '''
        Obtem os dados a serem lidos, direto da internet
        
        Returns: None
        '''
        
        result    = requests.get(self.config.link_download) # Get do arquivo
        path_down = os.path.join(self.config.paths['path_download'],self.config.namefiles['dwn_file']) # Caminho para salvar o arquivo
        
        with open(path_down,'wb') as fobj: # Salva arquivo no caminho de download
            fobj.write(result.content)
            
        return
        
    def get_data(self):
        '''
        Obtem dados do arquivo XLS e salva em um dataframe
        
        Returns: Dataframe, Self Object com dados lidos do arquivo XLS
        '''
        
        s = time.time() # Contador de tempo
        now_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Timestamp do inicio da rotina
        
        # Criando objeto Excel Application -----------------
        excel = DispatchEx('Excel.Application')
        #excel.Visible = True
        
        xlfile    = os.path.join(self.config.paths['path_download'],self.config.namefiles['dwn_file'])
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
        for nuf in items_uf:
            ws.Cells(val_der+5,3).Value = nuf
            
            for npd in items_pd:
        
                ws.cells(val_der+6,3).Value = npd 
                print(f"Iterando: {nuf} e {npd} - {(time.time()-s):.02f}")
                
                for row in np.arange(val_der+10, row_der+1):
                    for col in np.arange(3,col_der+1):
                        
                        # Meses ainda nao disponiveis
                        volume = ws.Cells(row,col).Value
                        if volume == "":
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
        
        df_der = pd.DataFrame(vDer)
        df_der.to_csv("dados_der.csv",sep=";",decimal=",",index=False)
        
        print(f"Tempo: {(time.time()-s)/60:.02f}")
        
        wb.Close(False)
        excel.Quit()

