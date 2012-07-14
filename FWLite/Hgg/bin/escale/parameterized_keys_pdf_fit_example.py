'''
This example takes a RooDataSet from a RooWorkspace in a TFile,
trains a ParameterizedKeysPdf on it and then fits its mode
and effective sigma to the same data.  This is a robust way
to estimate the mode and effective sigma and their uncertainties
for a binned sample.

It creates plots showing the data with the fitted
model and resulting values and prints the result of the fit.

TODO:
- It should split the data in two halfs by odd and even events,
trains ParameterizedKeysPdfs to both halfs and fits
their mode and effective sigmas to the independent halfs to
get their estimates.
- Factor it out in a class
- Wrap it in a command line tool
- Include interface with simple text config files
- Deal with very large datasets by merging neighboring
evnets
- Reduce the amount of the output
- Port to C++ only
- Fit in a limited range only

Origianlly developed for the PHOSPHOR Fit
https://twiki.cern.ch/twiki/bin/view/CMS/VGamma2011PhosphorFit

USAGE: python -i parameterized_keys_pdf_fit_example.py

Jan Veverka, Caltech, 16 May 2012
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
output_filename = 'result.root'
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
def save_result(fitresult):
    '''
    Stores the fit result in the root file under the output_filename name.
    '''
    w = ROOT.RooWorkspace('fitresults')
    w.Import(fitresult)
    w.writeToFile(output_filename)
## End of save_result(..)


#______________________________________________________________________________
def main():
    '''This is the entry point to execution.'''
    print 'Welcome to parameterized_keys_pdf_fit_example!'
    global data, model, x, fitresult
    data = getdata()
    data.SetName('zeeDataYong')
    ## Reduce data for debugging
    data = data.reduce(roo.EventRange(0, 5000))
    x = data.get()[variable]
    initialize_fit_parameters(data, x)
    old_precision = set_default_integrator_precision(1e-8, 1e-8)
    model = ParameterizedKeysPdf('model', 'model', x, mode, effsigma, data,
                                 rho=1, forcerange=True)
                                 
    fitresult = model.fitTo(data, roo.SumW2Error(True), roo.NumCPU(8), 
                            roo.Strategy(2), roo.Save())
    set_default_integrator_precision(*old_precision)
    make_plot(x, data, model)
    print '\n==  Fitted parameters =='
    mode.Print()
    effsigma.Print()
    save_result(fitresult)
    print '\nExiting parameterized_keys_pdf_fit_example with success.'
## End of main().


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user
    print '== Initial'
    fitresult.floatParsInit().Print('v')
    print '== Final'
    fitresult.floatParsFinal().Print('v')
    

## End of the module
