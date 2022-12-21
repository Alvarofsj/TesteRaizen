import os
import sys

# Insert folder into system path -----------
cwdPath = os.getcwd()
dbPath  = os.path.join(cwdPath,"database")
sys.path.append(dbPath)
#-------------------------------------------

# Insert modules from folder ---------------
from database.config import *
from database.Banco import *
from database.Postos import *
from database.Rotinas import *
#-------------------------------------------