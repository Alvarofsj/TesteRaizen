# !/usr/bin/env python
# *- coding: utf-8 -*-

import os

from Control  import *
from database import *

def main_call():
    config = Config()
    ctl = Control(config)
    
    ctl.download_new()
    ctl.get_insert_val()
    
if __name__ == '__main__':
    main_call()