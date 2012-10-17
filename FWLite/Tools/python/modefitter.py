'''
Estimates the mode of an unbinned dataset.

Jan Veverka, Caltech, 17 October 2012.
'''

import ROOT
import JPsi.MuMu.common.roofit as roo
from FWLite.Tools.parameterizedkeyspdf import ParameterizedKeysPdf

import FWLite.Tools.cmsstyle as cmsstyle
import FWLite.Tools.canvases as canvases

##------------------------------------------------------------------------------
class KeysResponseFitter:
    #__________________________________________________________________________
    def __init__(self, data, rho=1.5, printlevel=-1):
        if data.get().getSize() != 1:
            raise RuntimeError, 'Data must contain just one variable!'
        
        self.w = ROOT.RooWorkspace('KeysResponseFitter',
                                   'KeysResponseFitter Workspace')
        self.w.Import(data)
        self.data = self.w.data(data.GetName())
        self.data.SetName('data')        

        self.x = self.w.var(data.get().first().GetName())
        self.x.SetName('x')
        
        self.rho = rho        
        self.printlevel = printlevel

        ## Define mode and effsigma.
        self.mode = self.w.factory('mode[0, -50, 50]')
        self.effsigma = self.w.factory('effsigma[1, 0.01, 50]')
        for x in 'mode effsigma'.split():
            getattr(self, x).setUnit(self.x.getUnit())
        
        self.model = ParameterizedKeysPdf('model', 'model', self.x, self.mode,
                                          self.effsigma, self.data, rho=rho,
                                          forcerange=True)
        
        # self.dofit()
    ## end of __init__
    
    #__________________________________________________________________________
    def dofit(self):
        self.model.fitTo(self.data)
    ## end of doFit

    #__________________________________________________________________________
    def makeplot(self):
        self.canvas = canvases.next()
        self.plot = self.x.frame()
        self.data.plotOn(self.plot)
        self.model.plotOn(self.plot)
        self.model.paramOn(self.plot)
        self.plot.Draw()
        self.canvas.Update()
    
## end of KeysResponseFitter


#______________________________________________________________________________
def set_default_integrator_precision(eps_abs, eps_rel):
    '''
    Sets the default integration relative and absolute precition to eps
    and returns the old precision values
    '''
    old_precision = (ROOT.RooAbsReal.defaultIntegratorConfig().epsAbs(),
                     ROOT.RooAbsReal.defaultIntegratorConfig().epsRel())
    ROOT.RooAbsReal.defaultIntegratorConfig().setEpsAbs(eps_abs)
    ROOT.RooAbsReal.defaultIntegratorConfig().setEpsRel(eps_rel)
    return old_precision
## End of set_default_integrator_precision.


##------------------------------------------------------------------------------
def main():
    global fitters, workspaces
    fitters, workspaces = [], []
    
    set_default_integrator_precision(1e-8, 1e-8)
    
    for i in range(10):
        w = ROOT.RooWorkspace('test')
        model = w.factory('Gaussian::model(x[-5,5], m[0,-5,5], s[1,0.01,10])')
        x = w.var('x')
        data = model.generate(ROOT.RooArgSet(x), 1000)
        model.fitTo(data)
        workspaces.append(w)        
        
        fitter = KeysResponseFitter(data)    
        fitter.dofit()
        fitter.makeplot()
        fitters.append(fitter)
    
    print 'Gaussian fits:'
    for w in workspaces:
        print '% 5.3f +/- %5.3f   %5.3f +/- %5.3f' % (
          w.var('m').getVal(), w.var('m').getError(), w.var('s').getVal(),
          w.var('s').getError()
          )
    
    print 'KEYS fits:'
    for f in fitters:
        print '% 5.3f +/- %5.3f   %5.3f +/- %5.3f' % (
          f.mode.getVal(), f.mode.getError(), f.effsigma.getVal(),
          f.effsigma.getError()
          )
    canvases.update()
## end of main


##------------------------------------------------------------------------------
## Footer stuff
if __name__ == "__main__":
    main()
    import user

