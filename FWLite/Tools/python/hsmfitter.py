'''
Estimates the mode of an unbinned dataset using the half-sample mode.

Jan Veverka, Caltech, 23 October 2012.
'''

import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.cmsstyle as cmsstyle
import FWLite.Tools.canvases as canvases

from FWLite.Tools.modalinterval import ModalInterval
from FWLite.Tools.parameterizedkeyspdf import ParameterizedKeysPdf
from FWLite.Tools.resampler import Resampler

##------------------------------------------------------------------------------
class HSMFitter:
    #__________________________________________________________________________
    def __init__(self, data, nboot=1, printlevel=-1):
        if data.get().getSize() != 1:
            raise RuntimeError, 'Data must contain just one variable!'
        
        self.w = ROOT.RooWorkspace('HSMFitter',
                                   'HSMFitter Workspace')
        self.w.Import(data)
        self.data = self.w.data(data.GetName())
        self.data.SetName('data')        

        self.nboot = nboot        
        self.printlevel = printlevel

        self.mode = ROOT.RooRealVar('mode', 'mode', 0)
        self.mode.setVal(0)
        self.mode.setError(0)
        self.w.Import(self.mode)
        self.mode = self.w.var('mode')

        self.effsigma = ROOT.RooRealVar('effsigma', 'effsigma', 0)
        self.effsigma.setVal(0)
        self.effsigma.setError(0)
        self.w.Import(self.effsigma)
        self.effsigma = self.w.var('effsigma')

        self.bootset = ROOT.RooArgSet(self.mode, self.effsigma)
        self.bootdata = ROOT.RooDataSet('bootdata', 'bootdata', self.bootset)       

       # self.dofit()
    ## end of __init__
    
    #__________________________________________________________________________
    def dofit(self):
        mi = ModalInterval(self.data)
        mi.setSigmaLevel(1)
        self.mode.setVal(mi.halfSampleMode())
        self.effsigma.setVal(0.5 * mi.length())
        self.bootdata.add(self.bootset)
        resampler = Resampler(self.data)
        for iboot in range(self.nboot):
            mi = ModalInterval(resampler.bootstrap())
            mi.setSigmaLevel(1)
            self.mode.setVal(mi.halfSampleMode())
            self.effsigma.setVal(0.5 * mi.length())
            self.bootdata.add(self.bootset)
        self.mode.setVal(self.bootdata.mean(self.mode))
        self.effsigma.setVal(self.bootdata.mean(self.effsigma))
        self.mode.setError(self.bootdata.rmsVar(self.mode).getVal())
        self.effsigma.setError(self.bootdata.rmsVar(self.effsigma).getVal())
    ## end of dofit

    #__________________________________________________________________________
    def makeplot(self):
        self.canvas = canvases.next()
        self.plot = self.x.frame()
        self.data.plotOn(self.plot)
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
    ntoys=20
    ndata=1000
    randseed=15
    outputname = 'response_fits_ntoys1k_ndata1k_rho2.7_seed15.root'
    # outputname = 'response_fits_test.root'
    ROOT.RooRandom.randomGenerator().SetSeed(randseed)
    sw = ROOT.TStopwatch()
    global fitters, workspaces
    fitters, workspaces = [], []
    global histos
    histos = {
        'hsm_mode_val': ROOT.TH1F('hsm_mode_val', 'hsm_mode_val', 100, -1, 1),
        'hsm_mode_err': ROOT.TH1F('hsm_mode_err', 'hsm_mode_err', 100, 0.01, 0.5),
        'hsm_sigma_val': ROOT.TH1F('hsm_sigma_val', 'hsm_sigma_val', 100, 0.8, 1.2),
        'hsm_sigma_err': ROOT.TH1F('hsm_sigma_err', 'hsm_sigma_err', 100, 0.01, 0.05),
        'gauss_mode_val': ROOT.TH1F('gauss_mode_val', 'gauss_mode_val', 100, -1, 1),
        'gauss_mode_err': ROOT.TH1F('gauss_mode_err', 'gauss_mode_err', 100, 0.01, 0.05),
        'gauss_sigma_val': ROOT.TH1F('gauss_sigma_val', 'gauss_sigma_val', 100, 0.8, 1.2),
        'gauss_sigma_err': ROOT.TH1F('gauss_sigma_err', 'gauss_sigma_err', 100, 0.01, 0.05),
        }
    
    #set_default_integrator_precision(1e-8, 1e-8)
    
    sw.Start()
    for i in range(ntoys):
        w = ROOT.RooWorkspace('test')
        model = w.factory('Gaussian::model(x[-5,5], m[0,-5,5], s[1,0.01,10])')
        x = w.var('x')
        data = model.generate(ROOT.RooArgSet(x), ndata)
        model.fitTo(data)
        workspaces.append(w)        
        
        fitter = HSMFitter(data, nboot=500)    
        fitter.dofit()
        # fitter.makeplot()
        fitters.append(fitter)
        histos['hsm_mode_val'].Fill(fitter.mode.getVal())
        histos['hsm_mode_err'].Fill(fitter.mode.getError())
        histos['hsm_sigma_val'].Fill(fitter.effsigma.getVal())
        histos['hsm_sigma_err'].Fill(fitter.effsigma.getError())
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

    global output
    output = ROOT.TFile(outputname, 'recreate')
    for h in histos.values():
        h.SetDirectory(output)
    output.Write()
## end of main


##------------------------------------------------------------------------------
## Footer stuff
if __name__ == "__main__":
    main()
    import user

