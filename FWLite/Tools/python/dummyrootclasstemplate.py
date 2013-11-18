# -*- coding: utf-8 -*-
"""
Impoorts the custom ROOT class DummyRootClass in PyROOT.
  Usage:
  from FWLite.Tools.dummyrootclasstemplate import DummyRootClassTemplate
  idummy = DummyRootClassTemplate("Int_t")()
  fdummy = DummyRootClassTemplate("Float_t")()
  idummy.print()
  fdummy.print()
"""

import ROOT
import FWLite.Tools

DummyRootClassTemplate = ROOT.fwlite.DummyRootClassTemplate

#______________________________________________________________________________
def test():
    '''
    Tests the DummyRootClassTemplate.
    '''
    idummy = DummyRootClassTemplate("Int_t")(123)
    fdummy = DummyRootClassTemplate("Float_t")(4.56)
    idummy.printData()
    fdummy.printData()
## End of test()


#______________________________________________________________________________
if __name__ == '__main__':
    test()
    import user
    
