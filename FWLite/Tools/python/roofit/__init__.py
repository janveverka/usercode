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

#______________________________________________________________________________
def silence():
    '''
    Turns of RooFit messages.
    '''
    msgservice = ROOT.RooMsgService.instance()
    roo = ROOT.RooFit
    msgservice.setSilentMode(True)
    msgservice.getStream(0).removeTopic(roo.Caching)
    msgservice.getStream(1).removeTopic(roo.Caching)
    msgservice.getStream(0).removeTopic(roo.Minimization)
    msgservice.getStream(1).removeTopic(roo.Minimization)
    msgservice.getStream(0).removeTopic(roo.Plotting)
    msgservice.getStream(1).removeTopic(roo.Plotting)
    msgservice.getStream(0).removeTopic(roo.Fitting)
    msgservice.getStream(1).removeTopic(roo.Fitting)
    msgservice.getStream(0).removeTopic(roo.Eval)
    msgservice.getStream(1).removeTopic(roo.Eval)
    msgservice.getStream(0).removeTopic(roo.Integration)
    msgservice.getStream(1).removeTopic(roo.Integration)

    msgservice.setStreamStatus(0, False)
    msgservice.setStreamStatus(1, False)
## End of silence()  