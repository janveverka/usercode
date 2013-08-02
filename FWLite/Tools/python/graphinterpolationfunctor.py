"""
Impoorts the custom ROOT class GraphInterpolationFunctor in PyROOT.
  Usage:
  import ROOT
  from array import array
  from FWLite.Tools.graphinterpolationfunctor import GraphInterpolationFunctor
  graph = ROOT.TGraph(array('d', [0,1]), array('d', [0, 2]))
  f = GraphInterpolationFunctor(graph)
  print 'x     f(x)'
  for x in [0.1 * i for i in range(11)]:
      print x, '  ', f(x) 
"""

import ROOT
## The order of the following two lines matters!
import FWLite.Tools
ROOT.gROOT.ProcessLine('#include "FWLite/Tools/interface/GraphInterpolationFunctor.h"')

GraphInterpolationFunctor = ROOT.GraphInterpolationFunctor

#______________________________________________________________________________
def test():
    '''
    Tests the GraphInterpolationFunctor.
    '''
    from array import array
    graph = ROOT.TGraph(2, array('d', [0,1]), array('d', [0, 2]))
    f = GraphInterpolationFunctor(graph)
    print "x     f(x)"
    for x in [0.1 * i for i in range(11)]:
        print x, '  ', f(x) 
## End of test()


#______________________________________________________________________________
if __name__ == '__main__':
    test()
    import user
    
