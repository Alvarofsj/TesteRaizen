#!/usr/bin/env python
#*- coding: utf-8 -*-

import os
from datetime import datetime, date, timedelta

    
class Config(object):
    
    def __init__(self):
        
        cwdPath = os.getcwd() # Diretorio atual
        
        self.version = 1 # Versao atual
        
        self.link_download = "https://github.com/raizen-analytics/data-engineering-test/raw/master/assets/vendas-combustiveis-m3.xls"
        
        self.config_banco = dict(
            user    ='admin',
            password="",
            host    =os.path.join(os.getcwd(),"fuels.db"),
            database='fuels',
            port    =3306,
            raise_on_warnings=True,
            get_warnings     =True,
        )
        
        self.string_engine = f'sqlite:///{self.config_banco["host"]}' # String de conexão com o banco
        
        # Tabelas do BD
        self.tabelas = dict(
            deriv  = 'tbl_deriv',  # Tabela para dados de derivados do petroleo
            diesel = 'tbl_diesel', # Tabela para dados de diesel
            )
        # String de Busca
        self.str_busca = dict(
            diesel="Vendas, pelas distribuidoras¹, de óleo diesel por tipo e Unidade da Federação",
            deriv="Vendas, pelas distribuidoras¹, dos derivados combustíveis de petróleo por Unidade da Federação e produto",
        )
        
        # Filtros de Dados
        self.filtros = dict(
            diesel=["UN. DA FEDERAÇÃO","PRODUTO"],
            deriv=["UN. DA FEDERAÇÃO","PRODUTO"],
        )
        
        # Caminhos padrao
        self.paths = dict(
            app                  = cwdPath,
            path_download = os.path.join(cwdPath,"downloads"), # Caminho para downloads
            path_temp     = os.path.join(cwdPath,"tmp"),       # Caminho para pasta temporaria
        )
        
        # Nome do arquivo a ser baixado
        self.namefiles = dict(
            dwn_file = 'vendas-combustiveis-m3.xls',
        )
        
        # Numero dos meses
        self.mes_dict = dict(Janeiro = 1, Fevereiro=2, Março=3, 
            Abril=4, Maio=5, Junho=6, Julho=7, Agosto=8, Setembro=9, Outubro=10, Novembro=11, Dezembro=12
        )
        
        self.control = dict(
            time_gap    = 5.0,
        )
        
        self.cabecalho = \
        f'#----------------------------------------------------------------------------------#\n' + \
        f'#                                       BI-ETL                                     #\n' + \
        f'#                    Gestor de ETLs e emissao de relatorios - v.{self.version}                 #\n' + \
        f'#----------------------------------------------------------------------------------#\n'