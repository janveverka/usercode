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

DummyIntRootClass  = ROOT.fwlite.DummyIntRootClass
DummyIntRootClass2 = ROOT.fwlite.DummyIntRootClass2
DummyIntRootClass3 = ROOT.fwlite.DummyIntRootClass3
DummyIntRootClass4 = ROOT.fwlite.DummyRootClassTemplate("Int_t")

#______________________________________________________________________________
def test():
    '''
    Tests the DummyRootClassTemplate.
    '''
    dummies = [DummyIntRootClass (1),
               DummyIntRootClass2(2),
               DummyIntRootClass3(3),
               DummyIntRootClass4(4),]
    for dummy in dummies:
        print dummy.Class_Name(), " ",
        dummy.printData()

## End of test()


#______________________________________________________________________________
if __name__ == '__main__':
    test()
    import user
    
