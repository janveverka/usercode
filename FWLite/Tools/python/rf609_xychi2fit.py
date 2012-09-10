'''
This is a PyROOT version of 
rf609_xychi2fit.C: 'LIKELIHOOD AND MINIMIZATION' RooFit tutorial macro #609
See original at:
http:##root.cern.ch/root/html/tutorials/roofit/rf609_xychi2fit.C.html

Jan Veverka, Caltech, 10 September 2012.

USAGE: python -i rf609_xychi2fit.py
'''
import math
import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.cmsstyle as cmsstyle

import FWLite.Tools.canvases as canvases

#______________________________________________________________________________
def main():
    '''
    Main entry point of execution.
    '''
    ## C r e a t e   d a t a s e t   w i t h   X   a n d   Y   v a l u e s
    ## -------------------------------------------------------------------

    ## Make weighted XY dataset with asymmetric errors stored
    ## The StoreError() argument is essential as it makes
    ## the dataset store the error in addition to the values
    ## of the observables. If errors on one or more observables
    ## are asymmetric, one can store the asymmetric error
    ## using the StoreAsymError() argument
    x = ROOT.RooRealVar('x', 'x', -11, 11)
    y = ROOT.RooRealVar('y', 'y', -10, 200)
    dxy = ROOT.RooDataSet('dxy', 'dxy', ROOT.RooArgSet(x, y),
                          roo.StoreError(ROOT.RooArgSet(x, y)))
    
    ## Fill an example dataset with X,err(X),Y,err(Y) values
    for i in range(11):
      
        ## Set X value and error
        x.setVal(-10 + 2 * i)
        if i < 5:
            x.setError(0.5 / 1.)
        else:
            x.setError(1.0 / 1. )
          
        ## Set Y value and error
        y.setVal(x.getVal() * x.getVal() + 4 * math.fabs(ROOT.gRandom.Gaus()))
        y.setError(math.sqrt(y.getVal()))
        
        dxy.add(ROOT.RooArgSet(x, y))
    ## End of loop over dxy entries

    
    ## P e r f o r m   c h i 2   f i t   t o   X + / - d x   a n d   Y + / - d Y   v a l u e s
    ## ---------------------------------------------------------------------------------------

    ## Make fit function
    a = ROOT.RooRealVar('a', 'a', 0.0, -10, 10)
    b = ROOT.RooRealVar('b', 'b', 0, -100, 100)
    f = ROOT.RooPolyVar('f', 'f', x, ROOT.RooArgList(b, a, roo.RooConst(1)))
    
    ## Plot dataset in X-Y interpretation
    frame = x.frame(roo.Title('#chi^{2} fit of function set of '
                              '(X#pmdX,Y#pmdY) values'))
    dxy.plotOnXY(frame, roo.YVar(y))

    ## Fit chi^2 using X and Y errors
    f.chi2FitTo(dxy, roo.YVar(y))
    
    ## Overlay fitted function
    f.plotOn(frame)
    
    ## Alternative: fit chi^2 integrating f(x) over ranges defined by X errors,
    ## rather than taking point at center of bin
    f.chi2FitTo(dxy, roo.YVar(y), roo.Integrate(True))
    
    ## Overlay alternate fit result
    f.plotOn(frame, roo.LineStyle(ROOT.kDashed), roo.LineColor(ROOT.kRed))
    
    
    ## Draw the plot on a canvas
    canvases.wwidth = 600
    canvases.wheight = 600
    canvases.next('rf609_xychi2fit')
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetTopMargin(0.1)
    frame.GetYaxis().SetTitleOffset(1.0)
    frame.Draw()
    canvases.update()
    
## End of main()


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user
