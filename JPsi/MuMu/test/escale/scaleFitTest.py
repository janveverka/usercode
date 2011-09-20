import copy
import os
import re
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.energyScaleChains as esChains

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *
from JPsi.MuMu.common.plotData import PlotData
from JPsi.MuMu.scaleFitter import ScaleFitter
from JPsi.MuMu.scaleFitter import PhoEtBin
from JPsi.MuMu.scaleFitter import Model
from JPsi.MuMu.scaleFitter import DimuonMassMax
from JPsi.MuMu.scaleFitter import subdet_r9_categories 
from JPsi.MuMu.scaleFitModels import ws1

gROOT.LoadMacro("CMSStyle.C")
ROOT.CMSstyle()

## Get the data
## 715/pb for Vg Summer conferences
# _chains = esChains.getChains('v7')
## 2/fb of LP11 dataset
_chains = esChains.getChains('v11')

## Default fit of s = Ereco / Ekin - 1
sfit = ScaleFitter(
    name = 's_mc',
    title = 's-Fit, Powheg S4',
    labels = ['Powheg S4'],
    cuts = [],
    source = _chains['z'],
    xName = 's',
    xTitle = 's = E_{reco}/E_{kin} - 1',
    xExpression =  '100 * (1/kRatio - 1)',
    xRange = (-50, 100),
    xUnit = '%',
    nBins = 150,
    fitRange = (-50, 100),
    pdf = 'gauss',
    graphicsExtensions = [],
    massWindowScale = 1.5,
    fitScale = 1.2,
    )

## Default fit of strue = Ereco / Egen - 1
struefit = sfit.clone(
    name = 'strue_mc',
    title = 'strue-Fit, Powheg S4',
    xTitle = 's_{true} = E_{reco}/E_{gen} - 1',
    xExpression = '100 * (phoE/phoGenE - 1)',
    xRange = (-20, 40),
    nBins = (120),
    fitRange = (-20, 40),
    fitScale = 1.2,
    cuts = ['isFSR'],
    )

eb_loR9, eb_hiR9, ee_loR9, ee_hiR9 = tuple(subdet_r9_categories)

## ----------------------------------------------------------------------------
## Customize below
sfit1 = sfit.clone().applyDefinitions([
    DimuonMassMax(85),
    eb_loR9,
    PhoEtBin(12,15)
    ])

struefit1 = struefit.clone().applyDefinitions([
    DimuonMassMax(85),
    eb_loR9,
    PhoEtBin(12,15)
    ])

_fits = [
    sfit1.clone().applyDefinitions([Model('gauss')]),
    sfit1.clone().applyDefinitions([Model('cbShape')]),
    sfit1.clone().applyDefinitions([Model('lognormal')]),
    sfit1.clone().applyDefinitions([Model('bifurGauss')]),
    sfit1.clone().applyDefinitions([Model('gamma')]),
    struefit1.clone().applyDefinitions([Model('gauss')]),
    struefit1.clone().applyDefinitions([Model('cbShape')]),
    struefit1.clone().applyDefinitions([Model('lognormal')]),
    struefit1.clone().applyDefinitions([Model('bifurGauss')]),
    struefit1.clone().applyDefinitions([Model('gamma')]),
]

maxIterations = 10
fSigma = 1.5
pullEpsilon = 0.1

## Loop over plots
for fitter in _fits:
    fitter.getMassCut(ws1)
    fitter.getData(ws1)
    try:
        fitScale = fitter.fitScale
    except AttributeError:
        fitScale = fSigma
    name = fitter.name
    Deltas = ws1.var('#Deltas')
    DeltasOld = Deltas.getVal()
    sigmaL = ws1.var('#sigmaL')
    sigmaR = ws1.var('#sigmaR')
    sigma = ws1.var('#sigma')
    k = ws1.function('k')
    m0 = ws1.function('m0')

    for iteration in range(maxIterations):
        print "++ begin iteration", iteration
        if iteration == 0:
            if not hasattr(fitter, 'fitRange'):
                fitter.fitRange = (-30, 30)
        else:
            if fitter.pdf in ['model', 'cbShape', 'gauss']:
                fitter.fitRange = ( Deltas.getVal() - fitScale * sigma.getVal(),
                                    Deltas.getVal() + fitScale * sigma.getVal() )
            elif fitter.pdf in ['cruijff', 'bifurGauss']:
                fitter.fitRange = ( Deltas.getVal() - fitScale * sigmaL.getVal(),
                                    Deltas.getVal() + fitScale * sigmaR.getVal() )
            elif fitter.pdf == 'lognormal':
                fitter.fitRange = ( 100*(m0.getVal() / pow(k.getVal(), fitScale) - 1),
                                    100*(m0.getVal() * pow(k.getVal(), fitScale) - 1) )
            elif fitter.pdf == 'gamma':
                dsVal = Deltas.getVal()
                fsVal = fitScale * sigma.getVal()
                fitter.fitRange = ( dsVal - fsVal / (1+fsVal/100),
                                    dsVal + fsVal )
            else:
                raise RuntimeError, "Unsupported PDF: %s" % fitter.pdf
        fitter.name = name + '_iter%d' % iteration
        fitter.fitToData(ws1)
        fitter.makePlot(ws1)
        if iteration == 0:
            DeltasOld = Deltas.getVal()
        else:
            pull = ( Deltas.getVal() - DeltasOld ) / Deltas.getError()
            print "pull:", pull
            DeltasOld = Deltas.getVal()
            if abs(pull) < pullEpsilon:
                break
    fitter.niter = iteration + 1

#     fitter.fitRange = ( ws1.var('#Deltas').getVal() - 20,
#                         ws1.var('#Deltas').getVal() + 20 )
#     fitter.fit(ws1)

## <-- loop over plots

## Print a spreadsheet report
# print '\nSpreadsheet report'
# for plot in _fits:
#     ws1.loadSnapshot( plot.name )
#     print '%10f\t%10f\t%s' % ( ws1.var('#Deltas').getVal(),
#                                ws1.var('#Deltas').getError(),
#                                plot.title )
## <-- loop over plots


## Print a latex report
# print "\nLatex report"
# for plot in _fits:
#     ws1.loadSnapshot( plot.name )
#     print '  %50s | %6.2f $\pm$ %4.2f \\\\' % (
#         plot.title,
#         ws1.var('#Deltas').getVal(),
#         ws1.var('#Deltas').getError()
#     )
## <-- loop over plots


## Print an ASCII report
print '\nASCII report'
is_first_sfit = True
is_first_struefit = True
for plot in _fits:
    if not hasattr(plot, 'niter'):
        continue
    ## Extract the bare name w/o the appended iteration index
    m = re.search('(.*_iter)\d+', plot.name)
    if m:
        bareName = 'sFit_' + m.groups()[0]
    else:
        raise RuntimeError, "Failed to parse fit name `%s'" % plot.name
    for i in range (plot.niter-1, plot.niter):
        ws1.loadSnapshot( bareName + '%d' % i )
        if 'sfit1' in vars() and sfit1.title in plot.title:
            if is_first_sfit:
                is_first_sfit = False
                print sfit1.title
        elif 'struefit1' in vars() and struefit1.title in plot.title:
            if is_first_struefit:
                is_first_struefit = False
                print struefit1.title
        print '%6.2f +/- %4.2f' % ( ws1.var('#Deltas').getVal(),
                                    ws1.var('#Deltas').getError() ),
        if 'sfit1' in vars() and sfit1.title in plot.title:
            print plot.title[len(sfit1.title)+2:], i, "%.3g" % plot.chi2s[i]
        elif 'struefit1' in vars() and struefit1.title in plot.title:
            print plot.title[len(struefit1.title)+2:], i, "%.3g" % plot.chi2s[i]
        else:
            print plot.title, i, "%.3g" % plot.chi2s[i]
## <-- loop over plots

ws1.writeToFile('test.root')

if __name__ == "__main__":
    import user
