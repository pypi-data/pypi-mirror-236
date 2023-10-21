from . import *
from . import configmodule, initconfig
if configmodule.initdone == False:
   initconfig.initconfig()