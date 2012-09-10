'''
This is a PyROOT version of 
rf609_xychi2fit.C: 'LIKELIHOOD AND MINIMIZATION' RooFit tutorial macro #609
combined with
rf610_visualerror.C: 'LIKELIHOOD AND MINIMIZATION' RooFit tutorial macro #610
See originals at:
http:##root.cern.ch/root/html/tutorials/roofit/rf609_xychi2fit.C.html
http://root.cern.ch/root/html/tutorials/roofit/rf610_visualerror.C.html

Jan Veverka, Caltech, 10 September 2012.

USAGE: python -i xychi2fitter.py
'''
import math
import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.cmsstyle as cmsstyle

import FWLite.Tools.canvases as canvases

class XYChi2Fitter():
  
    #_________________________________________________________________________
    def __init__(self):
        self.create_toy_dataset()
        self.define_fit_function_parabola()
    ## End of __init__(self).
    
    
    #_________________________________________________________________________
    def create_toy_dataset(self):
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
        self.x, self.y, self.dxy = x, y, dxy
        
    ## End of create_dataset(self)
    
    
    #_________________________________________________________________________
    def define_fit_function_parabola(self):
        ## Make fit function
        self.a = ROOT.RooRealVar('a', 'a', 0.0, -10, 10)
        self.b = ROOT.RooRealVar('b', 'b', 0, -100, 100)
        self.f = ROOT.RooPolyVar('f', 'f', self.x, 
                                 ROOT.RooArgList(self.b, 
                                                 self.a, 
                                                 roo.RooConst(1)))
    ## End of define_fit_function(self)
    

    #_________________________________________________________________________
    def make_plot(self):
        frame = self.x.frame(roo.Title('#chi^{2} fit of function set of '
                                       '(X#pmdX,Y#pmdY) values'))

        ## Visualize 2- and 1-sigma errors
        #print "## Visualize 2- and 1-sigma errors"
        self.f.plotOn(frame, roo.VisualizeError(self.fresult, 2), 
                      roo.FillColor(ROOT.kGreen))
        self.f.plotOn(frame, roo.VisualizeError(self.fresult, 1), 
                      roo.FillColor(ROOT.kYellow))
        
        ## Plot dataset in X-Y interpretation
        #print "## Plot dataset in X-Y interpretation"
        self.dxy.plotOnXY(frame, roo.YVar(self.y))

        ## Overlay fitted function
        #print "## Overlay fitted function"
        self.f.plotOn(frame)
        return frame
      
    ## End of make_plot(self)
    
    
    #_________________________________________________________________________
    def draw_plot(self, frame):
        ## Draw the plot on a canvas
        #print "## Draw the plot on a canvas"
        canvases.wwidth = 600
        canvases.wheight = 600
        canvases.next('rf609_xychi2fit')
        ROOT.gPad.SetLeftMargin(0.15)
        ROOT.gPad.SetTopMargin(0.1)
        frame.GetYaxis().SetTitleOffset(1.0)
        frame.Draw()
        canvases.update()
    ## End of draw_plot()

    
    #_________________________________________________________________________
    def run(self):
        ## P e r f o r m   c h i 2   f i t   t o   X + / - d x   a n d   Y + / - d Y   v a l u e s
        ## ---------------------------------------------------------------------------------------

        ## Fit chi^2 using X and Y errors
        #print "## Fit chi^2 using X and Y errors"
        self.fresult = self.f.chi2FitTo(self.dxy, roo.YVar(self.y), roo.Save())
        
        frame = self.make_plot()                
        self.draw_plot(frame)
    ## End of run(self)
      
## End of class XYChi2Fitter      

#______________________________________________________________________________
def main():
    '''
    Main entry point of execution.
    '''
    global fitter
    fitter = XYChi2Fitter()
    fitter.run()    
## End of main()


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user
