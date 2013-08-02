"""
Impoorts the custom ROOT class DummyRootClass in PyROOT.
  Usage:
  from FWLite.Tools.dummyrootclass import DummyRootClass
  dummy = DummyRootClass()
  dummy.about()
"""

import ROOT
## The order of the following two lines matters!
import FWLite.Tools
ROOT.gROOT.ProcessLine('#include "FWLite/Tools/interface/DummyRootClass.h"')

DummyRootClass = ROOT.DummyRootClass

#______________________________________________________________________________
def test():
    '''
    Tests the DummyRootClass.
    '''
    dummy = DummyRootClass()
    dummy.about()
## End of test()


#______________________________________________________________________________
if __name__ == '__main__':
    test()
    import user
    
