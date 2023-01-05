# !/usr/bin/env python
# *- coding: utf-8 -*-

import os
from Control  import *
from database import *

config = Config()
ctl = Control(config)

ctl.download_new()
ctl.get_insert_val()