#!/usr/bin/env python
#*- coding: utf-8 -*-
import os
from datetime import datetime, date, timedelta

    
class Config(object):
    
    def __init__(self):
        
        cwdPath = os.getcwd() # Diretorio atual
        
        self.version = 1
        
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
        
        self.tables = dict(
            path = os.path.join(os.getcwd(),"tabelas"),
            tbl_deriv             ='tbl_deriv.csv',
            tbl_diesel            ='tbl_diesel.csv',
        )
    
        self.paths = dict(
            app                  = cwdPath,
        )
    
        self.config_acomph = dict(
            row=[6, 35],
            bloco_dados=8
        )
    
        self.config_rdh = dict(
            row=[8, 172],
            col=[1, 28]
        )
        
        self.control = dict(
            time_gap    = 5.0,
            hour_check  = 16,
            num_semana  = date(datetime.now().year,12,28).isocalendar()[1],
        )
        
        self.cabecalho = \
        f'#----------------------------------------------------------------------------------#\n' + \
        f'#                                       BI-ETL                                     #\n' + \
        f'#                    Gestor de ETLs e emissao de relatorios - v.{self.version}                 #\n' + \
        f'#----------------------------------------------------------------------------------#\n'