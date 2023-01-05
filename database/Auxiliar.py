# !/usr/bin/env python
# *- coding: utf-8 -*-

import os
from datetime import datetime, date, timedelta

class Auxiliar():
    
    def __init__(self):
        pass
        
    def anota(self,texto):
        ''' 
        Anota o texto em questao no arquivo de LOG 
        
        Returns: None
        '''
        
        # Data e hora do log -----------------------------
        now = datetime.now()
        data = now.date()
        hora = now.hour
        minu = now.minute
        
        strNow = f'{data}-{hora:02d}:{minu:02d}'
        #-------------------------------------------------
        
        # Backup Logs ------------------------------------
        if (now.day == 2) and (os.path.isfile(f"logs_{data}.zip") == False):# Apenas no segundo dia do mes
            
            zf = ZipFile(f"logs_{now.date()}.zip",'w', compression=ZIP_DEFLATED,compresslevel=9)
            zf.write("logs.txt")
            zf.close()
            
            os.remove("logs.txt") # Remove arquivo compactado
        #-------------------------------------------------
        
        logsv = open(os.path.join(os.getcwd(),"logs.txt"),"a")
        logsv.write(f'{strNow} - {texto}\n')
        logsv.close()
        
        return