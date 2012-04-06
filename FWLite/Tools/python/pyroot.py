##! /usr/bin/env python
'''
pyroot.py
---------
pyroot aims at being to PyROOT as root is to ROOT.
The main difference between pyroot and root is that pyroot 
gives you the python interpreter instead of CINT.
Eventually, it should respond to the command-line options and
arguments exactly the same way as ROOT does.
'''
## TODO: Use the optparse module to parse the command-line options
## and arguments.

import os
import sys
import user

from ROOT import *
import FWLite.Tools.roofit as RooFit

_main = sys.modules[__name__]

for arg in sys.argv:
    if os.path.exists(arg):
        ext = os.path.splitext(arg)[-1]
        ## Open the root files and attach them.
        if ext == '.root':
            nfiles = len(gROOT.GetListOfFiles())
            print 'Attaching %s as _file%d' % (arg, nfiles)
            setattr(_main, '_file%d' % nfiles, TFile.Open(arg))


