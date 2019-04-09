#!/usr/bin/env python3

import os, sys
import subprocess
import appscript
import platform
from plat_definer import *

os.chdir(os.path.dirname(__file__))
#print(os.getcwd())
cmd = 'python3 {}/after_login.py'.format(os.getcwd())
plat = Plat_define()
platform = plat.use_platform()
if platform == 'mac':
	appscript.app('Terminal').do_script(cmd)
elif platform == 'windows':
	subprocess.call('start "" {}'.format(cmd), shell=True)
elif platform == 'linux':
    subprocess.call(['gnome-terminal', '-x', cmd])
else:
    pass



