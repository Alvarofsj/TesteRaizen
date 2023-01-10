import os
import sys

# Insert folder into system path -----------
cwdPath = os.path.dirname(__file__)
sys.path.append(cwdPath)
#-------------------------------------------

# Insert modules from folder ---------------
from Control import *
#-------------------------------------------