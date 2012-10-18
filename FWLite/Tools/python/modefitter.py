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
        self.model.fitTo(self.data, roo.PrintLevel(1), roo.Verbose(False))
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
    ntoys=1000
    ndata=1000
    rho=2.7
    randseed=15
    outputname = 'response_fits_ntoys1k_ndata1k_rho2.7_seed15.root'
    # outputname = 'response_fits_test.root'
    ROOT.RooRandom.randomGenerator().SetSeed(randseed)
    sw = ROOT.TStopwatch()
    global fitters, workspaces
    fitters, workspaces = [], []
    global histos
    histos = {
        'keys_mode_val': ROOT.TH1F('keys_mode_val', 'keys_mode_val', 100, -1, 1),
        'keys_mode_err': ROOT.TH1F('keys_mode_err', 'keys_mode_err', 100, 0.01, 0.05),
        'keys_sigma_val': ROOT.TH1F('keys_sigma_val', 'keys_sigma_val', 100, 0.8, 1.2),
        'keys_sigma_err': ROOT.TH1F('keys_sigma_err', 'keys_sigma_err', 100, 0.01, 0.05),
        'keys_sigma_shape': ROOT.TH1F('keys_sigma_shape', 'keys_sigma_shape', 150, 0.5, 2.0),
        'gauss_mode_val': ROOT.TH1F('gauss_mode_val', 'gauss_mode_val', 100, -1, 1),
        'gauss_mode_err': ROOT.TH1F('gauss_mode_err', 'gauss_mode_err', 100, 0.01, 0.05),
        'gauss_sigma_val': ROOT.TH1F('gauss_sigma_val', 'gauss_sigma_val', 100, 0.8, 1.2),
        'gauss_sigma_err': ROOT.TH1F('gauss_sigma_err', 'gauss_sigma_err', 100, 0.01, 0.05),
        }
    
    set_default_integrator_precision(1e-8, 1e-8)
    
    sw.Start()
    for i in range(ntoys):
        w = ROOT.RooWorkspace('test')
        model = w.factory('Gaussian::model(x[-5,5], m[0,-5,5], s[1,0.01,10])')
        x = w.var('x')
        data = model.generate(ROOT.RooArgSet(x), ndata)
        model.fitTo(data)
        workspaces.append(w)        
        
        fitter = KeysResponseFitter(data, rho=rho)    
        fitter.dofit()
        # fitter.makeplot()
        fitters.append(fitter)
        histos['keys_mode_val'].Fill(fitter.mode.getVal())
        histos['keys_mode_err'].Fill(fitter.mode.getError())
        histos['keys_sigma_val'].Fill(fitter.effsigma.getVal())
        histos['keys_sigma_err'].Fill(fitter.effsigma.getError())
        histos['keys_sigma_shape'].Fill(fitter.model.shapewidth)
        histos['gauss_mode_val'].Fill(w.var('m').getVal())
        histos['gauss_mode_err'].Fill(w.var('m').getError())
        histos['gauss_sigma_val'].Fill(w.var('s').getVal())
        histos['gauss_sigma_err'].Fill(w.var('s').getError())
        

    sw.Stop()
    # print 'Gaussian fits:'
    # for w in workspaces:
    #     print '% 5.3f +/- %5.3f   %5.3f +/- %5.3f' % (
    #       w.var('m').getVal(), w.var('m').getError(), w.var('s').getVal(),
    #       w.var('s').getError()
    #       )
    
    # print 'KEYS fits:'
    # for f in fitters:
    #     print '% 5.3f +/- %5.3f   %5.3f +/- %5.3f' % (
    #       f.mode.getVal(), f.mode.getError(), f.effsigma.getVal(),
    #       f.effsigma.getError()
    #       )
    names = histos.keys()
    names.sort()
    for n in names:
        canvases.next(n)
        histos[n].Draw()
    canvases.update()
    print 'Real time: %.1f s' % sw.RealTime()

    output = ROOT.TFile(outputname, 'recreate')
    for h in histos.values():
        h.SetDirectory(output)
    output.Write()
    output.Close()
## end of main


##------------------------------------------------------------------------------
## Footer stuff
if __name__ == "__main__":
    main()
    import user

