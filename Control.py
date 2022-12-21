# !/usr/bin/env python
# *- coding: utf-8 -*-

import os, calendar
import sys
from datetime import *
from database import *
from UpdateAccess import *
import pandas as pd
import time

strPath = os.getcwd()

class Controller(object):
        
    def __init__(self, config):
        self.config = config
        self.cabecalho_email = "(BI)"
        self.remetente       = "Middle"
        pass
    
    def date_now(self):
        
        self.now     = datetime.now().date()          # Data de hoje
        self.nowt    = datetime.now()                 # Data e hora de hoje
        self.now1    = self.now + timedelta(days=-1)  # Data de um dia atrqs
        self.now2    = self.now + timedelta(days=-2)  # Data de um dia atrqs
        self.now6    = self.now + timedelta(days=-6)  # Data de sete dias atras
        self.now7    = self.now + timedelta(days=-7)  # Data de sete dias atras
        self.now35   = self.now + timedelta(days=-35) # Data de 35 dias atras
        self.now62   = self.now + timedelta(days=-62) # Data de 62 dias atras
        self.now366  = self.now + timedelta(days=-366)# Data de 1 ano atras
        self.fut1    = self.now + timedelta(days=+1)  # Data de 1 dia a frente
        self.fut7    = self.now + timedelta(days=+7)  # Data de 7 dias a frente
        self.fut8    = self.now + timedelta(days=+8)  # Data de 8 dias a frente
        self.fut9    = self.now + timedelta(days=+9)  # Data de 8 dias a frente
        
        self.year  = self.now.year                 # Ano de hoje
        self.month = self.now.month                # Mês de hoje
        self.day   = self.now.day                  # Dia de hoje
        self.now_i = date(self.year, self.month,1) # Primeiro dia do mes
        
        self.strDate  = f"{self.year}{self.month:02d}{self.day:02d}"                # String da data YYYYMMDD
        self.strDate1 = f"{self.fut1.year}{self.fut1.month:02d}{self.fut1.day:02d}" # String da data YYYYMMDD
        
        return
    
    def func_envia_email(self,destinos, pathfiles, esubject, message ,remetente, namefiles=None):
        ''' enderecos de destino, caminho dos arquivos a serem anexados, assunto, corpo, remetente e nome dos arquivos a serem anexados'''
        ''' Envia email padrao para os enderecos em "destinos" '''
    
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.application import MIMEApplication
        
        #sender = 'middle.alvaro@gmail.com' # Remetente
        #password = "carnage2"              # Senha do email remetente
        #app_password = "afvutwpnioyozuge"  # Senha de App do email 
        sender       = 'middle.informes@gmail.com' # Remetente
        password     = "2vtwr7tG#"                 # Senha do email remetente
        app_password = "zdivzkbpeufpyywx"          # Senha de App do email 
        receivers    = destinos                    # Destniatarios
        appPath      = pathfiles                   # Caminho dos arquivos anexos
            
        msg = MIMEMultipart()
        msg['From'] = remetente          #sender # Remetente
        msg['To'] = ", ".join(receivers) # Destinatarios
        msg['Subject'] = esubject        # Titulo/Assunto do e-mail
        
        msg.attach(MIMEText(message, 'plain')) # Mensagem do corpo do e-mail
        
        for f in namefiles or []:
            with open(os.path.join(pathfiles, f),'rb') as fil:
                part = MIMEApplication(fil.read(), Name=f)
            
            part['Content-Disposition'] = 'attachment;filename="%s"' %(f)
            msg.attach(part)
                
        try:
            smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465) # Acessa servidor SMTP do google com segurança SSL
            #smtpObj = smtplib.SMTP_SSL('smtp.solenergias.com:587')
            #smtpObj.starttls()
            smtpObj.login(sender,app_password) # Loga no servidor SMTP com a conta de e-mail fornecida
            msg = str(msg) 
            smtpObj.sendmail("Email Automatico", receivers, msg) # Envia o email com a mensagem da variavel "msg"
            smtpObj.quit()  # Fecha conexão com o servidor
            print("Email enviado com sucesso!")
        
        except Exception as ex:
            input("Error: Nao foi possivel enviar o e-mail.\n"+str(ex))
            
        return
        
        
    
    #def connect(self):
    #    con = imaplib.IMAP4_SSL(self.config.email['imap_url'])
    #    con.login(self.config.email['user'], self.config.email['password'])
    #
    #    if con.state == 'AUTH':
    #        print('Conexao com e-mail {:} efetuada'.format(self.config.email['user']))
    #
    #    self.con = con

    #def disconnect(self):
    #
    #    # Faz logout
    #    self.con.close()
    #    self.con.logout()
    #    print('Desconectado do email: {}\n\n'.format(self.config.email['user']))

    #def check_mailbox(self, mailbox):
    #    print('Verificacao da caixa {} em {:%Y-%m-%d %H:%M:%S}'.format(mailbox, datetime.datetime.now()))
    #
    #    self.con.select(mailbox=mailbox)
    #    result, data = self.con.uid('search', None, 'ALL')
    #    if data == [b'']:
    #
    #        print('Mailbox {} vazia\n'.format(mailbox))
    #        self.check = 0
    #
    #    else:
    #        print('Mailbox {} com e-mail\n'.format(mailbox))
    #        self.check = 1
    #
    #def get_mails_mailbox(self, mailbox):
    #    self.con.select(mailbox=mailbox)
    #
    #    result, data = self.con.uid('search', None, 'ALL')
    #
    #    # loop em todos os e-mails
    #    mails = list()
    #    for i, mail in enumerate(data[0].split()):
    #        result2, email_data = self.con.uid('fetch', mail, '(RFC822)')
    #        raw_email = email_data[0][1].decode('utf-8')
    #        email_message = email.message_from_string(raw_email)
    #
    #        # loop em todos os anexos
    #        for part in email_message.walk():
    #
    #            if part.get('Content-Disposition') is None:
    #                continue
    #
    #            else:
    #
    #                # Retira imagens de assinatura
    #                #if 'png' in part.get('Content-Description'):
    #                #    print(part.get('Content-Description'))
    #                #    continue
    #
    #
    #                filename = part.get_filename()
    #                content = part.get_payload(decode=True)
    #
    #
    #                # Checks para saber como guardar os diferentes tipos de arquivos
    #                if mailbox == 'RDH':
    #                #if mailbox == '2_ONS/2.1_RDH':
    #                    if 'JAN' in filename:
    #                        ano = str(datetime.datetime.now().year + 1)
    #
    #                    else:
    #                        ano = str(datetime.datetime.now().year)
    #
    #                if mailbox == 'ACOMPH':
    #                    ano = str(filename[-8:-4])
    #
    #                aux = dict(
    #                    filename=filename,
    #                    content=content,
    #                    ano=ano
    #                )
    #
    #                mails.append(aux)
    #
    #        # deleta e-mail
    #        self.con.uid('STORE', mail, '+FLAGS', '(\Deleted)')
    #        self.con.expunge()
    #
    #
    #    self.mails = mails
    #    #self.con.close()
    #    #self.con.logout()
    #
    #def download_files(self, path):
    #
    #    for i, mail in enumerate(self.mails):
    #
    #        file = open(
    #            file=os.path.join(
    #                path,
    #                mail['ano'],
    #                mail['filename']
    #            ),
    #            mode='wb'
    #        )
    #        file.write(mail['content'])
    #        file.close()

    #def create_list(self, nome):
    #    paths = list()
    #    for i, file in enumerate(self.mails):
    #
    #        if nome == 'rdh':
    #            paths.append(
    #                os.path.join(self.config.paths['paths_rdh'], file['ano'], file['filename'])
    #            )
    #
    #        else:
    #
    #            paths.append(
    #                os.path.join(self.config.paths['paths_acomph'], file['ano'], file['filename'])
    #            )
    #
    #
    #    df = pd.DataFrame(data=paths, columns=['path'])
    #
    #    df.to_csv(self.config.paths[nome], index=False)
    #
    #    return df
    
    def create_list_rel(self, nome):
        ''' 
        Verifica existencia de novos relatorios e insere suas informacoes no banco de dados
        
        :nome: Str, nome do relatorio (ex: rdh, acompH, etc)
        '''
        
        self.date_now() # Funcao objeto de datas e horas
        
        # Casos onde o arquivo ainda precisa ser baixado previamente
        if nome in ["merge"]: 
            
            if nome == "merge" and self.nowt.hour >= config.control['hour_check']:
                
                leitura = Hidrologia(config=config)
                leitura.download_merge()
        #-----------------------------------------------------------
        
        path_rel = os.path.join(self.config.paths['paths_'+nome]) # Caminho para os relatorios
        hist     = pd.read_csv(self.config.paths[nome],sep=";")   # Arquivo CSV com lista dos relatorios ja lidos
        vUp      = []                                             # Inciializando vetor de updates
        
        fileList = os.listdir(path_rel)
        fileList.sort()
        
        for i,file in enumerate(fileList,0):
                        
            if nome == "rdh": # Caso seja o RDH
                
                if len(file) > 13: # Se for o padrao de nome novo

                    if hist[hist['path']==file].empty:

                        vUp.append(os.path.join(path_rel,file))
                        hist = hist.append({'path':file},ignore_index=True)
                    
            elif nome == "acomph": # Caso seja o acompH
                
                if hist[hist['path']==file].empty:
                    
                    vUp.append(os.path.join(path_rel,file))
                    hist  = hist.append({'path':file},ignore_index=True)
                    
            elif nome == "pmedia": # Caso seja o arquivo de chuva pmedia
            
                if file.find("precipitacao_media") != -1:
                
                    if hist[hist['path']==file].empty:
                    
                        vUp.append(os.path.join(path_rel,file))
                        hist  = hist.append({'path':file},ignore_index=True)
                        
            elif nome == "gefs": # Caso seja o arquivo de chuva GEFS
            
                if file.find("GEFS50_precipitacao14d") != -1:
                    
                    if hist[hist['path']==file].empty:
                        
                        vUp.append(os.path.join(path_rel,file))
                        hist = hist.append({'path':file},ignore_index=True)
            
            elif nome == "ecmwf": # Caso seja o arquivo de chuva ECMWF
            
                if file.find("ECMWF_precipitacao14d") != -1:
                    
                    if hist[hist['path']==file].empty:
                        
                        vUp.append(os.path.join(path_rel,file))
                        hist = hist.append({'path':file},ignore_index=True)
            
            elif nome == "merge": # Caso seja o arquivo do merge
            
                if file.find("chuva") != -1:
                
                    if hist[hist['path']==file].empty:
                        
                        vUp.append(os.path.join(path_rel,file))
                        hist  = hist.append({'path':file},ignore_index=True)
            
            elif nome == "ipdo": # Caso seja o arquivo IPDO
                
                if file.find(".xlsm") != -1:
                
                    if hist[hist['path']==file].empty:
                        
                        vUp.append(os.path.join(path_rel,file))
                        hist  = hist.append({'path':file},ignore_index=True)
            
            elif nome == "smap": # Caso seja o arquivo de previsoes do SMAP
                
                if file.find("EC45") == -1 and file.find("PRECHIST") == -1:# Caso nao possua EC45 no nome do arquivo, nem PRECHIST
                
                    if hist[hist['path']==file].empty:
                        
                        vUp.append(os.path.join(path_rel,file))
                        hist = hist.append({'path':file},ignore_index=True)
            
            elif nome == "smap_ec45": # Caso seja o arquivo de previsoes do SMAP com o ECMWF de 45 dias
                
                if file.find("EC45") != -1:# Caso nao possua EC45 no nome do arquivo
                
                    if hist[hist['path']==file].empty:
                        
                        vUp.append(os.path.join(path_rel,file))
                        hist = hist.append({'path':file},ignore_index=True)
            
            elif nome == "enainter": # Caso seja o arquivo de previsoes do intersemanal
                
                if file.find("ENA-lista") != -1 and file.find("ec45") == -1: # Caso seja o arquivo de ENA correto
                                
                    if hist[hist['path']==file].empty:
                        
                        vUp.append(os.path.join(path_rel,file))
                        hist = hist.append({'path':file},ignore_index=True)
            
            elif nome == "enainter_ec45": # Caso seja o arquivo de previsoes do intersemanal
                
                if file.find("ENA-lista") != -1 and file.find("ec45") != -1: # Caso seja o arquivo de ENA correto (previsao com ECMWF de 45 dias)
                                
                    if hist[hist['path']==file].empty:
                        
                        vUp.append(os.path.join(path_rel,file))
                        hist = hist.append({'path':file},ignore_index=True)
            
            
            elif nome == "chuvaobs": # Caso seja o arquivo de chuva observada
                
                if file.find("prec-med-horaria") != -1: # Caso seja o arquivo de chuva observada horaria
                                
                    if hist[hist['path']==file].empty:
                        
                        vUp.append(os.path.join(path_rel,file))
                        hist = hist.append({'path':file},ignore_index=True)
                        
            elif nome == "rod_gefs": # Caso seja o arquivo de chuva observada
                
                if file.find("prec-med-gefs") != -1: # Caso seja o arquivo de chuva observada horaria
                                
                    if hist[hist['path']==file].empty:
                        
                        vUp.append(os.path.join(path_rel,file))
                        hist = hist.append({'path':file},ignore_index=True)
                        
            elif nome == "carga_sem": # Caso seja o arquivo de carga semanal
                
                if file.find("carga_semanal") != -1 and (file.find(str(self.year)) != -1 or file.find(str(self.year +1)) != -1):
                    
                    if hist[hist['path']==file].empty:
                    
                        vUp.append(os.path.join(path_rel,file))
                        hist = hist.append({'path':file},ignore_index=True)
                        
            elif nome == "vazao_sem": # Caso seja o arquivo de vazao semanal
                
                if file.find("Nao_Consistido_{}".format(self.year)) != -1 or file.find("Nao_Consistido_{}".format(self.year+1)) != -1:
                    
                    if hist[hist['path']==file].empty:
                    
                        vUp.append(os.path.join(path_rel,file))
                        hist = hist.append({'path':file},ignore_index=True)
                        
            elif nome == "pldinter": # Caso seja o arquivo de PLD do intersemanal
                
                if file.find("compila_cmo_medio_20") != -1:
                    
                    if hist[hist['path']==file].empty:
                    
                        vUp.append(os.path.join(path_rel,file))
                        hist = hist.append({'path':file},ignore_index=True)
                        
            elif nome == "carga_mes": # Caso seja o arquivo Carga Mensal

                if file.find("_carga_mensal.zip") != -1:
                
                    if hist[hist['path']==file].empty:
                    
                        vUp.append(os.path.join(path_rel,file))
                        hist  = hist.append({'path':file},ignore_index=True)
                        
            elif nome == "smap_hist": # Caso seja o arquivo Carga Mensal

                if file.find("PRECHIST") != -1:
                
                    if hist[hist['path']==file].empty:
                    
                        vUp.append(os.path.join(path_rel,file))
                        hist  = hist.append({'path':file},ignore_index=True)
                        
            elif nome == 'previvaz': # Caso seja o arquivo do previvaz
                
                if hist[hist['path']==file].empty:
                
                    vUp.append(os.path.join(path_rel,file))
                    hist  = hist.append({'path':file},ignore_index=True)
                    
            elif nome == 'ipdo_pdf': # Caso seja o IPDO PDF
                
                if hist[hist['path']==file].empty and file.find(".pdf") != -1:
                    
                    vUp.append(os.path.join(path_rel,file))
                    hist  = hist.append({'path':file},ignore_index=True)
                    
            elif nome == 'ophen': # Caso seja o OPHEN
                
                if hist[hist['path']==file].empty and file.find(".pdf") != -1:
                    
                    vUp.append(os.path.join(path_rel,file))
                    hist  = hist.append({'path':file},ignore_index=True)
                    
            elif nome == 'repdoe': # Caso seja o REPDOE
                
                if hist[hist['path']==file].empty and file.find(".pdf") != -1:
                    
                    vUp.append(os.path.join(path_rel,file))
                    hist  = hist.append({'path':file},ignore_index=True)
                    
            elif nome == 'oficios': # Caso seja um Oficio
                
                if hist[hist['path']==file].empty and file.find(".pdf") != -1:
                    
                    vUp.append(os.path.join(path_rel,file))
                    hist  = hist.append({'path':file},ignore_index=True)
                    
            elif nome == 'boletim_op': # Caso seja um boletim regulatorio
                
                if hist[hist['path']==file].empty and file.find(".pdf") != -1:
                    
                    vUp.append(os.path.join(path_rel,file))
                    hist  = hist.append({'path':file},ignore_index=True)
                    
            elif nome == "imerg": # Caso seja o arquivo de chuva observada pelo IMERG
                
                if file.find("prec-imerg-bac-horaria") != -1: # Caso seja o arquivo de chuva observada horaria
                                
                    if hist[hist['path']==file].empty:
                        
                        vUp.append(os.path.join(path_rel,file))
                        hist = hist.append({'path':file},ignore_index=True)
            
        df_up = pd.DataFrame(vUp,columns=["path"])       # DataFrame com os caminhos dos relatorios a serem inseridos na base
        hist.to_csv(self.config.paths[nome],index=False) # Reescreve o arquivo de historico com os novos registros
        
        return df_up
    
    def calcula_ena_hist(self):
        '''
        Calcula a ENA da rodada historica do SMAP. Criar arquivos CSV de extracoes
        '''
        
        ena_pass = os.path.join(self.config.paths['extrac'],'ena-diaria-bacia.csv')    # Nome arquivo ENA passada
        ena_hist = os.path.join(self.config.paths['extrac'],'ena-smap-hist-bacia.csv') # Nome arquivo ENA prevista
        vaz_hist = self.config.paths['vazao_historica']                                # Nome arquivo Vazao Historica
        dados_p  = self.config.paths['dados_postos']                                   # Nome arquivo com dados dos postos
        
        # Gerando dados historicos de bacias não-SMAP -----------------------------------
        df_vaz = pd.read_csv(vaz_hist,sep=";",decimal=",")
        df_pst = pd.read_csv(dados_p,sep=";",decimal=",")
        
        df_vaz = df_vaz[df_vaz['ano'] >= 2001].reset_index(drop=True)                # Filtra anos pertinentes
        df_pst = df_pst[['num_posto','num_ssis','num_bacia','bin_ena','val_produt']] # Filtra colunas pertinentes
        
        df_enah = df_vaz.merge(df_pst,on='num_posto',how='inner')       # Merge dos dados de posto com vazoes historicas
        df_enah = df_enah[df_enah['bin_ena']==1].reset_index(drop=True) # Filtrando apenas postos que entram no calculo da ENA
        
        for i in range(1,13): df_enah[str(i)] = df_enah[str(i)] * df_enah['val_produt'] # Transformando vazao em ENA
        
        #df_enah = df_enah[df_enah['num_bacia'].isin([11,17])].reset_index(drop=True)     # Filtra bacias do S.Franc. (NE) e P. do Sul
        df_enah = df_enah[df_enah['num_bacia'].isin([17])].reset_index(drop=True)        # Filtra bacias do S.Franc. (NE)
        df_enah = df_enah.groupby(by=['num_bacia','num_ssis','ano']).sum().reset_index() # Groupby para soma da ENA
        #--------------------------------------------------------------------------------
        
        # Unindo dados realizados e previstos -------------------------------------------
        df_ps = pd.read_csv(ena_pass,sep=";",decimal=",",parse_dates=['dat_medicao'])             # ENA passada por bacia
        df_ht = pd.read_csv(ena_hist,sep=";",decimal=",",parse_dates=['dat_medicao','data_prev']) # ENA historica prevista pelo SMAP, por Bacia
        df_ht = df_ht[df_ht['data_prev'] > df_ps['dat_medicao'].max()].reset_index(drop=True)     # Retirando os dias que ja sao realizados
        
        df_ht['modelo']    = [int(x[-4:]) for x in df_ht['modelo']] # Transformando nome do modelo no numero do ano
        df_ht['data_prev'] = df_ht['data_prev'].dt.date             # Transformando em formato Date
        
        # Criando historico de ENAs por dia --------------------------------------------
        vDados = list()
        for ano in df_ht['modelo'].unique():
            
            for nb in df_enah['num_bacia'].unique():
                
                for dt in df_ht['data_prev'].unique():
                    
                    if dt.year > df_ht.loc[0,'data_prev'].year: # Se o ano for diferente do ano inicial, buscar historico do ano seguinte
                        df_aux = df_enah[(df_enah['ano']==ano+1) & (df_enah['num_bacia']==nb)].reset_index(drop=True)
                    else:
                        df_aux = df_enah[(df_enah['ano']==ano) & (df_enah['num_bacia']==nb)].reset_index(drop=True)
                    
                    vDados.append(dict(
                                    dat_medicao = df_ht['dat_medicao'].max(),
                                    num_ssis    = df_aux.loc[0,'num_ssis'],
                                    num_bacia   = nb,
                                    data_prev   = dt,
                                    modelo      = ano,
                                    val_ena     = df_aux.loc[0,str(dt.month)]
                                    )
                                )
        
        df_hdia = pd.DataFrame(vDados)
        
        df_ht = pd.concat([df_ht,df_hdia],ignore_index=True,sort=False) # Concatena historico com dados de previsao
        #-------------------------------------------------------------------------------
        
        relac = df_ht[['num_ssis','num_bacia']].drop_duplicates().reset_index(drop=True) # Relacao Num. Bacia x Num. Ssis
        df_ps = df_ps.merge(relac,on='num_bacia',how='left')                             # Inclui o numero do subsistema nas ENAs passadas
        df_ps = df_ps[~df_ps['num_ssis'].isnull()].reset_index(drop=True)                # Exclui as bacias que nao sao SMAP
        
        df_ps['dat_medicao'] = df_ps['dat_medicao'].dt.date # Transforma formato datetime em formato date
        
        # Colocando no formato do arquivo com as previsoes -----------------------------
        df_ps['data_prev']   = df_ps['dat_medicao']                            # data_prev = dat_medicao
        df_ps['dat_medicao'] = df_ps['dat_medicao'].max() + timedelta(days=+1) # dat_medicao = dia de publicacao dos dados
        df_ps['modelo']      = "PRECHIST_2001"                                 # Cria coluna modelo para alterar posteriormente
        
        df_ps = df_ps[['dat_medicao','num_ssis','num_bacia','data_prev','modelo','val_ena']] # Reorganiza no mesmo formato
        
        for i,n in enumerate(df_ht['modelo'].unique(),0): # Para cada ano do historico de previsoes
            
            # Altera a coluna 'modelo' e concatena o realizado no previsto
            df_ps['modelo'] = n
            df_ht = pd.concat([df_ht,df_ps],ignore_index=True,sort=False)
        
        # -----------------------------------------------------------------------------
        
        df_ht['nom_hori'] = [ f"{x.year}/{x.month:02d}" for x in df_ht['data_prev']]                            # Criando horizonte baseado no mes de previsao
        df_ht             = df_ht.groupby(by=['num_ssis','num_bacia','modelo','nom_hori']).mean().reset_index() # Groupby por mes de previsao
        df_ht['val_ena']  = df_ht['val_ena'].round(0)                                                           # Arredonda ENA para 0 casas decimais
        
        # Transformando em dados por bacia e ssis -------------------------------------
        df_piv_bac = pd.pivot_table(df_ht, values='val_ena',index=["num_bacia","modelo"],columns=["nom_hori"]).reset_index()            # Pivot Table por bacia
        df_piv_bac.to_csv(os.path.join(self.config.paths['extrac'],"ena-smap-hist-bacia-obs-prev.csv"),sep=";",decimal=",",index=False) # Transforma em CSV
        
        df_ssis     = df_ht.groupby(by=['num_ssis','modelo','nom_hori']).agg(dict(val_ena='sum'))                                       # Groupby por Ssis
        df_piv_ssis = pd.pivot_table(df_ssis, values='val_ena',index=["num_ssis","modelo"],columns=["nom_hori"]).reset_index()          # Pivot Table por Ssis
        df_piv_ssis.to_csv(os.path.join(self.config.paths['extrac'],"ena-smap-hist-ssis-obs-prev.csv"),sep=";",decimal=",",index=False) # Transforma em CSV
        # -----------------------------------------------------------------------------
        
        # Gerando dados estatisticos --------------------------------------------------
        df_med      = df_ssis.groupby(by=['num_ssis','nom_hori']).agg(dict(val_ena='median'))                                                   # Groupby por Ssis, mediana
        df_piv_ssis = pd.pivot_table(df_med, values='val_ena',index=["num_ssis"],columns=["nom_hori"]).reset_index()                            # Pivot Table por Ssis
        df_piv_ssis.to_csv(os.path.join(self.config.paths['extrac'],"ena-smap-hist-ssis-obs-prev-mediana.csv"),sep=";",decimal=",",index=False) # Transforma em CSV
        
        df_std      = df_ssis.groupby(by=['num_ssis','nom_hori']).std()                                                                       # Groupby por Ssis, mediana
        df_piv_ssis = pd.pivot_table(df_std, values='val_ena',index=["num_ssis"],columns=["nom_hori"]).reset_index()                          # Pivot Table por Ssis
        df_piv_ssis.to_csv(os.path.join(self.config.paths['extrac'],"ena-smap-hist-ssis-obs-prev-stdev.csv"),sep=";",decimal=",",index=False) # Transforma em CSV
        # -----------------------------------------------------------------------------
        
        return
    
    def insert_val_previvaz(self,df):
        leitura = Hidrologia(config=config)
        insere  = Banco(config=config)
        
        # Leitura dos dados
        leitura.get_pvv(pvvs=df['path'])
        
        # Insercao no banco de dados
        insere.insert_previvaz(hidro=leitura)
        
    def insert_vaz_semanal(self,df):
        leitura = Hidrologia(config=config)
        insere  = Banco(config=config)
        
        # Leitura dos dados
        leitura.get_vazao_sem(vazaosem=df['path'])
        
        # Insercao no banco de dados
        insere.insert_vazao_sem(hidro=leitura)
    
    def insert_carga_semanal(self,df):
        leitura = Hidrologia(config=config)
        insere  = Banco(config=config)
        
        # Leitura dos dados
        leitura.get_carga_sem(cargasem=df['path'])
        
        # Insercao no banco de dados
        insere.insert_carga_sem(hidro=leitura)
    
    def insert_carga_mensal(self,df):
        leitura = Hidrologia(config=config)
        insere  = Banco(config=config)
        
        # Leitura dos dados
        leitura.get_carga_mes(cargames=df['path'])
        
        # Insercao no banco de dados
        insere.insert_carga_mes(hidro=leitura)
        
    
    def insert_chuvagefs(self,df):
        
        leitura = Hidrologia(config=config)
        insere  = Banco(config=config)
        
        # Leitura dos dados
        leitura.get_chuvagefs(gefs=df['path'])
        
        # Insercao no banco de dados
        insere.insert_gefs(hidro=leitura)
    
    
    def insert_chuvaobservada(self,df):
        
        leitura = Hidrologia(config=config)
        insere  = Banco(config=config)
        
        # Leitura dos dados
        leitura.get_chuvaobs(obs=df['path'])
        
        # Insercao no banco de dados
        insere.insert_chuvaobs(hidro=leitura)
    
    def insert_chuvaimerg(self,df):
        
        leitura = Hidrologia(config=config)
        insere  = Banco(config=config)
        
        # Leitura dos dados
        leitura.get_chuvaimerg(obs=df['path'])
        
        # Insercao no banco de dados
        insere.insert_chuvaimerg(hidro=leitura)
    
    def insert_intersemanal(self,df):
        
        leitura = Hidrologia(config=config)
        insere  = Banco(config=config)
        
        # Leitura dos dados
        leitura.get_enainter(enas=df['path'])
        
        # Insercao no banco de dados
        insere.insert_enainter(hidro=leitura)
    
    def insert_pld_inter(self,df):
        
        leitura = Hidrologia(config=config)
        insere  = Banco(config=config)
        
        # Leitura dos dados
        leitura.get_pldinter(plds=df['path'])
        
        # Insercao no banco de dados
        insere.insert_pldinter(hidro=leitura)
    
    def insert_intersemanal_ec45(self,df):
        
        leitura = Hidrologia(config=config)
        insere  = Banco(config=config)
        
        # Leitura dos dados
        leitura.get_enainter(enas=df['path'])
        
        # Insercao no banco de dados
        insere.insert_enainter_ec45(hidro=leitura)
    
    def insert_val_ipdo(self,df):
        
        leitura = Hidrologia(config=config)
        insere  = Banco(config=config)
        
        # Leitura dos dados
        leitura.get_ipdo(ipdos=df['path'])
        
        # Insercao no banco de dados
        insere.insert_ipdo(hidro=leitura)
    
    def export_val_ipdo(self):
    
        self.date_now()               # Funcao de datas
        export = Banco(config=config) # Objeto com funcao de query
        
        export.query_ipdo(self.now366,self.now1) # Executa Query
        
        df = export.dados_ipdo.round({"ena_ssis":0})
        df.to_csv(os.path.join(self.config.paths['extrac'],"val-ipdo.csv"),sep=";",decimal=",",index=False) # Transformando extracao em CSV
        
        os.system('call "'+self.config.paths['mod_ipdo']+'"') # Abre planilha que edita informacoes de ENA
        while not os.path.isfile(os.path.join(self.config.paths['img_ipdo'],"dados-ipdo-"+self.strDate+".png")):
            time.sleep(1)
            
        # Envio por e-mail ---------------------------------------------------------------------
        destinos  = config.destinos['mesa']
        pathfiles = self.config.paths['img_ipdo']
        esubject  = f"{self.cabecalho_email} Dados IPDO - {self.strDate}"
        message   = "E-mail automatico, favor nao responder."
        remetente = f"{self.remetente}"
        namefiles = ["dados-ipdo-"+self.strDate+".png"]
        
        self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        #---------------------------------------------------------------------------------------
        
        # Armazenamento individualizado --------------------------------------------------------
        
        export.query_arm_ipdo(self.now366, self.now1)
        df = export.dados_arm_ipdo
        df.to_csv(os.path.join(self.config.paths['extrac'],'val-arm-ipdo.csv'),sep=";",decimal=",",index=False,encoding="utf-8-sig") # Transformando extracao em CSV
        
        os.system('call "'+self.config.paths['mod_arm_ipdo']+'"') # Abre planilha que edita informacoes de ENA
        while not os.path.isfile(os.path.join(self.config.paths['img_ipdo'],"dados-arm-ipdo-"+self.strDate+".png")):
            time.sleep(1)
            
        # Envio por e-mail ---------------------------------------------------------------------
        destinos  = config.destinos['mesa']
        pathfiles = self.config.paths['img_ipdo']
        esubject  = f"{self.cabecalho_email} Arm. Historico IPDO - "+self.strDate
        message   = "E-mail automatico, favor nao responder."
        remetente = f"{self.remetente}"
        namefiles = ["dados-arm-ipdo-"+self.strDate+".png"]
        
        self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        #---------------------------------------------------------------------------------------
    
    def insert_prec_merge(self,df):
        
        leitura = Hidrologia(config=config)
        insere  = Banco(config=config)
        
        # Leitura dos dados
        leitura.get_merge(merges=df['path'])
        
        # Insercao no banco de dados
        insere.insert_merge(hidro=leitura)
    
    def export_prec_merge(self):
    
        self.date_now()               # Funcao de datas
        export = Banco(config=config) # Objeto com funcao de query
        
        export.query_merge(self.now6,self.now) # Executa Query
        
        df = export.dados_merge.round({"prec":2})
        df.to_csv(os.path.join(self.config.paths['extrac'],"merge-prec-bacia.csv"),sep=";",decimal=",",index=True) # Transformando extracao em CSV
        
        os.system('call "'+self.config.paths['mod_merge']+'"') # Abre planilha que edita informacoes de ENA
        
        while not os.path.isfile(os.path.join(self.config.paths['img_merge'],"merge-precipitacao-observada-"+self.strDate+".png")):
            time.sleep(1)
        
        # Envio por e-mail ---------------------------------------------------------------------
        destinos = config.destinos['middle_bc']
        pathfiles = self.config.paths['img_merge']
        esubject = f"{self.cabecalho_email} Precipitação Observada - Merge - {self.strDate}"
        message = "E-mail automatico, favor nao responder."
        remetente = f"{self.remetente}"
        namefiles = ["merge-precipitacao-observada-"+self.strDate+".png"]
        
        self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        #---------------------------------------------------------------------------------------
        
    def insert_prec(self,df,modelo):
    
        leitura = Hidrologia(config=config)
        insere  = Banco(config=config)
        
        # Leitura dos dados
        leitura.get_pmedia(pmedias=df['path'],modelo=modelo)
        
        # Insercao no banco de dados
        insere.insert_pmedia(hidro=leitura,modelo=modelo)
        
    def export_prec(self,modelo):
    
        self.date_now()               # Funcao de datas
        export = Banco(config=config) # Objeto com funcao de query
        
        if modelo == "eta+gefs": # O simbolo '+' nao pode ser atribuido ao nome de uma variavel
            modelo2 = "pmedia"
        else:
            modelo2 = modelo
        
        export.query_chuva(self.now1,self.now,modelo) # Executa Query
        
        df = export.dados_ch.round({"prec":2})
        df.to_csv(os.path.join(self.config.paths['extrac'],"prev-prec-bacia-"+modelo2+".csv"),sep=";",decimal=",",index=True) # Transformando extracao em CSV
        
        export.query_chuva(self.now7,self.now,modelo) # Executa Query
        
        df = export.dados_ch.round({"prec":2})
        df.to_csv(os.path.join(self.config.paths['extrac'],"prev-prec-bacia-7-dias-"+modelo2+".csv"),sep=";",decimal=",",index=True) # Transformando extracao em CSV
        
        if modelo == "eta+gefs":
            
            os.system('call "'+self.config.paths['mod_prev']+'"') # Abre planilha que edita informacoes de ENA
            while not os.path.isfile(os.path.join(self.config.paths['img_prev'],"boletim-climatico-"+self.strDate+"-00z.pdf")):
                time.sleep(1)
        
            # Envio por e-mail ---------------------------------------------------------------------
            destinos = config.destinos['mesa']
            pathfiles = self.config.paths['img_prev']
            esubject  = f"{self.cabecalho_email} Previsão de Precipitação - rodada 00z - {self.strDate}"
            message = "E-mail automatico, favor nao responder."
            remetente = f"{self.remetente}"
            #namefiles = ["previsao-precipitacao-ons-"+self.strDate+".png","boletim-climatico-"+self.strDate+"-00z.pdf"]
            namefiles = ["boletim-climatico-"+self.strDate+"-00z.pdf"]
            
            self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
            #---------------------------------------------------------------------------------------
        
        # Extracao Fernanda --------------------------------------------------------------------
        if modelo == "eta+gefs" and self.day ==1: 
            
            self.export_prec_mes()
            
            destinos  = ['alvaro.franca2@gmail.com']
            pathfiles = self.config.paths['extrac']
            esubject  = f"{self.cabecalho_email} Chuva Prevista do Mes - {self.strDate}"
            message   = "Chuva prevista segundo o modelo Conjunto ONS. \n E-mail automatico, favor nao responder."
            remetente = self.remetente
            namefiles = ["chuva-prevista-mes.csv"]
            
            self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        
    def insert_vaz(self,nome,df):
        ''' Nome do relatorio (RDH ou AcompH) e dataframe com os caminhos dos relatorios a serem inseridos '''
        
        leitura = Hidrologia(config=config)
        insere  = Banco(config=config)
        #udb     = UpdateDB()
        
        if nome == "rdh":
            
            # Leitura dos dados
            leitura.get_rdh(rdhs=df['path'], coords=config.config_rdh)
            
            # Insercao no banco de dados
            insere.insert_rdh(hidro=leitura)
            
            # Insercao no banco de dados Access
            # udb.getRdh(path_rdh=df['path'])
            # udb.updateAccess()
   
        else:
            
            for i,n in enumerate(df['path'],0):
                
                # Leitura dos dados
                df = pd.DataFrame([n],columns=["path"])
                leitura.get_acomph(acomphs=df['path'], config_acomph=config.config_acomph)
                
                # Insercao no banco de dados
                insere.insert_acomph(hidro=leitura)
                
                # Insercao no banco de dados Access
                # udb.getAcompH()
    
    def export_vaz(self):
    
        self.date_now()               # Funcao de datas
        export = Banco(config=config) # Objeto com funcao de query
        
        export.query_ena(self.now7,self.now + timedelta(days=-1)) # Executa Query
        
        # Extracao por subsistema --------------------------------------------------------------------------------
        df = export.dados_sub.round({"val_ena":0}).astype({"val_ena":int})                                  # Arredondando valores
        df.to_csv(os.path.join(self.config.paths['extrac'],"ena-diaria-subsistema.csv"),sep=";",index=True) # Transformando extracao em CSV
        #---------------------------------------------------------------------------------------------------------
        
        # Extracao por bacia -------------------------------------------------------------------------------------
        df = export.dados_bac.round({"val_ena":0}).astype({"val_ena":int})                             # Arredondando valores
        df.to_csv(os.path.join(self.config.paths['extrac'],"ena-diaria-bacia.csv"),sep=";",index=True) # Transformando extracao em csv
        #---------------------------------------------------------------------------------------------------------
        
        # Extracao por posto -------------------------------------------------------------------------------------
        df = export.dados_posto.round({"val_ena":0}).astype({"val_ena":int})                                        # Arredondando valores
        df.to_csv(os.path.join(self.config.paths['extrac'],"ena-diaria-posto.csv"),sep=";",index=False,decimal=",") # Transformando extracao em csv
        #---------------------------------------------------------------------------------------------------------
        
        # Extracao para itaipu -----------------------------------------------------------------------------------
        df = export.dados_inc.round({"val_ena":0}).astype({"val_ena":int})                                                 # Arredondando valores
        df = df.round({"val_ena_incr":0}).astype({"val_ena_incr":int})                                                     # Arredondando valores
        df.to_csv(os.path.join(self.config.paths['extrac'],"ena-diaria-posto-itaipu.csv"),sep=";",index=False,decimal=",") # Transformando extracao em csv
        #---------------------------------------------------------------------------------------------------------
        
        os.system('call "'+self.config.paths['mod_ena']+'"') # Abre planilha que edita informacoes de ENA
        while not os.path.isfile(os.path.join(self.config.paths['img_ena'],"Acompanhamento-Hidrologico-"+self.strDate+".png")):
            time.sleep(1)
        
        # Envio por e-mail (Acompanhamento) ----------------------------------------------------
        destinos = config.destinos['mesa']
        pathfiles = self.config.paths['img_ena']
        esubject = f"{self.cabecalho_email} Acompanhamento Hidrologico - {self.strDate}"
        message = "E-mail automatico, favor nao responder."
        remetente = f"{self.remetente}"
        namefiles = ["Acompanhamento-Hidrologico-"+self.strDate+".png"]
        
        self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        #---------------------------------------------------------------------------------------
        #
        #os.system('call "'+self.config.paths['mod_smap']+'"') # Abre planilha que edita informacoes de ENA
        #while not os.path.isfile(os.path.join(self.config.paths['img_smap'],"benchmark-previsoes-smap-"+self.strDate+".pdf")):
        #    time.sleep(1)
        #
        ## Envio por e-mail (Chuva Vazao) -------------------------------------------------------
        #destinos = config.destinos['mesa']
        #pathfiles = self.config.paths['img_smap']
        #esubject = f"{self.cabecalho_email} Benchmark ENAs SMAP - {self.strDate}"
        #message = "E-mail automatico, favor nao responder."
        #remetente = f"{self.remetente}"
        #namefiles = ["benchmark-previsoes-smap-"+self.strDate+".pdf"]
        ##bacias = ["Grande","Paranaiba","Paranapanema-SE","Tiete","Tocantins","Uruguai","Iguacu","Parana","SaoFrancisco-SE","Amazonas-SE","OSul","Tocantins-N"]
        ##for bac in bacias:
        ##    namefiles.append("Previsao-Vazao-"+bac+"-"+self.strDate+".png")
        #
        #self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        ##---------------------------------------------------------------------------------------
        
        # Extracao por posto para 35 dias ------------------------------------------------------------------------
        export.query_vazao_diaria(self.now35, self.now+ timedelta(days=-1)) # Executa Query
        
        df = export.dados_dias.round({"val_ena":0}).astype({"val_ena":int})                                                   # Arredondando valores
        df.to_csv(os.path.join(self.config.paths['extrac'],"vazao-diaria-posto-35-dias.csv"),sep=";",index=False,decimal=",") # Vazao dos ultimos 35 dias em csv
        
        df = export.dados_arm
        df.to_csv(os.path.join(self.config.paths['extrac'],"arm-diario-35-dias.csv"),sep=";",index=False,decimal=",") # Armazenamento por posto dos ultimos 35 dias em csv
        #---------------------------------------------------------------------------------------------------------
    
    def export_arm_rdh(self):
        
        export = Banco(config=config) # Objeto com funcao de query
        
        # Extracao por posto para 35 dias ------------------------------------------------------------------------
        export.query_vazao_diaria(self.now35, self.now+ timedelta(days=-1)) # Executa Query
                
        df = export.dados_arm
        df.to_csv(os.path.join(self.config.paths['extrac'],"arm-diario-35-dias.csv"),sep=";",index=False,decimal=",") # Armazenamento por posto dos ultimos 35 dias em csv
        
        print("Dados de armazenamento exportados com sucesso.")
        #---------------------------------------------------------------------------------------------------------
        
    
    def insert_val_smap(self,df):
    
        leitura = Hidrologia(config=config)
        insere  = Banco(config=config)
        
        # Leitura dos dados
        leitura.get_smap(smaps=df['path'])
        
        # Insercao no banco de dados
        insere.insert_smap(hidro=leitura)
    
    def insert_val_smap_ec45(self,df):
    
        leitura = Hidrologia(config=config)
        insere  = Banco(config=config)
        
        # Leitura dos dados
        leitura.get_smap(smaps=df['path'])
        
        # Insercao no banco de dados
        insere.insert_smap_ec45(hidro=leitura)
        
    def insert_val_smap_hist(self,df):
    
        leitura = Hidrologia(config=config)
        insere  = Banco(config=config)
        
        # Leitura dos dados
        leitura.get_smap(smaps=df['path'])
        
        # Insercao no banco de dados
        insere.insert_smap_hist(hidro=leitura)
        
    def export_val_smap(self,ec45=0,hist=0):
    
        self.date_now()               # Funcao de datas
        export = Banco(config=config) # Objeto com funcao de query
        
        if ec45 != 0: # Caso seja o caso de rodada com o EC45
        
            export.query_smap_ec45(self.now1,self.now)     # Executa Query de vazoes do SMAP com ECMWF45
            export.query_smap_ec45_ena(self.now1,self.now) # Executa Query de ENAs por bacia do SMAP com ECMWF45
            
            df = export.dados_smap_ec45
            df.to_csv(os.path.join(self.config.paths['extrac'],"prev-smap-ec45-posto.csv"),sep=";",decimal=",",index=False) # Transformando extracao em CSV
            df = export.dados_ena_smap_ec45
            df.to_csv(os.path.join(self.config.paths['extrac'],"ena-smap-ec45-bacia.csv"),sep=";",decimal=",",index=False) # Transformando extracao em CSV
            
            return
        
        elif hist != 0: # Caso seja o SMAP historico
            
            export.query_smap_hist(self.now366,self.now)     # Executa Query de vazoes do SMAP historico
            export.query_smap_hist_ena(self.now366,self.now) # Executa Query de ENAs por bacia do SMAP historico
            
            df = export.dados_smap_hist
            df.to_csv(os.path.join(self.config.paths['extrac'],"prev-smap-hist-posto.csv"),sep=";",decimal=",",index=False) # Transformando extracao em CSV
            df = export.dados_ena_smap_hist
            df.to_csv(os.path.join(self.config.paths['extrac'],"ena-smap-hist-bacia.csv"),sep=";",decimal=",",index=False) # Transformando extracao em CSV
            
            self.calcula_ena_hist()
            
            os.system('call "'+self.config.paths['mod_smap_hist']+'"') # Abre planilha que edita informacoes de ENA
            
            while not os.path.isfile(os.path.join(self.config.paths['img_smap_hist'],"Previsoes-SMAP-Historico-"+self.strDate+".pdf")):
                time.sleep(1)
            
            # Envio por e-mail (Chuva Vazao) -------------------------------------------------------
            destinos = config.destinos['mesa']
            pathfiles = self.config.paths['img_smap_hist']
            esubject = f"{self.cabecalho_email} Previsoes SMAP Historico - {self.strDate}"
            message = "E-mail automatico, favor nao responder."
            remetente = f"{self.remetente}"
            namefiles = ["Previsoes-SMAP-Historico-"+self.strDate+".pdf"]
            
            self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
            
            return
        
        elif ec45==0 and hist ==0: # Caso nao seja nem o EC45 nem o Historico
        
            export.query_smap(self.now1,self.now)     # Executa Query de vazoes do SMAP
            export.query_smap_ena(self.now1,self.now) # Executa Query de ENAs por bacia do SMAP
            
            df = export.dados_smap
            df.to_csv(os.path.join(self.config.paths['extrac'],"prev-smap-posto.csv"),sep=";",decimal=",",index=False) # Transformando extracao em CSV
            df = export.dados_ena_smap
            df.to_csv(os.path.join(self.config.paths['extrac'],"ena-smap-bacia.csv"),sep=";",decimal=",",index=False) # Transformando extracao em CSV
        
        check_mod = ['ECMWF','GEFS','PMEDIA_ORIG','zero']
        
        max_data = df['dat_medicao'].max()
        df_aux   = df[df['dat_medicao']==max_data].reset_index(drop=True)
        
        # Envia o E-mail ---------------------------------------------------------------------------
        if df_aux['modelo'].unique().sort() == check_mod.sort(): # Checa se todos os modelos estao disponiveis
            
            os.system('call "'+self.config.paths['mod_smap']+'"') # Abre planilha que edita informacoes de ENA
            
            while not os.path.isfile(os.path.join(self.config.paths['img_smap'],"benchmark-previsoes-smap-"+self.strDate+".pdf")):
                time.sleep(1)
            
            # Envio por e-mail (Chuva Vazao) -------------------------------------------------------
            destinos = config.destinos['mesa']
            pathfiles = self.config.paths['img_smap']
            esubject = f"{self.cabecalho_email} Benchmark ENAs SMAP Preliminar - {self.strDate}"
            message = "E-mail automatico, favor nao responder."
            remetente = f"{self.remetente}"
            namefiles = ["benchmark-previsoes-smap-"+self.strDate+".pdf"]
            #bacias = ["Grande","Paranaiba","Paranapanema-SE","Tiete","Tocantins","Uruguai","Iguacu","Parana","SaoFrancisco-SE","Amazonas-SE","OSul","Tocantins-N"]
            #for bac in bacias:
            #    namefiles.append("Previsao-Vazao-"+bac+"-"+self.strDate+".png")
            
            self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        #-------------------------------------------------------------------------------------------
        
    def export_enainter(self,ec45=0):
        
        self.date_now()
        export = Banco(config=config)
        
        if ec45 == 0:
            export.query_enainter(self.now6,self.now) # Executa query
            namefile = "ena-intersemanal.csv"
        else:
            export.query_enainter(self.now6,self.now,ec45=ec45) # Executa query
            namefile = "ena-intersemanal-ec45.csv"
        
        df = export.dados_enainter
        df.to_csv(os.path.join(self.config.paths['extrac'],namefile),sep=";",decimal=",",index=False) # Transformando extracao em CSV
        
        if ec45 == 0:
            os.system('call "'+self.config.paths['mod_enainter']+'"') # Abre planilha que edita informacoes de ENA
            
            while not os.path.isfile(os.path.join(self.config.paths['img_enainter'],"Previsao-Vazoes-Semanais-Hist-"+self.strDate+".pdf")):
                time.sleep(1)
            
            # Envio por e-mail (Chuva Vazao) -------------------------------------------------------
            destinos = config.destinos['mesa']
            pathfiles = self.config.paths['img_enainter']
            esubject = f"{self.cabecalho_email} Previsao de ENAs Intersemanal - {self.strDate}"
            message = "E-mail automatico, favor nao responder."
            remetente = self.remetente
            namefiles = ["Previsao-Vazoes-Semanais-Hist-"+self.strDate+".pdf","Previsao-Vazoes-Mensais-Hist-"+self.strDate+".pdf","Previsao-Vazoes-Atual-"+self.strDate+".pdf"]
            
            self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
            #-------------------------------------------------------------------------------------------
        
    def export_pldinter(self,ec45=0):
        
        self.date_now()
        export = Banco(config=config)
        
        if calendar.weekday(self.year,self.month,self.day) == 6:
            export.query_pldinter(self.now2,self.now) # Executa query
        else:
            export.query_pldinter(self.now1,self.now) # Executa query
        
        namefile = 'pld-intersemanal.csv'
        
        df = export.dados_pldinter
        df.to_csv(os.path.join(self.config.paths['extrac'],namefile),sep=";",decimal=",",index=False) # Transformando extracao em CSV
        
        if ec45 == 0:
            os.system('call "'+self.config.paths['mod_pldinter']+'"') # Abre planilha que edita informacoes de ENA
            
            while not os.path.isfile(os.path.join(self.config.paths['img_pldinter'],"Previsao-Vazoes-Semanais-Hist-"+self.strDate+".pdf")):
                time.sleep(1)
            
            # Envio por e-mail (Chuva Vazao) -------------------------------------------------------
            destinos = config.destinos['mesa']
            pathfiles = self.config.paths['img_pldinter']
            esubject = f"{self.cabecalho_email} Previsao de ENAs e PLDs Intersemanal - {self.strDate}"
            message = "E-mail automatico, favor nao responder."
            remetente = self.remetente
            namefiles = ["Previsao-Vazoes-Semanais-Hist-"+self.strDate+".pdf","Previsao-Vazoes-Mensais-Hist-"+self.strDate+".pdf"]
            
            self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
            #-------------------------------------------------------------------------------------------
        
        return
        
    def export_chuvaobs(self):
        
        self.date_now()
        export = Banco(config=config)
        
        # Chuva Ultimo Dia ---------------
        export.query_chuvaobs(self.now1,self.now) # Executa query
        
        df = export.dados_chuva_obs
        df.to_csv(os.path.join(self.config.paths['extrac'],"chuva-observada-merge.csv"),sep=";",decimal=",",index=False) # Transformando extracao em CSV
        
        data_max = df['dat_medicao'].max()
        hora_max = df[df['dat_medicao']==data_max]['hora'].max()
        
        print(f"Exportando dados de chuva do Merge para a hora {hora_max}")
        #---------------------------------
        
        # Chuva 7 dias--------------------
        export.query_chuvaobs(self.now7,self.now) # Executa query
        
        df = export.dados_chuva_obs
        df.to_csv(os.path.join(self.config.paths['extrac'],"chuva-observada-merge-7-dias.csv"),sep=";",decimal=",",index=False) # Transformando extracao em CSV
        #---------------------------------
        
        os.system('call "'+self.config.paths['mod_obs']+'"') # Abre planilha que edita informacoes
        
        envia_email = 0
        if hora_max == 9:
            
            os.system('call "'+self.config.paths['mod_comp']+'"') # Abre planilha que edita informacoes
            envia_email=1

        # Envio por e-mail (Chuva Obs) ---------------------------------------------------------
        while not os.path.isfile(os.path.join(self.config.paths['img_obs'],"boletim-chuva-realizada-"+self.strDate+"-"+str(hora_max).zfill(2)+"h.pdf")):
            time.sleep(1)
            
        destinos = config.destinos['mesa']
        pathfiles = self.config.paths['img_obs']
        esubject = f"{self.cabecalho_email} Chuva Realizada - {self.strDate} - {hora_max:02d}h"
        message = "E-mail automatico, favor nao responder."
        remetente = f"{self.remetente}"
        namefiles = ["boletim-chuva-realizada-"+self.strDate+"-"+str(hora_max).zfill(2)+"h.pdf"]
        
        self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        #---------------------------------------------------------------------------------------
        
        # Envio por e-mail (Comparativo) -------------------------------------------------------
        if envia_email == 1:
            while not os.path.isfile(os.path.join(self.config.paths['img_comp'],"Comparativo-Realizado-Previsto-"+self.strDate+".pdf")):
                time.sleep(1)
            
            destinos = config.destinos['mesa']
            pathfiles = self.config.paths['img_comp']
            esubject = f"{self.cabecalho_email} Comparativo de Chuva Realizada x Prevista - {self.strDate}"
            message = "E-mail automatico, favor nao responder."
            remetente = f"{self.remetente}"
            namefiles = ["Comparativo-Realizado-Previsto-"+self.strDate+".pdf"]
            
            self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        
        # Extracao Fernanda --------------------------------------------------------------------
        if self.day == 1 and envia_email == 1:
            self.export_chuvaobs_mes()
            
            destinos  = ["alvaro.franca2@gmail.com"]
            pathfiles = self.config.paths['extrac']
            esubject  = f"{self.cabecalho_email} Chuva Realizada do Mes - {self.strDate}"
            message   = "Chuva realizada segundo o modelo Merge. \n E-mail automatico, favor nao responder."
            remetente = f"{self.remetente}"
            namefiles = ["chuva-observada-mes.csv"]
            
            self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        #---------------------------------------------------------------------------------------
        
        return
        
    def export_chuvaimerg(self):
        
        self.date_now()
        export = Banco(config=config)
        
        # Chuva ultimo dia ------------------
        export.query_chuvaimerg(self.now1,self.now) # Executa query
        
        df = export.dados_chuva_obs_imerg                                                               # Dataframe de dados do IMERG para ultimo dia
        df = df.groupby(by=['dat_medicao','nom_bacia','hora']).agg(dict(val_prec='mean')).reset_index() # Dados medios por hora
        
        df.to_csv(os.path.join(self.config.paths['extrac'],"chuva-observada-imerg.csv"),sep=";",decimal=",",index=False) # Transformando extracao em CSV
        
        data_max = df['dat_medicao'].max()
        hora_max = df[df['dat_medicao']==data_max]['hora'].max()
        
        print(f"Exportando dados de chuva do IMERG para a hora {hora_max}")
        #---------------------------------
        
        # Chuva 7 dias--------------------
        export.query_chuvaimerg(self.now7,self.now) # Executa query
        
        df = export.dados_chuva_obs_imerg                                                               # Dataframe de dados do IMERG para os ult. 7 dias
        df = df.groupby(by=['dat_medicao','nom_bacia','hora']).agg(dict(val_prec='mean')).reset_index() # Dados medios por hora
        
        df.to_csv(os.path.join(self.config.paths['extrac'],"chuva-observada-imerg-7-dias.csv"),sep=";",decimal=",",index=False) # Transformando extracao em CSV
        #---------------------------------
        
        os.system('call "'+self.config.paths['mod_imerg']+'"') # Abre planilha que edita informacoes
        
        # Envio por e-mail (Chuva Obs IMERG) ---------------------------------------------------
        while not os.path.isfile(os.path.join(self.config.paths['img_imerg'],"boletim-chuva-realizada-imerg-"+self.strDate+"-"+str(hora_max).zfill(2)+"h.pdf")):
            time.sleep(1)
            
        destinos = config.destinos['mesa']
        pathfiles = self.config.paths['img_imerg']
        esubject = f"{self.cabecalho_email} Chuva Realizada (IMERG) - {self.strDate} - {hora_max:02d}h"
        message = "E-mail automatico, favor nao responder."
        remetente = f"{self.remetente}"
        namefiles = ["boletim-chuva-realizada-imerg-"+self.strDate+"-"+str(hora_max).zfill(2)+"h.pdf"]
        
        self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        #---------------------------------------------------------------------------------------
        #
        ## Envio por e-mail (Comparativo) -------------------------------------------------------
        #if envia_email == 1:
        #    while not os.path.isfile(os.path.join(self.config.paths['img_comp'],"Comparativo-Realizado-Previsto-"+self.strDate+".pdf")):
        #        time.sleep(1)
        #    
        #    destinos = config.destinos['mesa']
        #    pathfiles = self.config.paths['img_comp']
        #    esubject = f"{self.cabecalho_email} Comparativo de Chuva Realizada x Prevista - {self.strDate}"
        #    message = "E-mail automatico, favor nao responder."
        #    remetente = f"{self.remetente}"
        #    namefiles = ["Comparativo-Realizado-Previsto-"+self.strDate+".pdf"]
        #    
        #    self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        
        return
        
    def export_chuvagefs(self):
        
        self.date_now()
        export = Banco(config=config)
        
        export.query_chuvagefs(self.now1,self.now) # Executa query
        
        df = export.dados_chuva_gefs
        df.to_csv(os.path.join(self.config.paths['extrac'],"chuva-prevista-gefs.csv"),sep=";",decimal=",",index=False) # Transformando extracao em CSV
        
        max_data = df['dat_medicao'].max()
        df_fil   = df[df['dat_medicao']==max_data].reset_index(drop=True)
        rodada   = df_fil['rodada'].max()
        
        os.system('call "'+self.config.paths['mod_rod_gefs']+'"')
        
        while not os.path.isfile(os.path.join(self.config.paths['img_prev'],"boletim-climatico-gefs-{}-{}z.pdf".format(self.strDate,str(rodada).zfill(2)))):
            time.sleep(1)
        
        # Envio por e-mail ---------------------------------------------------------------------
        destinos  = self.config.destinos['mesa']
        pathfiles = self.config.paths['img_prev']
        esubject  = f"{self.cabecalho_email} Previsão de Precipitação GEFS - rodada {rodada:02d}z - {self.strDate}"
        message   = "E-mail automatico, favor nao responder."
        remetente = f"{self.remetente}"
        namefiles = ["boletim-climatico-gefs-{}-{}z.pdf".format(self.strDate,str(rodada).zfill(2))]
        
        self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        #---------------------------------------------------------------------------------------
        #print("E-mail da rodada {} enviado!".format(rodada))
    
    def export_carga_sem(self):
        
        self.date_now()
        export = Banco(config=config)
        
        export.query_carga_sem(self.now35,self.fut9) # Executa query
        
        df = export.dados_carga_sem
        df.to_csv(os.path.join(self.config.paths['extrac'],"carga-semanal.csv"),sep=";",decimal=",",index=False) # Transformando extracao em CSV
        
        max_date = df['data_gera'].max()
        revisao  = df[df['data_gera']==max_date]['revisao'].max()
        
        os.system('call "'+self.config.paths['mod_carga_sem']+'"')
        
        while not os.path.isfile(os.path.join(self.config.paths['img_carga_sem'],"Revisao-Semanal-Carga-{}.png".format(self.strDate))):
            time.sleep(1)
        
        # Envio por e-mail ---------------------------------------------------------------------
        destinos  = self.config.destinos['mesa']
        pathfiles = self.config.paths['img_carga_sem']
        esubject  = f"{self.cabecalho_email} Revisao de Carga Semanal - Revisao {revisao} do mes {max_date.month} - {self.strDate}"
        message   = "E-mail automatico, favor nao responder."
        remetente = f"{self.remetente}"
        namefiles = ["Revisao-Semanal-Carga-{}.png".format(self.strDate)]
        
        self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        #---------------------------------------------------------------------------------------
    
    def export_vaz_sem(self):
        
        self.date_now()
        export = Banco(config=config)
        
        export.query_vazao_sem(self.now35,self.fut8) # Executa query
        
        df = export.dados_vazao_sem
        df.to_csv(os.path.join(self.config.paths['extrac'],"vazao-semanal.csv"),sep=";",decimal=",",index=False) # Transformando extracao em CSV
        
        max_date = df['dat_medicao'].max()
        revisao  = df[df['dat_medicao']==max_date]['revisao'].max()
        
        os.system('call "'+self.config.paths['mod_vazao_sem']+'"')
        
        while not os.path.isfile(os.path.join(self.config.paths['img_vazao_sem'],"Revisao-Semanal-Vazao-{}.png".format(self.strDate))):
            time.sleep(1)
        
        # Envio por e-mail ---------------------------------------------------------------------
        destinos  = self.config.destinos['mesa']
        pathfiles = self.config.paths['img_vazao_sem']
        esubject  = f"{self.cabecalho_email} Revisao de Vazao Semanal - Revisao {revisao} do mes {max_date.month} - {self.strDate}"
        message   = "E-mail automatico, favor nao responder."
        remetente = f"{self.remetente}"
        namefiles = ["Revisao-Semanal-Vazao-{}.png".format(self.strDate)]
        
        self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        #---------------------------------------------------------------------------------------
    
    def export_chuvaobs_mes(self):
        
        self.date_now()
        export = Banco(config=config)
        
        month_ant = self.now62.month
        year_ant  = self.now62.year
        
        lastday_ant = calendar.monthrange(year_ant,month_ant)[1]
        
        data_ini = date(year_ant,month_ant,lastday_ant)
        data_fim = date(self.year,self.month,1)
        
        #-----------------------------------------
        export.query_chuvaobs(data_ini,data_fim) # Executa query
        df = export.dados_chuva_obs
        
        datas_med = df['dat_medicao'].unique().tolist() # Datas do mes
        del datas_med[0]                                # Excluindo data do fim do mes anterior
        del datas_med[len(datas_med)-1]                 # Excluindo data do inicio do mes atual
        
        vDados = list()
        for data in datas_med:
            
            data_pos = data + timedelta(days=+1)
            
            df_aux   = df[(df['dat_medicao']==data) & (df['hora'] >= 8)].reset_index(drop=True)     # Chuva das 9 as 00 do dia
            df_aux_2 = df[(df['dat_medicao']==data_pos) & (df['hora'] <= 8)].reset_index(drop=True) # Chuva das 1 as 8 do dia seguinte
            
            bacias = df_aux['nom_bacia'].unique() # Bacias 
            
            for bacia in bacias:
                
                df_aux_bac   = df_aux[df_aux['nom_bacia']==bacia].reset_index(drop=True)     # Filtra para bacia
                df_aux_bac_2 = df_aux_2[df_aux_2['nom_bacia']==bacia].reset_index(drop=True) # Filtra para bacia
                
                prec = pd.to_numeric(df_aux_bac['val_prec']).sum() + pd.to_numeric(df_aux_bac_2['val_prec']).sum() # Precipitacao
                
                vDados.append(dict(
                                    dat_medicao= data,
                                    nom_bacia  = bacia,
                                    prec       = prec,
                                   )
                             )
        
        df_acumulado = pd.DataFrame(vDados)                                    # Transforma em DF
        df_acumulado = df_acumulado.groupby(['nom_bacia']).sum().reset_index() # Somando valores do dia
        
        for i,n in df_acumulado.iterrows():
            
            if n['nom_bacia'] in ['Grande','Paranaiba','Tiete','Paranapanema','Parana','Madeira']:
                df_acumulado.loc[i,'nom_ssis'] = "SE"
            elif n['nom_bacia'] in ['Iguacu','OSUL','Uruguai']:
                df_acumulado.loc[i,'nom_ssis'] = "S"
            elif n['nom_bacia'] in ['SaoFrancisco']:
                df_acumulado.loc[i,'nom_ssis'] = "NE"
            else:
                df_acumulado.loc[i,'nom_ssis'] = "N"
        
        df_acumulado = df_acumulado.groupby(['nom_ssis']).mean().reset_index()
        df_acumulado.to_csv(os.path.join(self.config.paths['extrac'],"chuva-observada-mes.csv"),sep=";",decimal=",",index=False) # Transformando extracao em CSV
        
        #---------------------------------------------------------------------------------------
        
    def export_prec_mes(self):
    
        self.date_now()               # Funcao de datas
        export = Banco(config=config) # Objeto com funcao de query
        
        month_ant = self.now62.month
        year_ant  = self.now62.year
        
        lastday_ant = calendar.monthrange(year_ant,month_ant)[1]
        
        data_ini = date(year_ant,month_ant,lastday_ant)
        data_fim = date(self.year,self.month,1) + timedelta(days=-2)
        
        export.query_chuva(data_ini,data_fim,"eta+gefs") # Executa Query
        
        df = export.dados_ch.round({"prec":2}).reset_index()
        
        datas_med = df['data_gera'].unique().tolist() # Datas do mes
        
        vDados = list()
        for data in datas_med:
            
            data_pos = data + timedelta(days=+1)
            df_aux = df[(df['data_gera']==data) & (df['data_prev']==data_pos)].reset_index(drop=True) # Data previsao = Data de Geração -1
            
            bacias = df_aux['nom_bacia'].unique() # Bacias do modelo
            
            for bacia in bacias: 
                
                df_aux_bac = df_aux[df_aux['nom_bacia']==bacia].reset_index()
                
                prec = df_aux_bac['prec'].sum()
                
                vDados.append(dict(
                                    data_prev = data_pos,
                                    nom_bacia = bacia,
                                    prec      = prec,
                                   )
                             )
               
        df_acumulado = pd.DataFrame(vDados)
        df_acumulado = df_acumulado.groupby(['nom_bacia']).sum().reset_index() # Somando valores do dia
        
        for i,n in df_acumulado.iterrows():
            
            if n['nom_bacia'] in ['Grande','Paranaiba','Tiete','Paranapanema','Parana','Madeira']:
                df_acumulado.loc[i,'nom_ssis'] = "SE"
            elif n['nom_bacia'] in ['Iguacu','OSUL','Uruguai']:
                df_acumulado.loc[i,'nom_ssis'] = "S"
            elif n['nom_bacia'] in ['SaoFrancisco']:
                df_acumulado.loc[i,'nom_ssis'] = "NE"
            else:
                df_acumulado.loc[i,'nom_ssis'] = "N"
        
        df_acumulado = df_acumulado.groupby(['nom_ssis']).mean().reset_index()
        df_acumulado.to_csv(os.path.join(self.config.paths['extrac'],"chuva-prevista-mes.csv"),sep=";",decimal=",",index=False) # Transformando extracao em CSV
        #---------------------------------------------------------------------------------------
        
    def export_carga_mes(self):
        
        self.date_now()
        export = Banco(config=config)
        
        export.query_carga_mes(self.now35,self.now) # Executa query
        
        df = export.dados_carga_mes
        df.to_csv(os.path.join(self.config.paths['extrac'],"carga-mensal.csv"),sep=";",decimal=",",index=False) # Transformando extracao em CSV
        
        max_date =  df['data_gera'].max() + timedelta(days=+10)
        
        os.system('call "'+self.config.paths['mod_carga_mes']+'"')
        
        while not os.path.isfile(os.path.join(self.config.paths['img_carga_mes'],"carga-mensal-pmo-{}.png".format(self.strDate))):
            time.sleep(1)
            print(os.path.join(self.config.paths['img_carga_mes'],"carga-mensal_pmo-{}.png".format(self.strDate)))
        
        # Envio por e-mail ---------------------------------------------------------------------
        destinos  = self.config.destinos['mesa']
        pathfiles = self.config.paths['img_carga_mes']
        esubject  = f"{self.cabecalho_email} Revisao de Carga Mensal - PMO do mes {max_date.month}"
        message   = "E-mail automatico, favor nao responder."
        remetente = f"{self.remetente}"
        namefiles = ["carga-mensal-pmo-{}.png".format(self.strDate)]
        
        self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        #---------------------------------------------------------------------------------------
    
    def export_previvaz(self):
        
        self.date_now()
        export = Banco(config=config)
        
        export.query_previvaz(self.now35,self.now,ano_inicial=2001) # Executa query
        
        df = export.dados_pvv
        df.to_csv(os.path.join(self.config.paths['extrac'],"historico-previvaz.csv"),sep=";",decimal=",",index=False) # Transformando extracao em CSV
        
    def export_ipdo_pdf(self,df_up):
        '''
        Envia os novos relatorios do IPDO (PDF)
        
        :df_up: Dataframe, nome dos arquivos novos a serem enviados
        '''
        
        self.date_now()
        
        # Envio por e-mail ---------------------------------------------------------------------
        destinos  = self.config.destinos['mesa']
        pathfiles = self.config.paths['paths_ipdo_pdf']
        esubject  = f"{self.cabecalho_email} IPDO PDF - {self.strDate}"
        message   = "E-mail automatico, favor nao responder."
        remetente = f"{self.remetente}"
        namefiles = [x.rsplit('\\',1)[-1] for x in df_up['path']]
        
        self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        #---------------------------------------------------------------------------------------
        
    def export_ophen(self,df_up):
        '''
        Envia os novos relatorios do OPHEN
        
        :df_up: Dataframe, nome dos arquivos novos a serem enviados
        '''
        
        self.date_now()
        
        # Envio por e-mail ---------------------------------------------------------------------
        destinos  = self.config.destinos['mesa']
        pathfiles = self.config.paths['paths_ophen']
        esubject  = f"{self.cabecalho_email} OPHEN - {self.strDate}"
        message   = "E-mail automatico, favor nao responder."
        remetente = f"{self.remetente}"
        namefiles = [x.rsplit('\\',1)[-1] for x in df_up['path']]
        
        self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        #---------------------------------------------------------------------------------------
        
    def export_repdoe(self,df_up):
        '''
        Envia os novos relatorios do REPDOE
        
        :df_up: Dataframe, nome dos arquivos novos a serem enviados
        '''
        
        self.date_now()
        
        # Envio por e-mail ---------------------------------------------------------------------
        destinos  = self.config.destinos['mesa']
        pathfiles = self.config.paths['paths_repdoe']
        esubject  = f"{self.cabecalho_email} REPDOE - {self.strDate1}"
        message   = "E-mail automatico, favor nao responder."
        remetente = f"{self.remetente}"
        namefiles = [x.rsplit('\\',1)[-1] for x in df_up['path']]
        
        self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        #---------------------------------------------------------------------------------------
        
    def export_oficios(self,df_up):
        '''
        Envia os novos oficios publicados no SINtegre
        
        :df_up: Dataframe, nome dos arquivos novos a serem enviados
        '''
        
        self.date_now()
        
        # Envio por e-mail ---------------------------------------------------------------------
        destinos  = self.config.destinos['mesa']
        pathfiles = self.config.paths['paths_oficios']
        esubject  = f"{self.cabecalho_email} Novo Oficio - {self.strDate}"
        message   = "E-mail automatico, favor nao responder."
        remetente = f"{self.remetente}"
        namefiles = [x.rsplit('\\',1)[-1] for x in df_up['path']]
        
        self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        #---------------------------------------------------------------------------------------
        
    def export_boletim_op(self,df_up):
        '''
        Envia os novos Boletins Regulatorios publicados no SINtegre
        
        :df_up: Dataframe, nome dos arquivos novos a serem enviados
        '''
        
        self.date_now()
        
        # Envio por e-mail ---------------------------------------------------------------------
        destinos  = self.config.destinos['mesa']
        pathfiles = self.config.paths['paths_boletim_op']
        esubject  = f"{self.cabecalho_email} Boletim Regulatorio - {self.strDate}"
        message   = "E-mail automatico, favor nao responder."
        remetente = f"{self.remetente}"
        namefiles = [x.rsplit('\\',1)[-1] for x in df_up['path']]
        
        self.func_envia_email(destinos, pathfiles, esubject, message ,remetente, namefiles)
        #---------------------------------------------------------------------------------------
        
#-------------------------------------------------------------------------------------------------------------------------------

