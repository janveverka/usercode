'''
This example takes a RooDataSet from a RooWorkspace in TFile,
splits it in two halfs by odd and even events,
trains ParameterizedKeysPdfs to both halfs and fits
their mode and effective sigmas to the independent halfs to
get their estimates.  It creates plots showing the data with the fitted
model and resulting values.

USAGE: python -i parameterized_keys_pdf_fit_example.py

Jan Veverka, Caltech, 16 March 2012
'''

import os
import ROOT
import FWLite.Tools.roofit as roo

import FWLite.Tools.cmsstyle as cmsstyle
import FWLite.Tools.canvases as canvases
import FWLite.Tools.legend as legend
import FWLite.Tools.latex as latex

from FWLite.Tools.parameterizedkeyspdf import ParameterizedKeysPdf


## CONFIGURATION BEGIN ========================================================
path = '/raid2/veverka/yyTrees/escale'
# path = '/Users/veverka/Work/Data/zeeDataYong'
filename = ('zeeWsShapev1Smear.DoubleElectronRun2011AB16Jan2012v1AOD.'
            'etcut25.corr451.eleid1.datapu0.mcpu0.m70to110.scale2.'
            'smear0.root')
workspace = 'zeeShape'
dataset = 'rds_mpair_ebeb_tenmcat_0'
variable = 'rv_mass'
## CONFIGURATION END ==========================================================

#______________________________________________________________________________
## Parameters to be fitted
mode = ROOT.RooRealVar('mode', 'mode', 0, -1, 1)
effsigma = ROOT.RooRealVar('effsigma', 'effsigma', 1, 1e-6, 10) 

#______________________________________________________________________________
def getdata():
    '''
    Clones the dataset from the file, closes the file and returns the clone.
    '''    
    rootfile = ROOT.TFile.Open(os.path.join(path, filename))
    data = rootfile.Get(workspace).data(dataset).Clone()
    rootfile.Close()
    return data
## End of getdata().


#______________________________________________________________________________
def initialize_fit_parameters(data, x):
    '''
    Set the range and value of mode and effsigma based on the data.
    '''
    ## Define variables for the range boundaries to pass by reference
    (lowest, highest) = (ROOT.Double(), ROOT.Double())
    ## Find the range of the data with a 10% margin
    data.getRange(x, lowest, highest, 0.1)

    ## Set the range of the observable to cover the data
    x.setRange(lowest, highest)

    ## Set mode range to cover the data
    mode.setRange(lowest, highest)
    ## Set mode initial value to the mean of the data
    mode.setVal(data.mean(x))
    
    ## Get the standard deviation of the data
    sigma = data.sigma(x)
    ## Set effsigma range to cover the spread of the data
    effsigma.setRange(1e-3 * sigma, highest - lowest)
    ## Set effsigma initial value to the standard deviation of the data
    effsigma.setVal(sigma)
## End of initialize_fit_parameters(..)

    
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


#______________________________________________________________________________
def make_plot(x, data, model):
    '''
    Plot x data with the overlayed fitted model.
    '''
    global plot
    plot = x.frame()
    data.plotOn(plot)
    model.plotOn(plot)
    model.paramOn(plot)
    canvases.next(workspace)
    plot.Draw()
    canvases.update()
## End of make_plot


#______________________________________________________________________________
def main():
    '''This is the entry point to execution.'''
    print 'Welcome to parameterized_keys_pdf_fit_example!'
    global data, model, x
    data = getdata()
    ## Reduce data for debugging
    # data = data.reduce(roo.EventRange(0, 1000))
    x = data.get()[variable]
    initialize_fit_parameters(data, x)
    old_precision = set_default_integrator_precision(1e-8, 1e-8)
    model = ParameterizedKeysPdf('model', 'model', x, mode, effsigma, data,
                                 rho=1, forcerange=True)
    model.fitTo(data, roo.SumW2Error(True), roo.NumCPU(8), roo.Strategy(2))
    set_default_integrator_precision(*old_precision)
    make_plot(x, data, model)
    print '\n==  Fitted parameters =='
    mode.Print()
    effsigma.Print()
    print '\nExiting parameterized_keys_pdf_fit_example with success.'
## End of main().


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user

## End of the module
