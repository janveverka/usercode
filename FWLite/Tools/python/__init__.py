#Automatically created by SCRAM
import os
__path__.append(os.path.dirname(os.path.abspath(__file__).rsplit('/FWLite/Tools/',1)[0])+'/cfipython/osx106_amd64_gcc421/FWLite/Tools')

## Added to be able to use custom ROOT classes defined in this package
import ROOT

if 'CMSSW_BASE' not in os.environ:
    raise RuntimeError, "Run `cmsenv' first!"

lib_name = 'libFWLiteTools'
include_path = os.path.join(os.environ['CMSSW_BASE'], 'src')

print "INFO:", __name__, "loading `%s'" % lib_name
ROOT.gSystem.Load(lib_name)

if include_path not in ROOT.gSystem.GetIncludePath():
    print "INFO:", __name__, 
    print ": Adding `%s' to the include path." % include_path
    ROOT.gROOT.ProcessLine('.include %s' % include_path)

