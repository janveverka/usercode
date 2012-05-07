'''
Test the extraction of the mode and effective sigma
using parametrized KEYS PDF.

1. Create a mohter PDF of known location and width
2. Draw a toy sample of the mother PDF
3. Use parametrized KEYS PDF to extract the mode and effective sigma
4. Compare the estimate with the true
5. Repeat 2-4 for a number of toys.
6. Plot the distribution of residuals and pulls for the mode and eff. sigma
7. Plot the distribution of the statistical errors of the mode and eff. sigma
8. Repeat for different mother PDF.  Try Gaussian, Breit-Wigner, Landau, Log-normal
   Binomial.
'''

import os
import ROOT
import FWLite.Tools.roofit as roo

import FWLite.Tools.cmsstyle as cmsstyle
import FWLite.Tools.canvases as canvases
import FWLite.Tools.legend as legend
import FWLite.Tools.latex as latex

from FWLite.Tools.parameterizedkeyspdf import ParameterizedKeysPdf


#______________________________________________________________________________
class ToyFitter:
    '''
    Holds data associated with the MC toys.
    '''
    #__________________________________________________________________________
    def __init__(self):
        pass
    ## End of __init__(...) 
## End of ToyFitter


#______________________________________________________________________________
def main():
    '''This is the entry point to execution.'''
    print 'Welcome to test_pkeys - test of the mode and effective sigma'
    print 'extraction for a generic distribution using ParametrizedKeysPdf.'
    
    w = ROOT.RooWorkspace('w', 'w')
    
    truepdf = w.factory('Gaussian::truepdf(x[-5,5],m[0],s[1])')
    data = truepdf.generate(ROOT.RooArgSet(w.var('x')), 10000)
    canvases.next('truepdf')
    plot = w.var('x').frame()
    data.plotOn(plot)
    truepdf.plotOn(plot)
    plot.Draw()
    
    toypdf = ParameterizedKeysPdf('toypdf', 'toypdf', w.var('x'), 
                                  w.factory('mtoy[0,-5,5]'), 
                                  w.factory('stoy[1,0.1,5]'), data, rho=3)
    toypdf.shape.plotOn(plot, roo.LineColor(ROOT.kRed))
    toypdf.fitTo(data)
    toypdf.plotOn(plot, roo.LineColor(ROOT.kGreen))
    plot.Draw()
        
    
    canvases.update()
    print 'Exiting test_pkeys with success!'
## End of main().


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user

## End of this module
