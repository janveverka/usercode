'''
Extracts a linear correctin for R9 in MC through a parametrized KEYS
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
import FWLite.Tools.dataset as dataset

from Zmmg.FWLite.pmvtrees import get_trees
from FWLite.Tools.parameterizedkeyspdf import ParameterizedKeysPdf


## CONFIGURATION BEGIN ========================================================
name = 'r9_EB_pt25up_v15reco'
tree_version = 'v15reco'
variable = ROOT.RooRealVar('R9', 'phoR9', 0.3, 1.1)
weight = {
    'z'   : ROOT.RooRealVar('weight', 'pileup.weight', 0, 100),
    'data': ROOT.RooRealVar('weight', '1', 0, 100),
    }
cuts = [
    'phoIsEB',
    'phoPt > 25',
    'mmMass + mmgMass < 180',
    ]
fit_range = (0.9, 1.0)
plot_range = (0.9, 1.0)
output_filename = 'r9fit.root'
## CONFIGURATION END ==========================================================

variable.setRange('fit', *fit_range)
variable.setRange('plot', *plot_range)

#______________________________________________________________________________
## Parameters to be fitted
mode = ROOT.RooRealVar('mode', 'mode', 0, -1, 1)
effsigma = ROOT.RooRealVar('effsigma', 'effsigma', 1, 1e-6, 10) 

#______________________________________________________________________________
def getdata():
    '''
    Clones the dataset from the file, closes the file and returns the clone.
    '''    
    trees = get_trees(tree_version)
    data = {}
    for source, tree in trees.items():
        data[source] = dataset.get(tree=tree, variable=variable,
                                   weight=weight[source], cuts = cuts)
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
def make_plot(x, data, model, name=name):
    '''
    Plot x data with the overlayed fitted model.
    '''
    global plot
    plot = x.frame(roo.Range('plot'))
    data.plotOn(plot)
    model.plotOn(plot)
    model.paramOn(plot)
    canvases.next(name)
    plot.Draw()
    canvases.update()
## End of make_plot


#______________________________________________________________________________
def save_results(fitresult, name):
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
    s, r = {}, {}
    for name, res in fitresults.items():
        print name
        for pars in [res.floatParsFinal(), res.constPars()]:
            for i in range(pars.getSize()):
                pars[i].Print()
                if pars[i].GetName() == 'mode':
                    s[name] = pars[i].getVal()
                elif pars[i].GetName() == 'effsigma':
                    r[name] = pars[i].getVal()
            
    ## (x-s)/r = (x0-s0)/r0
    ## x = s + (x0-s0)*r/r0
    ##   = s - s0 * r/r0 + x0 * r/r0
    scaling = r['Data'] / r['MC']
    print "s =", s
    print "r =", r
    print "== Correction for MC =="
    print "R9corr = %g + %g * R9" % (s['Data'] - s['MC'] * scaling, scaling)
    
## End of print_report(..)


#______________________________________________________________________________
def main():
    '''This is the entry point to execution.'''
    print 'Welcome to parameterized_keys_pdf_fit_example!'
    global data, model, x, fitresults
    data = getdata()
    ## Reduce data for debugging
    for source, dataset in data.items():
        # data[source] = dataset.reduce(roo.EventRange(0, 1000))
        pass
    x = data['data'].get()[variable.GetName()]
    old_precision = set_default_integrator_precision(1e-8, 1e-8)
    model = ParameterizedKeysPdf('model', 'model', x, mode, effsigma, data['z'],
                                 rho=0.6, forcerange=True)
    #initialize_fit_parameters(data['data'], x)
    for var, varname in zip([mode, effsigma], ['mode', 'width']):
        var.setVal(getattr(model, 'shape' + varname + 'var').getVal())
    make_plot(x, data['z'], model.shape, 'MC_Shape')
    fitresults = {}
    for source in 'z data'.split():
        dataset = data[source]
        name = {'z': 'MC', 'data': 'Data'}[source]
        dataset.SetName(name)
        if source == 'data':
            # mode.setConstant(True)
            pass
        fitresult = model.fitTo(dataset, roo.SumW2Error(True),
                                roo.NumCPU(8), roo.Strategy(2), 
                                roo.Save(), roo.Range('fit'))
        fitresults[name] = fitresult
        make_plot(x, dataset, model, name)
        save_result(fitresult, name)

    print_report(fitresults)
    set_default_integrator_precision(*old_precision)
    print '\nExiting r9scaler with success.'
## End of main().


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user

## End of the module
