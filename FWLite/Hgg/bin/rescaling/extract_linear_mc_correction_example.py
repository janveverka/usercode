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
from FWLite.Tools.resampler import Resampler


## CONFIGURATION BEGIN ========================================================
# path = '/raid2/veverka/yyTrees/escale'
# path = '/Users/veverka/Work/Data/zeeDataYong'
source = {
    'raw': dict(
        path = '.',
        filename = 'DoubleElectron_barrel_highR9.root',
        workspace = None,
        dataset = 'MVAPresel',
        ),
    'target' : dict(
        path = '.',
        filename = 'DYToEE_M-20_CT10_barrel_highR9.root',
        workspace = None,
        dataset = 'MVAPresel',
        ),
    }
variable = 'sigE_o_E_lead'
output_filename = 'result.root'
plot_range = (0.004, 0.014)
fit_range = (0.005, 0.012)
kde_training_max_events = 50000

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
    data = {}
    for name, src in source.items():
        rootfile = ROOT.TFile.Open(os.path.join(src['path'], src['filename']))
        if src['workspace']:
            workspace = rootfile.Get(src['workspace'])
            data[name] = workspace.data(src['dataset']).Clone()
        else:
            data[name] = rootfile.Get(src['dataset']).Clone()
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
    # global plot
    if plot_range:
        plot = x.frame(roo.Range(*plot_range), roo.Title(data.GetName()))
    else:
        plot = x.frame(roo.Title(data.GetName()))
    data.plotOn(plot)
    model.plotOn(plot)
    model.paramOn(plot)
    canvases.next(data.GetName()).SetGrid()
    plot.Draw()
    canvases.update()
## End of make_plot


#______________________________________________________________________________
def make_comparison_plot(data_raw, data_target, x_corr):
    '''
    Plot x data with the overlayed fitted model.
    '''
    data_corr = get_corrected_data(data_raw, x_corr)
    # global plot
    if plot_range:
        plot = x.frame(roo.Range(*plot_range))
    else:
        plot = x.frame()
    plot.SetTitle('Raw (red) vs Corrected (blue) vs Target (black) Data')
    if b_corr.getVal() > 1.:
        data_raw.plotOn(plot, roo.LineColor(ROOT.kRed), 
                        roo.MarkerColor(ROOT.kRed))
        data_corr.plotOn(plot, roo.LineColor(ROOT.kBlue), 
                         roo.MarkerColor(ROOT.kBlue))
        data_target.plotOn(
          plot, 
          roo.Rescale(data_raw.sumEntries() / data_target.sumEntries())
          )
    else:
        data_target.plotOn(plot)
        data_raw.plotOn(
            plot, roo.LineColor(ROOT.kRed), roo.MarkerColor(ROOT.kRed),
            roo.Rescale(data_target.sumEntries() / data_raw.sumEntries())
            )
        data_corr.plotOn(
            plot, roo.LineColor(ROOT.kBlue), roo.MarkerColor(ROOT.kBlue),
            roo.Rescale(data_target.sumEntries() / data_corr.sumEntries())
            )
        
    canvases.next('Raw_vs_Corrected_vs_Target_Data').SetGrid()
    plot.Draw()
    canvases.update()
## End of make_comparison_plot


#______________________________________________________________________________
def get_corrected_data(data_raw, correction):
    debugmsg(1)
    data_corr = data_raw.Clone()
    data_corr.Print()
    x_corr_var = data_corr.addColumn(correction)
    debugmsg(2)
    data_corr = data_corr.Reduce(ROOT.RooArgSet(x_corr_var))
    data_corr.Print()
    x_corr_var = data_corr.get()[correction.GetName()]
    x_corr_var.Print()
    ROOT.RooArgList(x_corr_var).Print()
    rename_func = ROOT.RooFormulaVar(
        x.GetName(), x.GetName(), correction.GetName(),
        ROOT.RooArgList(x_corr_var)
        )
    debugmsg(3)
    x_corr_var = data_corr.addColumn(rename_func)
    data_corr = data_corr.Reduce(ROOT.RooArgSet(x_corr_var))
    return data_corr
## End of get_corrected_data


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
def debugmsg(msg):
    print '+++ DEBUG {m}'.format(m=msg)
## End of debugmsg


#______________________________________________________________________________
def get_correction(x_raw, params_raw, params_target):
    '''
    Calculate linear correction:
    x_corrected = m_t + s_t/s_r * (x_raw - m_r)
                = a + b * x_raw
    a = m_t - s_t / s_r * m_r
    b = s_t / s_r
    '''
    global a_corr
    a_corr = x_raw.Clone('a_corr')
    global b_corr
    b_corr = ROOT.RooRealVar('b_corr', 'b_corr', 1., 0.001, 1000.)
    
    params_raw_map = {}
    for i in range(params_raw.getSize()):
        param = params_raw[i]
        params_raw_map[param.GetName()] = param

    params_target_map = {}
    for i in range(params_target.getSize()):
        param = params_target[i]
        params_target_map[param.GetName()] = param
    
    mr = params_raw_map['mode'].getVal()
    sr = params_raw_map['effsigma'].getVal()
    mt = params_target_map['mode'].getVal()
    st = params_target_map['effsigma'].getVal()
    
    a_corr.setVal(mt - mr * st / sr)
    b_corr.setVal(st / sr)

    ## Error propagation
    emr = params_raw_map['mode'].getError()
    esr = params_raw_map['effsigma'].getError()
    emt = params_target_map['mode'].getError()
    est = params_target_map['effsigma'].getError()
    
    oplus = lambda x, y: ROOT.TMath.Sqrt(x*x + y*y)
    oplus3 = lambda x, y, z: ROOT.TMath.Sqrt(x*x + y*y + z*z)
    
    ## Neglect correlation of sr and mr
    a2 = mr * st / sr
    ea2 = a2 * oplus3(emr/mr, est/st, esr/sr)
    a_corr.setError(oplus(emt, ea2))
    
    b_corr.setError(oplus(est / st, esr / sr) * st/sr)
    
    x_corr = ROOT.RooFormulaVar(
                'x_corr', 'Linear correction for %s' % x_raw.GetName(),
                '{a} + {b} * {x_raw}'.format(a = a_corr.GetName(),
                                             b = b_corr.GetName(),
                                             x_raw = x_raw.GetName()),
                ROOT.RooArgList(a_corr, b_corr, x_raw)
                )
    return x_corr
## End of get_correction


#______________________________________________________________________________
def main():
    '''This is the entry point to execution.'''
    global data, model, x, fitresult
    data = getdata()
    x = data['raw'].get()[variable]
    if fit_range:
        x.setRange('fit', *fit_range)
    if plot_range:
        x.setRange('plot', *plot_range)
    initialize_fit_parameters(data['raw'], x)
    old_precision = set_default_integrator_precision(1e-8, 1e-8)
    ## Reduce data for model building
    data_kde_training = data['raw']
    if data['raw'].numEntries() > kde_training_max_events:
        resampler = Resampler(data['raw'])
        data['raw_reduced'] = resampler.bootstrap(
            name = data['raw'].GetName() + '_boot',
            title = data['raw'].GetTitle() + ' Bootstrap Replica',
            size = kde_training_max_events,
            )
        data_kde_training = data['raw_reduced']    
    
    model = ParameterizedKeysPdf('model', 'model', x, mode, effsigma, 
                                 data_kde_training, rho=0.8, forcerange=True)
                
    
    fitresult = {}
    for name, dataset in data.items():
        dataset.SetName(name + 'Data')
        ## Reduce data for debugging
        # dataset = dataset.reduce(roo.EventRange(0, 10000))
        fitresult[name] = model.fitTo(dataset, roo.SumW2Error(True), 
                                      roo.NumCPU(8), roo.Strategy(2),
                                      roo.Save())
        make_plot(x, dataset, model)
                            
        print '\n==  Fitted parameters =='
        mode.Print()
        effsigma.Print()
        save_result(fitresult[name])
    set_default_integrator_precision(*old_precision)
    x_corr = get_correction(x, fitresult['raw'].floatParsFinal(),
                            fitresult['target'].floatParsFinal())
    make_comparison_plot(data['raw'], data['target'], x_corr)
## End of main().


#______________________________________________________________________________
if __name__ == '__main__':
    print 'Welcome to extract_linear_mc_correction_example!'
    main()
    import user
    print '== Initial Parameters =='
    for name in 'raw_reduced raw target'.split():
        print '===', name, '==='
        fitresult[name].floatParsInit().Print('v')

    print '\n== Final Parameters =='
    for name in 'raw_reduced raw target'.split():
        print '===', name, '==='
        fitresult[name].floatParsFinal().Print('v')

    print '\n== Correction =='
    print 'x_corr should match x_target better than x_raw'
    print
    print 'x_corr = a_corr + b_corr * x_raw'
    a_corr.Print()
    b_corr.Print()
    print 'x_corr = %.*f + %.*f * x_raw' % (6, a_corr.getVal(), 
                                            4, b_corr.getVal())

    print '\nExiting extract_linear_mc_correction_example with success.'
    
    

## End of the module
