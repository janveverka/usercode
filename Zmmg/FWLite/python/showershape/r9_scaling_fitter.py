'''
Extracts a scaling correctin for R9 in MC through a parametrized KEYS
PDF fit.

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

USAGE: python -i r9_scaling_fitter.py

Jan Veverka, Caltech, 20 July 2012
'''

import math
import os
import ROOT
import FWLite.Tools.roofit as roo

import FWLite.Tools.cmsstyle as cmsstyle
import FWLite.Tools.canvases as canvases
import FWLite.Tools.legend as legend
import FWLite.Tools.latex as latex
import FWLite.Tools.dataset as dataset

from Zmmg.FWLite.pmvtrees import get_trees
from FWLite.Tools.parameterizedkeyspdf import ParameterizedKeysPdf


## CONFIGURATION BEGIN ========================================================
name = 'r9_EB_pt25up_v15reco_muOutsidePhoton'
title = 'Barrel'
tree_version = 'v15reco'
variable = ROOT.RooRealVar('R9', 'Photon R_{9}', 0.3, 1.1)
varexpression = 'phoR9'
weight = {
    'z'   : ROOT.RooRealVar('weight', 'pileup.weight', 0, 100),
    'data': ROOT.RooRealVar('weight', '1', 0, 100),
    }
cuts = [
    '!phoIsEB',
    'phoPt > 10',
    'mmMass + mmgMass < 180',
    ## Exclude photons with muon hitting the 3x3 central crystals
    'abs(muNearIEtaX - phoIEtaX) >= 2 & abs(muNearIPhiY - phoIPhiY) >= 2',
    ## Include only photons with muon hitting the 3x3 central crystals
    # 'abs(muNearIEtaX - phoIEtaX) <= 1 & abs(muNearIPhiY - phoIPhiY) <= 1',
    ## Exclude photons with muon hitting the clustering region
    #'(abs(muNearIEtaX - phoIEtaX) > 6 | abs(muNearIPhiY - phoIPhiY) > 6)',
    ]
fit_range = (0.3, 1.1)
plot_range = (0.85, 1.0)
output_filename = 'r9fit.root'
## CONFIGURATION END ==========================================================

variable.setRange('fit', *fit_range)
variable.setRange('plot', *plot_range)

#______________________________________________________________________________
## Parameters to be fitted
mode = ROOT.RooRealVar('mode', 'mode', 0, -1, 1)
effsigma = ROOT.RooRealVar('effsigma', 's', 1, 1e-6, 10) 

#______________________________________________________________________________
def getdata():
    '''
    Clones the dataset from the file, closes the file and returns the clone.
    '''    
    trees = get_trees(tree_version)
    vartitle = variable.GetTitle()
    variable.SetTitle(varexpression)
    data = {}
    for source, tree in trees.items():
        data[source] = dataset.get(tree=tree, variable=variable,
                                   weight=weight[source], cuts = cuts)
    variable.SetTitle(vartitle)
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
def make_plot(x, data, model, name=name, title=name):
    '''
    Plot x data with the overlayed fitted model.
    '''
    global plot
    plot = x.frame(roo.Range('plot'))
    plot.SetTitle(title)
    data.plotOn(plot)
    model.plotOn(plot, roo.Range('plot'), roo.NormRange('plot'))
    #model.paramOn(plot)
    canvases.next(name)
    plot.Draw()
    canvases.update()
## End of make_plot


#______________________________________________________________________________
def save_result(fitresult, name):
    '''
    Stores the fit result in the root file under the output_filename name.
    '''
    global w
    if 'w' not in vars():
          w = ROOT.RooWorkspace('fitresults')
    w.Import(fitresult, name)
    w.writeToFile(output_filename)
## End of save_result(..)


#______________________________________________________________________________
def print_report(fitresults):
    print '\n==  Fitted parameters =='
    ## As scale and resolution
    r, er = {}, {}
    for name, res in fitresults.items():
        print name
        for pars in [res.floatParsFinal(), res.constPars()]:
            for i in range(pars.getSize()):
                pars[i].Print()
                if pars[i].GetName() == 'effsigma':
                    r[name] = pars[i].getVal()
                    er[name] = pars[i].getError()
            
    ## (x-s)/r = (x0-s0)/r0
    ## x = s + (x0-s0)*r/r0
    ##   = s - s0 * r/r0 + x0 * r/r0
    oplus = lambda x, y: math.sqrt(x * x + y * y)
    scaling = r['Data'] / r['MC']
    error = scaling * oplus(er['Data']/r['Data'], er['MC']/r['MC'])
    
    print "== Correction for MC =="
    print "R9corr = (%.5f +/- %.5f) * R9" % (scaling, error)
    
## End of print_report(..)


#______________________________________________________________________________
def fix_model_parameters(model):
    '''
    Sets and fixes the model parameters such that only the scaling is fitted.
    That is R9_corrected = s * R9
    '''
    mode.setConstant(True)
    

    mode.setVal(0)
    effsigma.setVal(1)
    
    model.shapemodevar.setVal(0)
    model.shapewidthvar.setVal(1)
## End of fix_model_parameters(model)

#______________________________________________________________________________
def main():
    '''This is the entry point to execution.'''
    print 'Welcome to r9_scaling_fitter!'
    global data, model, x, fitresults
    data = getdata()
    ## Reduce data for debugging
    for source, dataset in data.items():
        # data[source] = dataset.reduce(roo.EventRange(0, 1000))
        pass
    x = variable
    old_precision = set_default_integrator_precision(1e-8, 1e-8)
    model = ParameterizedKeysPdf('model', 'model', x, mode, effsigma, data['z'],
                                 rho=0.7, forcerange=True)
    fix_model_parameters(model)
    # make_plot(x, data['z'], model.shape, name + 'MC_Shape', '')
    fitresults = {}
    for source in 'z data'.split():
        dataset = data[source]
        label = {'z': 'MC', 'data': 'Data'}[source]
        dataset.SetName(label)
        if source == 'data':
            # mode.setConstant(True)
            pass
        fitresult = model.fitTo(dataset, roo.SumW2Error(True),
                                roo.NumCPU(8), roo.Strategy(2), 
                                roo.Save(), roo.Range('fit'))
        fitresults[label] = fitresult
        make_plot(x, dataset, model, '_'.join([name,label]), '')
        # save_result(fitresult, label)

    print_report(fitresults)
    set_default_integrator_precision(*old_precision)
    print '\nExiting r9_scaling_fitter with success.'
## End of main().


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user

## End of the module
