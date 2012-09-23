import re
import sys
import ROOT

_titlePattern = re.compile("^[A-Z]")

### Black Magic to Make RooFit work on MacOS X --------------------------------
if sys.platform == 'darwin':
    try:
        import libRooFit
    except ImportError:
        pass

### Rename the RooWorkspace::import method to avoid conflict with Python--------
setattr(ROOT.RooWorkspace, 'Import', getattr(ROOT.RooWorkspace, 'import'))

### Rename the RooAbsData::reduce method to avoid conflict with Python--------
# setattr(ROOT.RooAbsData, 'Reduce', getattr(ROOT.RooAbsData, 'reduce'))

### Define all the callable attributes of ROOT.RooFit
for method in dir(ROOT.RooFit):
    if callable(getattr(ROOT.RooFit, method)) and re.search(_titlePattern, method):
        if method in vars():
            print "% not imported since it already exists!" % method
        else:
            setattr(sys.modules[__name__], method, getattr(ROOT.RooFit, method))

