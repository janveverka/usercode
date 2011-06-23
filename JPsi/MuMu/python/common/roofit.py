import re
import sys
import ROOT

_titlePattern = re.compile("^[A-Z]")

for method in dir(ROOT.RooFit):
    if callable(getattr(ROOT.RooFit, method)) and re.search(_titlePattern, method):
        if hasattr(sys.modules[__name__], method):
            print "% not imported since it already exists!" % method
        else:
            setattr(sys.modules[__name__], method, getattr(ROOT.RooFit, method))
