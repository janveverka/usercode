##! /usr/bin/env python
'''
pyroot.py
---------
pyroot aims at being to PyROOT as root is to ROOT.
The main difference between pyroot and root is that pyroot 
gives you the python interpreter instead of CINT.
Eventually, it should respond to the command-line options and
arguments exactly the same way as ROOT does.

This python script is intended to be called by the shell script
`FWLite/Tools/scripts/pyroot'.
'''
## TODO: Use the optparse module to parse the command-line options
## and arguments.

import os
import sys
import user

from ROOT import *
import FWLite.Tools.roofit as RooFit

_main = sys.modules[__name__]

## Loop over command-line arguments for the files:
for arg in sys.argv[1:]:
  
    ## Skip options
    if arg[0] == '-':
        continue
    filename = arg.strip('+')
    ext = os.path.splitext(filename)[-1]
    
    ## Open the root files and attach them:
    if ext == '.root':
        if not os.path.exists(filename):
            print 'Warning in pyroot: file %s not found!' % filename
            continue
        nfiles = len(gROOT.GetListOfFiles())
        print 'Attaching %s as _file%d' % (filename, nfiles)
        setattr(_main, '_file%d' % nfiles, TFile.Open(filename))
    
    ## Process python macros:
    elif ext == '.py':
        if not os.path.exists(filename):
            print 'Warning in pyroot: macro %s not found!' % filename
            continue
        print 'Processing %s...' % filename
        execfile(filename)
        
    ## Process ROOT macros:
    else:
        if not os.path.exists(filename):
            print 'Warning in pyroot: macro %s not found!' % filename
            continue
        print 'Processing %s...' % filename
        gROOT.ProcessLine('.x ' + arg)

## Check for the exit option:
if '-q' in sys.argv:
    exit()
