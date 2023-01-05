# !/usr/bin/env python
# *- coding: utf-8 -*-

import os, calendar
import sys
import pandas as pd
import time

from datetime import datetime, date, timedelta
from database import *

strPath = os.getcwd()

class Control(object):
        
    def __init__(self, config):
        self.config = config
        self.rotinas = Rotinas()
        pass
    
    def download_new(self):
        
        self.rotinas.download_data()
        
        return
    
    def get_insert_val(self):
        
        # Obtem dados
        self.rotinas.get_data()
        
        return
