"""
Impoorts the custom ROOT class Double32IOEmulator in PyROOT.
  Usage:
  from FWLite.Tools.double32ioemulator import Double32IOEmulator
  reduce_precision = Double32IOEmulator()
  pi = 3.1415926535897931
  print 'pi:', pi
  print 'reduced-precision pi:', reduce_precision(pi)
"""

import ROOT
## The order of the following two lines matters!
import FWLite.Tools
# ROOT.gROOT.ProcessLine('#include "FWLite/Tools/interface/Double32IOEmulator.h"')

Double32IOEmulator = ROOT.Double32IOEmulator

#______________________________________________________________________________
def test():
    '''
    Tests the Double32IOEmulator.
    '''
    reduce_precision = Double32IOEmulator()
    pi = 3.1415926535897931
    print 'pi:', pi
    print 'reduced-precision pi:', reduce_precision(pi)    
## End of test()


#______________________________________________________________________________
if __name__ == '__main__':
    test()
    import user
    
