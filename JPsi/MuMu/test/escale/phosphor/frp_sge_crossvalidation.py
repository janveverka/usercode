'''
Plot photon energy scale vs pt in the 4 categories 
of (EB, EE) x (low R9, high R9) for MC truth, MC fit and real-data fit
with the PHOSPHOR method
'''

import os
import socket
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases
from JPsi.MuMu.common.binedges import BinEdges
from JPsi.MuMu.scaleFitter import subdet_r9_categories
from JPsi.MuMu.escale.fitResultPlotter import FitResultPlotter

ROOT.gStyle.SetPadTopMargin(0.1)
canvases.wwidth = 400
canvases.wheight = 400
canvases.yperiod = 10

categories = list(subdet_r9_categories)
binedges  = list(BinEdges([10, 12, 15, 20, 25, 30, 50]))
binedges2 = list(BinEdges([10, 12, 15, 20, 25, 30, 999]))
bincenters    = [0.5 * (lo + hi) for lo, hi in binedges]
binhalfwidths = [0.5 * (hi - lo) for lo, hi in binedges]
xgetter_factory  = lambda: lambda workspace, i = iter(bincenters)    : i.next()
exgetter_factory = lambda: lambda workspace, i = iter(binhalfwidths) : i.next()


#______________________________________________________________________________
def get_basepath():
    '''
    Return the common part of the path to data files depending
    on the host machine.
    '''
    hostname_to_basepath_map = {
        't3-susy.ultralight.org':
            '/raid2/veverka/phosphor/sge_baseline',
        'Jan-Veverkas-MacBook-Pro.local':
            '/Users/veverka/Work/Data/phosphor/sge_baseline',
        }
    return hostname_to_basepath_map[socket.gethostname()]
## End of get_basepath()


#______________________________________________________________________________
def make_list_of_sources(jobname_template):
    '''
    Returns a list of the tuples [(f1, w1, s1), ..., (fN, wN sN)]
    where (f, w, s) stand for (filename, workspace, snapshot).
    The jobname_template is expected to contain the {lo} and {hi}
    strings that will be substituted for the pt ranges, for example
    sge_mc_EB_pt{lo}to{hi}_v13_evt1of4 will be formatted to
    sge_mc_EB_pt10to12_v13_evt1of4, sge_mc_EB_pt12to15_v13_evt1of4, etc.    
    '''
    filenames, workspaces, snapshots = [], [], []

    ## Common path to all the fit result.
    basepath = get_basepath()
    ## Allways the same (due to a bug).
    basefilename = ('phosphor5_model_and_fit_'
                    'test_mc_EE_highR9_pt30to999_v13_evt1of4.root')
    ## Common to all MC fits.
    if 'mc' in jobname_template.split('_'):
        snapshot = 'mc_fit'
    else:
        snapshot = None

    ## Loop over the pt bins:
    for lo, hi in binedges2:
        ## The job name encodes the pt, category and data/MC
        jobname = jobname_template.format(lo=lo, hi=hi)
        
        filename = os.path.join(basepath, jobname, basefilename)
        workspace = jobname + '_workspace'
        
        filenames.append(filename)
        workspaces.append(workspace)
        snapshots.append(snapshot)
        
    return zip(filenames, workspaces, snapshots)
## End of make_list_of_sources(jobname_template)


#______________________________________________________________________________
def value_getter_factory(varname):
    '''
    Returns a function that takes a workspace and returns the value of the
    variable of the given name.
    '''
    return lambda workspace: workspace.var(varname).getVal()
## value_getter_factory(name)


#______________________________________________________________________________
def error_getter_factory(varname):
    '''
    Returns a function that takes a workspace and returns the error of the
    variable of the given name.
    '''
    return lambda workspace: workspace.var(varname).getError()
## error_getter_factory(name)


#______________________________________________________________________________
def var_vs_pt_getter_factory(varname):
    """
    Returns a tupler of 4 functions that take a workspace and return
    x, y, ex, ey where y and ey correspond to the value and error of
    a workspace variable of the given name and x and ex are pt bins defined
    in the global xgetter_factory function.
    """
    xgetter  = xgetter_factory()
    exgetter = exgetter_factory()
    ygetter  = value_getter_factory(varname)
    eygetter = error_getter_factory(varname)
    return (xgetter, ygetter, exgetter, eygetter)
## End of var_vs_pt_getter_factory(varname)


#______________________________________________________________________________
def value_fitresult_getter_factory(fitresult, varname):
    '''
    Returns a function that takes a workspace and returns the final value
    of a floated parameter of the given name for the given fit result 
    name.
    '''
    return lambda w: w.obj(fitresult).floatParsFinal().find(varname).getVal()
## value_fitresult_getter_factory(fitresult, varname)


#______________________________________________________________________________
def error_fitresult_getter_factory(fitresult, varname):
    '''
    Returns a function that takes a workspace and returns the final error
    of a floated parameter of the given name for the given fit result 
    name.
    '''
    return lambda w: w.obj(fitresult).floatParsFinal().find(varname).getError()
## error_fitresult_getter_factory(fitresult, varname)


#______________________________________________________________________________
def var_vs_pt_fitresult_getter_factory(fitresult, varname):
    """
    Returns a tupler of 4 functions that take a workspace and return
    x, y, ex, ey where y and ey correspond to the value and error of
    a final state of a floated parameter of a fit result stored in the 
    workspace of the given name and x and ex are pt bins defined
    in the global xgetter function.
    """
    xgetter  = xgetter_factory()
    exgetter = exgetter_factory()
    ygetter  = value_fitresult_getter_factory(fitresult, varname)
    eygetter = error_fitresult_getter_factory(fitresult, varname)
    return (xgetter, ygetter, exgetter, eygetter)
## End of var_vs_pt_fitresult_getter_factory(fitresult, varname)


#______________________________________________________________________________
def adjust_ranges(graph, xrange, yrange):
    graph.GetXaxis().SetLimits(*xrange)
    graph.GetHistogram().SetMinimum(yrange[0])
    graph.GetHistogram().SetMaximum(yrange[1])
## End of adjust_ranges

#______________________________________________________________________________
class Config():
    """Holds fitResultPlotter configuration data."""
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
## end of Config

scale_configurations = []
for cat in categories:
    for period, version in zip('2011A 2011B 2011AB'.split(),
                               'v14 v15 v13'.split()):        
        name_base = '%s_pt{lo}to{hi}_%s' % (cat.name, version)
        jobname_template0 = 'sgetest_mc_%s_evt3of4' % name_base
        jobname_template1 = 'sgetest_mc_%s_evt1of4' % name_base
        jobname_template2 = 'sgetest_mc_%s_evt2of4' % name_base
        jobname_template3 = 'sgetest_mc_%s_evt3of4' % name_base
        jobname_template4 = 'sgetest_mc_%s_evt4of4' % name_base
        if period == '2011AB':
            fitresult = 'fitresult_data'
            period_title = '2011A+B'
        else:
            fitresult = 'fitresult_' + period
            period_title = period
        cfg = Config(
            ## Canvas name
            name = '4xvalidation_scale_%s_%s' % (cat.name, period), 
            ## Canvas title
            title = ', '.join(cat.labels + (period_title,)),
            ## Axis titles
            xtitle = 'E_{T}^{#gamma} (GeV)',
            ytitle = 'E^{#gamma} Scale (%)',
            ## 0 : MC truth, 1-4: MC fit 1-4
            sources0 = make_list_of_sources(jobname_template0),
            sources1 = make_list_of_sources(jobname_template1),
            sources2 = make_list_of_sources(jobname_template2),
            sources3 = make_list_of_sources(jobname_template3),
            sources4 = make_list_of_sources(jobname_template4),
            getters0 = var_vs_pt_getter_factory('phoScaleTrue'),
            getters1 = var_vs_pt_getter_factory('phoScale'),
            getters2 = var_vs_pt_getter_factory('phoScale'),
            getters3 = var_vs_pt_getter_factory('phoScale'),
            getters4 = var_vs_pt_getter_factory('phoScale'),
            )
        scale_configurations.append(cfg)
## End of loop categories


resolution_configurations = []
for cat in categories:
    for period, version in zip('2011A 2011B 2011AB'.split(),
                               'v14 v15 v13'.split()):        
        name_base = '%s_pt{lo}to{hi}_%s' % (cat.name, version)
        jobname_template0 = 'sgetest_mc_%s_evt3of4' % name_base
        jobname_template1 = 'sgetest_mc_%s_evt1of4' % name_base
        jobname_template2 = 'sgetest_mc_%s_evt2of4' % name_base
        jobname_template3 = 'sgetest_mc_%s_evt3of4' % name_base
        jobname_template4 = 'sgetest_mc_%s_evt4of4' % name_base
        if period == '2011AB':
            fitresult = 'fitresult_data'
            period_title = '2011A+B'
        else:
            fitresult = 'fitresult_' + period
            period_title = period
        cfg = Config(
            ## Canvas name
            name = 'validation4x_resoln_%s_%s' % (cat.name, period),
            
            ## Canvas title
            title = ', '.join(cat.labels + (period_title,)),
            ## Axis titles
            xtitle = 'E_{T}^{#gamma} (GeV)',
            ytitle = 'E^{#gamma} Resolution (%)',
            ## 0 : MC truth, 1-4: MC fit 1-4
            sources0 = make_list_of_sources(jobname_template0),
            sources1 = make_list_of_sources(jobname_template1),
            sources2 = make_list_of_sources(jobname_template2),
            sources3 = make_list_of_sources(jobname_template3),
            sources4 = make_list_of_sources(jobname_template4),
            getters0 = var_vs_pt_getter_factory('phoResTrue'),
            getters1 = var_vs_pt_getter_factory('phoRes'),
            getters2 = var_vs_pt_getter_factory('phoRes'),
            getters3 = var_vs_pt_getter_factory('phoRes'),
            getters4 = var_vs_pt_getter_factory('phoRes'),
            )
        resolution_configurations.append(cfg)
## End of loop categories


plotters = []

#==============================================================================
for cfg in scale_configurations[:]:
    ## MC, EB, 2011A+B, 1 of 4 statistically independent tests
    plotter = FitResultPlotter(cfg.sources0, cfg.getters0, cfg.xtitle, 
                               cfg.ytitle, title = 'MC Truth', name=cfg.name)                          
    plotter.getdata()
    plotter.makegraph()

    for i in range(1,5):
        plotter.sources = getattr(cfg, 'sources%d' % i)
        plotter.getters = getattr(cfg, 'getters%d' % i)
        plotter.title = 'MC Fit %d' % i
        plotter.getdata()
        plotter.makegraph()

    canvases.next('c_' + cfg.name).SetGrid()
    plotter.plotall(title = cfg.title,
                    styles = [20, 25, 26, 27, 28],
                    colors = [getattr(ROOT, 'k' + c) for c in
                              'Black Red Orange Green Blue'.split()],
                    legend_position = 'topright')
    #adjust_ranges(plotter.graphs[0], (0, 60), (-11, 17))
    plotter.graphs[0].Draw('p')
    canvases.canvases[-1].Modified()
    canvases.canvases[-1].Update()
    canvases.update()
    plotters.append(plotter)
## End of loop over configurations.

#==============================================================================
for cfg in resolution_configurations[:]:
    ## MC, EB, 2011A+B, 1 of 4 statistically independent tests
    plotter = FitResultPlotter(cfg.sources0, cfg.getters0, cfg.xtitle, 
                               cfg.ytitle, title = 'MC Truth', name=cfg.name)                          
    plotter.getdata()
    plotter.makegraph()
    
    for i in range(1,5):
        plotter.sources = getattr(cfg, 'sources%d' % i)
        plotter.getters = getattr(cfg, 'getters%d' % i)
        plotter.title = 'MC Fit %d' % i
        plotter.getdata()
        plotter.makegraph()
    
    canvases.next('c_' + cfg.name).SetGrid()
    plotter.plotall(title = cfg.title,
                    styles = [20, 25, 26, 27, 28],
                    colors = [getattr(ROOT, 'k' + c) for c in
                              'Black Red Orange Green Blue'.split()],
                    legend_position = 'topright')
          
    #adjust_ranges(plotter.graphs[0], (0, 100), (-2, 17))
    plotter.graphs[0].Draw('p')
    canvases.canvases[-1].Modified()
    canvases.canvases[-1].Update()
    canvases.update()
    plotters.append(plotter)
## End of loop over configurations.

#==============================================================================
## Make histogram of the residuals
for plot in plotters:
    if 'scale' in plot.name:
        xtitle = 'Fitted - True Scale (%)'
        title = 'Scale Residuals'
    else:
        xtitle = 'Fitted - True Resolution (%)'
        title = 'Resolution Residuals'

    plot.residual_histogram = hist = ROOT.TH1F("h_" + plot.name,
                                               plot.title + ", " + title,
                                               21, -5.25, 5.25)
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle("Fits")

    ymc = plot.graphs[0].GetY()

    for graph in plot.graphs[1:]:
        for i in range(graph.GetN()):
            residual = graph.GetY()[i] - ymc[i]
            hist.Fill(residual)
    canvases.next(plot.residual_histogram.GetName())
    # hist.GetXaxis().SetRangeUser(hist.GetMean() - 3 * hist.GetRMS(),
    #                              hist.GetMean() + 3 * hist.GetRMS())
    hist.Draw()
    hist.Fit("gaus")
## End of loop over plotters

canvases.update()

h_scale_residuals = ROOT.TH1F("h_scale_residuals",
                              "Scale Residuals",
                              21, -5.25, 5.25)

h_scale_residuals_eb = ROOT.TH1F("h_scale_residuals_eb",
                                 "Barrel, Scale Residuals",
                                 21, -5.25, 5.25)

h_scale_residuals_ee = ROOT.TH1F("h_scale_residuals_ee",
                                 "Endcaps, Scale Residuals",
                                 21, -5.25, 5.25)

for i in range(4):
    h_scale_residuals.Add(plotters[i*3 + 2].residual_histogram)
for i in range(2):
    h_scale_residuals.Add(plotters[i*3 + 2].residual_histogram)
for i in range(2):
    h_scale_residuals.Add(plotters[i*3 + 8].residual_histogram)

for hist in [h_scale_residuals,
             h_scale_residuals_eb,
             h_scale_residuals_ee]:
    canvases.next(hist.GetName())
    hist.Fit("gaus")
    hist.Draw()
# print 'sources:', sources

#file = ROOT.TFile.Open(filepath)
#workspace = file.Get(jobname + '_workspace')
#workspace.Print()
