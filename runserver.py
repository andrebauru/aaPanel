#coding: utf-8
# +-------------------------------------------------------------------
# | aaPanel
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2099 aaPanel(www.aapanel.com) All rights reserved.
import sys
import os
from types import ModuleType

# Mock chdir for Linux-specific path
workspace_dir = os.path.dirname(os.path.abspath(__file__))
original_chdir = os.chdir
def safe_chdir(path):
    norm_path = str(path).replace('\\', '/').rstrip('/')
    if norm_path == '/www/server/panel':
        path = workspace_dir
    elif '/www/server/panel/' in str(path) or str(path).startswith('/www/server/panel/'):
        path = str(path).replace('/www/server/panel', workspace_dir)
    try:
        original_chdir(path)
    except Exception:
        try:
            original_chdir(workspace_dir)
        except Exception:
            pass

os.chdir = safe_chdir

# Mock fcntl for Windows
if sys.platform == 'win32':
    class MockFcntl(ModuleType):
        LOCK_SH = 1
        LOCK_EX = 2
        LOCK_NB = 4
        LOCK_UN = 8
        def flock(self, fd, op):
            pass
        def ioctl(self, fd, op, arg=0, mutate_flag=False):
            return 0
    sys.modules['fcntl'] = MockFcntl('fcntl')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'class')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'class_v2')))

from os import environ
from BTPanel import app,sys

if __name__ == '__main__':
    f = open('data/port.pl')
    PORT = int(f.read())
    HOST = '0.0.0.0'
    f.close()
    app.run(host=HOST,port=PORT)
