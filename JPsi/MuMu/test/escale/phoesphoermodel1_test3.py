'''
Build 1D model fT(t|s,r) for log(mmgMass^2 - mmMass^2) as functions of
PhoES and PhoER through a confolution in t
fT(t|s,r) = fT1(t) * fT2(t|s,r).
Test that it closes on smeared MC.

Jan Veverka, Caltech, 18 January 2012
'''

##- Boilerplate imports --------------------------------------------------------

import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.energyScaleChains import getChains
from JPsi.MuMu.common.latex import Latex
from JPsi.MuMu.common.parametrizedkeyspdf import ParametrizedKeysPdf
from JPsi.MuMu.escale.logphoereskeyspdf import LogPhoeresKeysPdf
from JPsi.MuMu.escale.montecarlocalibrator import MonteCarloCalibrator

##-- Configuration -------------------------------------------------------------
## Selection
name = 'EB_highR9_pt20-25'
cuts = ['mmMass + mmgMass < 190',
        'isFSR',
        'phoGenE > 0',
        ]

##------------------------------------------------------------------------------
def parse_name_to_cuts():
    'Parse the name and apply the relevant cuts.'
    if 'EB' in name:
        cuts.append('phoIsEB')
        if 'highR9' in name:
            cuts.append('phoR9 > 0.94')
        elif 'lowR9' in name:
            cuts.append('phoR9 < 0.94')
    elif 'EE' in name:
        cuts.append('!phoIsEB')
        if 'highR9' in name:
            cuts.append('phoR9 > 0.95')
        elif 'lowR9' in name:
            cuts.append('phoR9 < 0.95')

    if 'pt' in name:
        ## Split the name into tokens.
        for tok in name.split('_'):
            ## Get the token with the pt
            if 'pt' in tok:
                lo, hi = tok.replace('pt', '').split('-')
                cuts.append('%s <= phoPt & phoPt < %s' % (lo, hi))
## End of parse_name_to_cuts().

##------------------------------------------------------------------------------
def init():
    'Initialize workspace and common variables and functions.'
    parse_name_to_cuts()
    ## Create the default workspace
    global w
    w = ROOT.RooWorkspace('w')

    ## Define data observables. 
    global mmgMass, mmMass, phoERes, mmgMassPhoGenE, weight
    mmgMass = w.factory('mmgMass[40, 140]')
    mmgMassPhoGenE = w.factory('mmgMassPhoGenE[0, 200]')
    mmMass = w.factory('mmMass[10, 140]')
    phoERes = w.factory('phoERes[-70, 100]')
    weight = w.factory('weight[1]')

    ## Define model parameters.
    global phoScale, phoRes
    phoScale = w.factory('phoScale[0,-50,50]')
    phoRes = w.factory('phoRes[3,0.01,50]')

    ## Set units.
    for x, u in zip([phoScale, phoRes],
                    '% %'.split()):
        x.setUnit(u)

    ## Prep for storing fit results in the workspace.
    global phoScaleTarget, phoResTarget, params
    phoScaleTarget = w.factory('phoScaleTarget[0,-50,50]')
    phoResTarget = w.factory('phoResTarget[5,0.01,50]')
    params = ROOT.RooArgSet(phoScaleTarget, phoResTarget)
    w.defineSet('params', params)
## End of init().


##------------------------------------------------------------------------------
def get_data(zchain = getChains('v11')['z']):
    'Get the nominal data that is used for smearing.'
    ## The TFormula expression defining the data is given in the titles.
    weight.SetTitle('pileup.weight')
    phoERes.SetTitle('100 * phoERes')
    mmgMassPhoGenE.SetTitle('threeBodyMass(mu1Pt, mu1Eta, mu1Phi, 0.106, '
                            '              mu2Pt, mu2Eta, mu2Phi, 0.106, '
                            '              phoGenE * phoPt / phoE, '
                            '                     phoEta, phoPhi, 0)')
    ## Create a preselected tree
    tree = zchain.CopyTree('&'.join(cuts))
    ## Have to copy aliases by hand
    for a in zchain.GetListOfAliases():
        tree.SetAlias(a.GetName(), a.GetTitle())

    ## Get the nominal dataset
    global data
    data = dataset.get(tree=tree, weight=weight, cuts=cuts,
                       variables=[mmgMass, mmMass, phoERes, mmgMassPhoGenE])

    ## Set units and nice titles
    for x, t, u in zip([mmgMass, mmgMassPhoGenE, mmMass, phoERes],
                       ['reconstructed m_{#mu#mu#gamma}',
                        'reconstructed m_{#mu#mu#gamma} with E_{gen}^{#gamma}',
                        'm_{#mu#mu}',
                        'E_{reco}^{#gamma}/E_{gen}^{#gamma} - 1', ],
                       'GeV GeV GeV %'.split()):
        x.SetTitle(t)
        x.setUnit(u)
    ##-- Get Smeared Data ------------------------------------------------------
    ## Enlarge the range of the observable to get vanishing tails.
    range_save = (phoERes.getMin(), phoERes.getMax())
    phoERes.setRange(-90, 150)
    global calibrator
    calibrator = MonteCarloCalibrator(data)
    phoERes.setRange(*range_save)
## End of get_data.

##------------------------------------------------------------------------------
sw = ROOT.TStopwatch()
sw.Start()

init()
get_data()

## Define variables
t = w.factory('t[0,5,10]')

## Get t1 data
t1func = w.factory(
    'expr::t1func("log(mmgMassPhoGenE^2 - mmMass^2)", {mmgMassPhoGenE, mmMass})'
    )
t1func.SetName('t')
data.addColumn(t1func)
t1data = data.reduce(ROOT.RooArgSet(t))
t1func.SetName('t1func')
data = data.reduce(ROOT.RooArgSet(mmgMass, mmMass, phoERes, mmgMassPhoGenE))

## Get t2 data
t.setRange(-1, 1)
t2func = w.factory(
    'expr::t2func("log(0.01 * phoERes + 1)", {phoERes})'
    )
t2func.SetName('t')
data.addColumn(t2func)
t2func.SetName('t2func')
t2data = data.reduce(ROOT.RooArgSet(t))
data = data.reduce(ROOT.RooArgSet(mmgMass, mmMass, phoERes, mmgMassPhoGenE))

## Get t data
t.setRange(5, 10)
tfunc = w.factory('expr::tfunc("log(mmgMass^2 - mmMass^2)", {mmgMass, mmMass})')
tfunc.SetName('t')
data.addColumn(tfunc)
tfunc.SetName('tfunc')
tdata = data.reduce(ROOT.RooArgSet(t))
data = data.reduce(ROOT.RooArgSet(mmgMass, mmMass, phoERes, mmgMassPhoGenE))

## Build the model fT1(t1) for log(mmgMassPhoGenE^2 - mmMass^2)
t.setRange(5, 10)
nomirror = ROOT.RooKeysPdf.NoMirror
t1pdf = ROOT.RooKeysPdf('t1pdf', 't1pdf', t, t1data, nomirror, 1.5)

## Build the model fT2(t2|s,r) for log(Ereco/Egen) ft2(t2|r,s)
t.setRange(-1, 1)
t2pdf = LogPhoeresKeysPdf('t2pdf', 't2pdf', phoERes, t, phoScale, phoRes, data,
                          rho=1.5)

## Build the model for fT(t|s,r) = fT1(t1) * fT2(t2|s,r)
t.setRange(5, 10)
t.setBins(1000, "cache")
tpdf = ROOT.RooFFTConvPdf('tpdf', 'tpdf', t, t1pdf, t2pdf)
tpdf.setBufferFraction(0.1)

## Plot fT1(t1) with training data.
canvases.next('t1pdf').SetGrid()
t.setRange(5, 10)
t.SetTitle('log(m_{#mu#mu#gamma,E_{gen}^{#gamma}}^{2} - m_{#mu#mu}^{2})')
plot = t.frame(roo.Range(7.5, 9))
t1data.plotOn(plot)
t1pdf.plotOn(plot)
plot.Draw()

## Plot fT2(t2|s,r) fitted to training data.
canvases.next('t2pdf').SetGrid()
t.setRange(-1, 1)
t.SetTitle('log(E_{reco}^{#gamma}/E_{gen}^{#gamma})')
t2pdf.fitTo(t2data, roo.Range(ROOT.TMath.Log(0.5), ROOT.TMath.Log(2.0)))
plot = t.frame(roo.Range(-0.15, 0.15))
t2data.plotOn(plot)
t2pdf.plotOn(plot)
plot.Draw()
Latex([
    's_{shape}: %.3f %%' % t2pdf.s0val,
    's_{sfit}: %.3f #pm %.3f %%' % (phoScale.getVal(), phoScale.getError()),
    's_{fit} - s_{shape}: %.4f #pm %.4f %%' % (
        phoScale.getVal() - t2pdf.s0val,
        phoScale.getError()
        ),
    'r_{shape}: %.3f %%' % t2pdf.r0val,
    'r_{fit}: %.3f #pm %.3f %%' % (phoRes.getVal(), phoRes.getError()),
    'r_{fit}/r_{shape}: %.4f #pm %.4f' % (
        phoRes.getVal() / t2pdf.r0val,
        phoRes.getError() / t2pdf.r0val),
    ], position=(0.2, 0.75)).draw()

## Plot fT(t|s,r) fitted to data
canvases.next('tpdf').SetGrid()
t.setRange(5, 10)
t.SetTitle('log(m_{#mu#mu#gamma}^{2} - m_{#mu#mu}^{2})')
tpdf.fitTo(tdata, roo.Range(6.5, 10))
plot = t.frame(roo.Range(7.5, 9))
tdata.plotOn(plot)
tpdf.plotOn(plot)
tpdf.paramOn(plot)
plot.Draw()
tdata.plotOn(plot)

canvases.update()
sw.Stop()
print 'CPU time:', sw.CpuTime(), 's, real time:', sw.RealTime(), 's'
 

if __name__ == '__main__':
    # main()
    import user