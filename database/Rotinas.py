# !/usr/bin/env python
# *- coding: utf-8-sig -*-

import os, time, requests
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from win32com.client import DispatchEx
from sqlalchemy.orm import Session, aliased

from config   import *
from Auxiliar import *
from Banco    import *

auxi = Auxiliar()

class Rotinas():
    def __init__(self):
        
        self.config = Config()
        
        pass
        
    def download_data(self):
        '''
        Obtem os dados a serem lidos, direto da internet. Tambem salva
        o arquivo mais recente, caso ele ja exista, com extensao '_old'.
        
        Returns: None
        '''
        
        result    = requests.get(self.config.link_download) # Get do arquivo
        path_down = os.path.join(self.config.paths['path_download'],self.config.namefiles['dwn_file']) # Caminho para salvar o arquivo
        
        # Caso o arquivo ja exista, altera o nome
        try:
            os.rename(
                      path_down,os.path.join(self.config.paths['path_download'],
                      self.config.namefiles['dwn_file'][:-4]+"_old"+self.config.namefiles['dwn_file'][-4:])
                      )
        except:
            try:
                # Exclui mais antigo
                os.remove(
                        os.path.join(self.config.paths['path_download'],
                        self.config.namefiles['dwn_file'][:-4]+"_old"+self.config.namefiles['dwn_file'][-4:])
                        )
                
                # Renomeia mais novo
                os.rename(
                        path_down,os.path.join(self.config.paths['path_download'],
                        self.config.namefiles['dwn_file'][:-4]+"_old"+self.config.namefiles['dwn_file'][-4:])
                        )
                
                print("> Arquivo mais antigo excluido. Novo arquivo gerado.")
                auxi.anota("Arquivo mais antigo excluido. Novo arquivo gerado.")
                
            except:
                print("> Arquivo XLS ainda nao existente.")
                auxi.anota("Arquivo XLS ainda nao existente.")
            
            
        
        # Salvando o arquivo no diretorio
        try:
            with open(path_down,'wb') as fobj: # Salva arquivo no caminho de download
                fobj.write(result.content)
            print("> Arquivo baixado com sucesso.")
            auxi.anota("Arquivo XLS baixado com sucesso.")
        except:
            print("> Nao foi possível fazer o download de novos dados.")
            auxi.anota("Nao foi possível fazer o download de novos dados.")
            
        return
    
    def check_dados(self, df_total, df_fuel):
        '''
        Checa se os dados coletados da tabela correspondem aos valores totais
        disponibilizados.
        
        df_total: Dataframe, dados totais de um tipo de dado
        df_fuel: Dataframe, dados detalhados de um tipo de dado
        
        Returns: Boolean, True se os valores conferem, senao False
        '''
        
        df_nf = df_fuel.groupby(by=['year_month']).agg(dict(volume='sum')).reset_index() # Agrupa por data
        df_nf['volume'] = df_nf['volume'].round(0)                                       # Arredonda para 0 decimais
        
        df_total['volume'] = df_total['volume'].round(0) # Arredonda para 0 decimais
        
        # Sort para comparacao dos dados
        df_total.sort_values(by=['year_month'],inplace=True) # Sort por data
        df_nf.sort_values(by=['year_month'], inplace=True)   # Sort por data
        
        # Resetando index para comparacao exata
        df_total.reset_index(drop=True,inplace=True)
        df_nf.reset_index(drop=True,inplace=True)
        
        # Agrupa por ano
        df_total['year'] = [x.year for x in df_total['year_month']]
        df_nf['year'] = [x.year for x in df_nf['year_month']]
        
        df_tyear = df_total.groupby(by=['year']).agg(dict(volume='sum')).reset_index() # Agrupa dados totais por ano
        df_nfyear = df_nf.groupby(by=['year']).agg(dict(volume='sum')).reset_index()   # Agrupa dados totais por ano
        
        # Realiza check
        check = False
        if df_total.equals(df_nf) and df_tyear.equals(df_nfyear): # Caso ambos sejam iguais
            
            check = True
        
        return check
    
    def get_data(self):
        '''
        Obtem dados do arquivo XLS e salva em um dataframe
        
        Returns: None
        '''
        
        s = time.time() # Contador de tempo
        now_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Timestamp do inicio da rotina
        
        # Array mnemonicos para a tabela de cada dado. A ordem sera seguida de acordo
        # com o declarado no arquivo config.py
        dados_busca = [x for x in self.config.filtros] # Mnemonico dos items a serem lidos (deriv e diesel nesse caso)
        
        # Criando objeto Excel Application -----------------
        excel = DispatchEx('Excel.Application')
        excel.Visible = self.config.xls_visible
        
        xlfile    = os.path.join(self.config.paths['path_download'],self.config.namefiles['dwn_file'])
        sheetname = "Plan1"
        
        wb   = excel.Workbooks.Open(xlfile) # Workbook
        ws   = wb.Worksheets('Plan1')       # Sheet referente aos dados
        
        #deriv  = "Vendas, pelas distribuidoras¹, dos derivados combustíveis de petróleo por Unidade da Federação e produto"
        #diesel = "Vendas, pelas distribuidoras¹, de óleo diesel por tipo e Unidade da Federação"
        
        mes_dict = self.config.mes_dict
        #-----------------------------------------------------
        
        # Encontra Dados -------------------------------------
        
        # Encontrando cada tabela pela linha
        
        # Array para linha inicial do bloco de dados. A ordem sera seguida de acordo
        # com o declarado no arquivo config.py
        vIni = list() 
        for l in self.config.str_busca:
            for i in range(42,ws.UsedRange.Rows.count):
                
                # Caso encontro a string de busca, guarda o numero da linha inicial
                if str(ws.Cells(i,2).Value).find(self.config.str_busca[l]) != -1:
                    vIni.append(i)
        
        # Encontrando numero da tabela dinamica
        
        # Array para indice da PivotTable do bloco de dados. A ordem sera seguida de acordo
        # com o declarado no arquivo config.py
        vPvt = list()
        for i, nm in enumerate(self.config.str_busca,0):    # Para cada string de bytearray
            for j,pvt in enumerate(ws.PivotTables(),1): # Para cada PivotTable do XLS
                nrow = ws.PivotTables(j).TableRange2.Row
                
                if nrow == vIni[i]+5:
                    vPvt.append(j)
                    break
        #----------------------------------------------
        
        # Lendo dados ---------------------------------
        vDados = list() # Array para dados finis
        for i,lin in enumerate(vIni,0):
        
            unit = str(ws.Cells(lin,2).Value)[-3:-1] # Unidade do Combustivel
            
            # Derivados do Petroleo-------------
            
            # Encontrando coluna maxima de dados
            for c in range(3,100):
                
                if str(ws.Cells(lin+9,c).Value).find("NO ANO") !=  -1:
                    col_ano = c-1
                    break
            
            # Encontrando linha maxima de dados
            for r in range(lin+8,lin+100):
                
                if str(ws.Cells(r,2).Value).find("Total do Ano") !=  -1:
                    row_mes = r-1
                    break

            # Seleciona a tabela dinamica
            tbl_pivot = ws.PivotTables(vPvt[i])
            
            # Filtro um
            fil_one   = tbl_pivot.PivotFields(self.config.filtros[dados_busca[i]][0])
            items_one = fil_one.PivotItems()
            
            # Filtro dois
            fil_two   = tbl_pivot.PivotFields(self.config.filtros[dados_busca[i]][1])
            items_two = fil_two.PivotItems()
            
            # Itera sob tabelas e filtros para obtencao dos dados
            
            # Dados totais para conferencia
            vTot = list()
            for row in np.arange(lin+10, row_mes+1): # Cada linha da PvT
                for col in np.arange(3,col_ano+1):   # Cada coluna da PvT
                    
                    # Meses ainda nao disponiveis
                    volume = ws.Cells(row,col).Value
                    #if volume == "":
                    if volume is None or str(volume) == "":
                        volume = 0
                        
                    vTot.append(dict(
                                    year_month = date(int(ws.Cells(lin+9,col).Value),mes_dict[ws.Cells(row,2).Value],1),
                                    volume = volume,
                                    )
                                )
            
            df_total = pd.DataFrame(vTot) # Dataframe com valores totais
            
            vFuel = list()   # Array para dados individuais
            for nuf in items_one: # Filtro um
                ws.Cells(lin+5,3).Value = nuf
                
                for npd in items_two: # Filtro dois
            
                    ws.cells(lin+6,3).Value = npd 
                    print(f"> Iterando: {dados_busca[i]} - {nuf} e {npd} - {(time.time()-s):.02f}")
                    auxi.anota(f"Lendo dados: {dados_busca[i]} - {nuf} e {npd}")
                    
                    for row in np.arange(lin+10, row_mes+1): # Cada linha
                        for col in np.arange(3,col_ano+1):   # Cada coluna
                            
                            # Meses ainda nao disponiveis
                            volume = ws.Cells(row,col).Value
                            #if volume == "":
                            if volume is None or str(volume) == "":
                                volume = 0
                                
                            vFuel.append(dict(
                                            year_month = date(int(ws.Cells(lin+9,col).Value),mes_dict[ws.Cells(row,2).Value],1),
                                            uf = nuf.Name,
                                            product = npd.Name,
                                            unit = unit,
                                            volume = volume,
                                            created_at = now_timestamp,
                                            )
                                        )
                            #df = pd.DataFrame(vFuel)
                            #df['year_month']= pd.to_datetime(df['year_month'], format='%Y-%m-%d')
                            #df['year_month']= [x.date() for x in df['year_month']]
                            #input(df.dtypes)
            print(f"Execucao do ciclo: {(time.time()-s)/60:.02f}")
            auxi.anota(f"Execucao do ciclo: {(time.time()-s)/60:.02f}")
            
            check = self.check_dados(df_total,pd.DataFrame(vFuel))
            if check:
                vDados.append(vFuel)
                self.insert_data(df = pd.DataFrame(vFuel), tbl = dados_busca[i])
            else:
                print("> Dados coletados e valores totais nao conferem. Os dados nao serao inseridos na base.")
                auxi.anota("Dados coletados e valores totais nao conferem. Os dados nao serao inseridos na base.")
        
        # Transforma em CSV
        for i,d in enumerate(vDados,0):
            
            path_file = os.path.join(self.config.paths['path_temp'],f"dados_{dados_busca[i]}.csv")
            
            df = pd.DataFrame(d)
            df.to_csv(path_file,sep=";",decimal=",",index=False, encoding='utf-8-sig')
        
        print(f"Tempo final: {(time.time()-s)/60:.02f}")
        auxi.anota(f"Tempo final: {(time.time()-s)/60:.02f}")
        #-----------------------------------------------------------------------
        
        wb.Close(False)
        excel.Quit()
        
        return
        
    def insert_data(self,df,tbl):
        '''
        Insere informacoes no banco de dados na tabela correspondente
        
        df: Dataframe, dados a serem inseridos no banco de dados
        tbl: Str, nome da tabela onde seram inseridos os dados
        
        Returns: None
        '''
        
        session = Session(bind=engine)
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Leitura dos dados e inclusão em objetos Tabela
        dados = list()
        for i, dado in df.iterrows():
            
            if tbl == 'deriv':
                dados.append(
                    DerivFuel(
                        year_month = dado.year_month,
                        uf         = dado.uf,
                        product    = dado['product'],
                        unit       = dado.unit,
                        volume     = dado.volume,
                        created_at = dado.created_at
                    )
                
                )
            
            elif tbl == 'diesel':
                dados.append(
                    DieselFuel(
                        year_month = dado.year_month,
                        uf         = dado.uf,
                        product    = dado['product'],
                        unit       = dado.unit,
                        volume     = dado.volume,
                        created_at = dado.created_at
                    )
                
                )
                
        
        # Insercao em massa
        try:
            session.bulk_save_objects(objects=dados)
        except:
            print("> Erro na leitura dos dados. Provavelmente o tipo dos dados esta incorreto.")
            auxi.anota("Erro na leitura dos dados. Provavelmente o tipo dos dados esta incorreto.")
            return
        
        try:
            session.commit()
            print(f"> Dados '{tbl}' inseridos com sucesso na base de dados")
            auxi.anota(f"Dados '{tbl}' inseridos com sucesso na base de dados")
        except:
            print('> Nao foi possivel inserir os dados na base.')
            auxi.anota('Nao foi possivel inserir os dados na base.')
        
        return
        


