import os
import re
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.energyScaleChains as esChains

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *
from JPsi.MuMu.common.plotData import PlotData
from JPsi.MuMu.scaleFitter import ScaleFitter
from JPsi.MuMu.scaleFitModels import *

gROOT.LoadMacro("CMSStyle.C")
ROOT.CMSstyle()

## Get the data
## 715/pb for Vg Summer conferences
# _chains = esChains.getChains('v7')
## 2/fb of LP11 dataset
_chains = esChains.getChains('v10')

## Cuts common to all plots
_commonCuts = [
#     'abs(1/kRatio - 1) < 0.5',
#     'abs(mmgMass-90.0) < 4',
    'mmMass < 80'
    # 'abs(scEta) < 0.9',
]

## ----------------------------------------------------------------------------
## Customize below
_fits = [

    ScaleFitter(
        name = 'EB_lowR9_mc_pt10-12_gauss_mmMass85',
        title = 'Barrel, R9 < 0.94, pt 10-12 GeV, MC, Gauss, m(mm) < 85 GeV',
        labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'E_{T}^{#gamma} #in [10, 12] GeV', 'Powheg S4', 'Gauss', 'm_{#mu^{+}#mu^{-}} < 85 GeV' ],
        cuts = ['phoIsEB', 'phoR9 < 0.94', '10 < phoPt', 'phoPt < 12', 'mmMass<85'],
        source = _chains['z'],
        expression = '100 * (1/kRatio - 1)',
        xRange = (-50, 150),
        nBins = 200,
        fitRange = (-100, 100),
        pdf = 'gauss',
        graphicsExtensions = ['png'],
        massWindowScale = 1.5,
        fitScale = 1.2
    ),

    ScaleFitter(
        name = 'EB_lowR9_mc_pt10-12_gauss_mmMass80',
        title = 'Barrel, R9 < 0.94, pt 10-12 GeV, MC, Gauss, m(mm) < 80 GeV',
        labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'E_{T}^{#gamma} #in [10, 12] GeV', 'Powheg S4', 'Gauss', 'm_{#mu^{+}#mu^{-}} < 80 GeV' ],
        cuts = ['phoIsEB', 'phoR9 < 0.94', '10 < phoPt', 'phoPt < 12', 'mmMass<80'],
        source = _chains['z'],
        expression = '100 * (1/kRatio - 1)',
        xRange = (-50, 150),
        nBins = 200,
        fitRange = (-100, 100),
        pdf = 'gauss',
        graphicsExtensions = ['png'],
        massWindowScale = 1.5,
        fitScale = 1.2
    ),

    ScaleFitter(
        name = 'EB_lowR9_mc_pt10-12_gauss_mmMass75',
        title = 'Barrel, R9 < 0.94, pt 10-12 GeV, MC, Gauss, m(mm) < 75 GeV',
        labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'E_{T}^{#gamma} #in [10, 12] GeV', 'Powheg S4', 'Gauss', 'm_{#mu^{+}#mu^{-}} < 75 GeV' ],
        cuts = ['phoIsEB', 'phoR9 < 0.94', '10 < phoPt', 'phoPt < 12', 'mmMass<75'],
        source = _chains['z'],
        expression = '100 * (1/kRatio - 1)',
        xRange = (-50, 150),
        nBins = 200,
        fitRange = (-100, 100),
        pdf = 'gauss',
        graphicsExtensions = ['png'],
        massWindowScale = 1.5,
        fitScale = 1.2
    ),

    ## Barrel, MC, high R9
    ScaleFitter(
        name = 'EB_lowR9_mc_pt30-999_lognormal',
        title = 'Barrel, R9 < 0.94, pt 30-999 GeV, MC, Lognormal',
        source = _chains['z'],
        expression = '100 * (1/kRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 < 0.94', '30 < phoPt', 'phoPt < 999'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'E_{T}^{#gamma} > 30 GeV', 'Powheg S4', 'Lognormal' ],
        xRange = (-20, 50),
        nBins = 120,
        fitRange = (-100, 100),
        pdf = 'lognormal',
#         graphicsExtensions = ['png', 'eps'],
        graphicsExtensions = ['png'],
        massWindowScale = 1.5,
        fitScale = 1.5
    ),

    ScaleFitter(
        name = 'EB_lowR9_mc_pt30-999_bifurGauss',
        title = 'Barrel, R9 < 0.94, pt 30-999 GeV, MC, Bifur. Gauss',
        source = _chains['z'],
        expression = '100 * (1/kRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 < 0.94', '30 < phoPt', 'phoPt < 999'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'E_{T}^{#gamma} > 30 GeV', 'Powheg S4', 'Bifur. Gauss' ],
        xRange = (-20, 40),
        nBins = 120,
        fitRange = (-100, 100),
        pdf = 'bifurGauss',
#         graphicsExtensions = ['png', 'eps'],
        graphicsExtensions = ['png'],
        massWindowScale = 1.5,
        fitScale = 1.5
    ),

    ScaleFitter(
        name = 'EB_lowR9_mc_pt30-999_gauss',
        title = 'Barrel, R9 < 0.94, pt 30-999 GeV, MC, Gauss',
        source = _chains['z'],
        expression = '100 * (1/kRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 < 0.94', '30 < phoPt', 'phoPt < 999'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'E_{T}^{#gamma} > 30 GeV', 'Powheg S4', 'Gauss' ],
        xRange = (-20, 40),
        nBins = 120,
        fitRange = (-100, 100),
        pdf = 'gauss',
#         graphicsExtensions = ['png', 'eps'],
        graphicsExtensions = ['png'],
        massWindowScale = 1.5,
        fitScale = 1.5
    ),

    ScaleFitter(
        name = 'EB_lowR9_mc_pt30-999_cbShape',
        title = 'Barrel, R9 < 0.94, pt 30-999 GeV, MC, CB',
        source = _chains['z'],
        expression = '100 * (1/kRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 < 0.94', '30 < phoPt', 'phoPt < 999'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'E_{T}^{#gamma} > 30 GeV', 'Powheg S4', 'Crystal Ball' ],
        xRange = (-20, 40),
        nBins = 120,
        fitRange = (-100, 100),
        pdf = 'cbShape',
#         graphicsExtensions = ['png', 'eps'],
        graphicsExtensions = ['png'],
        massWindowScale = 1.5,
        fitScale = 1.5
    ),

#     ScaleFitter(
#         name = 'EB_highR9_mc_pt10-15_cbShape',
#         title = 'Barrel, R9 > 0.94, pt 10-15 GeV, MC, CB',
#         source = _chains['z'],
#         expression = '100 * (1/kRatio - 1)',
#         cuts = _commonCuts + ['phoIsEB', 'phoR9 > 0.94', '10 < phoPt', 'phoPt < 15'],
#         labels = [ 'Barrel', 'R_{9}^{#gamma} > 0.94', 'E_{T}^{#gamma} #in [10,15] GeV', 'Powheg S4', 'CB' ],
#         fitRange = (-20, 20),
#         pdf = 'cbShape',
#     ),
#
#     ScaleFitter(
#         name = 'EB_highR9_mc_pt10-15_cruijff',
#         title = 'Barrel, R9 > 0.94, pt 10-15 GeV, MC, Cruijff',
#         source = _chains['z'],
#         expression = '100 * (1/kRatio - 1)',
#         cuts = _commonCuts + ['phoIsEB', 'phoR9 > 0.94', '10 < phoPt', 'phoPt < 15'],
#         labels = [ 'Barrel', 'R_{9}^{#gamma} > 0.94', 'E_{T}^{#gamma} #in [10,15] GeV', 'Powheg S4', 'Cruijff' ],
#         fitRange = (-20, 20),
#         pdf = 'cruijff',
#     ),
#
#     ScaleFitter(
#         name = 'EB_highR9_mc_pt10-15_bifurGauss',
#         title = 'Barrel, R9 > 0.94, pt 10-15 GeV, MC, Bifur. Gauss',
#         source = _chains['z'],
#         expression = '100 * (1/kRatio - 1)',
#         cuts = _commonCuts + ['phoIsEB', 'phoR9 > 0.94', '10 < phoPt', 'phoPt < 15'],
#         labels = [ 'Barrel', 'R_{9}^{#gamma} > 0.94', 'E_{T}^{#gamma} #in [10,15] GeV', 'Powheg S4', 'Bifur. Gaus' ],
#         fitRange = (-20, 20),
#         pdf = 'bifurGauss',
#     ),
#
#
#     ScaleFitter(
#         name = 'EB_highR9_mc_pt10-15_bifurLogNormal',
#         title = 'Barrel, R9 > 0.94, pt 10-15 GeV, MC, -log(k)',
#         source = _chains['z'],
#         expression = '- 100 * log(kRatio)',
#         cuts = _commonCuts + ['phoIsEB', 'phoR9 > 0.94', '10 < phoPt', 'phoPt < 15'],
#         labels = [ 'Barrel', 'R_{9}^{#gamma} > 0.94', 'E_{T}^{#gamma} #in [10,15] GeV', 'Powheg S4', 'Bifur. Log-Normal' ],
#     ),

    ## Barrel, MC, low R9, old corrections
#     ScaleFitter(
#         name = 'EB_lowR9_mc_default_pt10-15',
#         title = 'Barrel, R9 < 0.94, pt 10-15 GeV, MC, default corrections',
#         source = _chains['z'],
#         expression = '100 * (1/kRatio - 1)',
#         cuts = _commonCuts + [ 'phoIsEB',
#                                'phoR9 < 0.94',
#                                '10 < phoPt', 'phoPt < 15' ],
#         labels = [ 'Barrel',
#                    'R_{9}^{#gamma} < 0.94',
#                    'E_{T}^{#gamma} #in [10,15] GeV',
#                    'Powheg S4',
#                    'Default Corr.' ],
#         fitRange = (-30, 30),
#     ),

#     ScaleFitter(
#         name = 'EB_lowR9_mc_default_pt10-15_mlogk',
#         title = 'Barrel, R9 < 0.94, pt 10-15 GeV, MC, default corrections, -log(k)',
#         source = _chains['z'],
#         expression = '- 100 * log(kRatio)',
#         cuts = _commonCuts + [ 'phoIsEB',
#                                'phoR9 < 0.94',
#                                '10 < phoPt', 'phoPt < 15' ],
#         labels = [ 'Barrel',
#                    'R_{9}^{#gamma} < 0.94',
#                    'E_{T}^{#gamma} #in [10,15] GeV',
#                    'Powheg S4',
#                    'Default Corr.' ],
#     ),

    ## Barrel, MC, low R9, new corrections
#     ScaleFitter(
#         name = 'EB_lowR9_mc_new_pt10-15',
#         title = 'Barrel, R9 < 0.94, pt 10-15 GeV, MC, new corrections',
#         source = _chains['z'],
#         expression = '100 * (1/newCorrKRatio - 1)',
#         cuts = _commonCuts + [ 'phoIsEB',
#                                'phoR9 < 0.94',
#                                '10 < phoPt', 'phoPt < 15' ],
#         labels = [ 'Barrel',
#                    'R_{9}^{#gamma} < 0.94',
#                    'E_{T}^{#gamma} #in [10,15] GeV',
#                    'Powheg S4',
#                    'New Corr.' ],
#     ),

#     ScaleFitter(
#         name = 'EB_lowR9_mc_new_pt10-15_mlogk',
#         title = 'Barrel, R9 < 0.94, pt 10-15 GeV, MC, new corrections, -log(k)',
#         source = _chains['z'],
#         expression = '- 100 * log(newCorrKRatio)',
#         cuts = _commonCuts + [ 'phoIsEB',
#                                'phoR9 < 0.94',
#                                '10 < phoPt', 'phoPt < 15' ],
#         labels = [ 'Barrel',
#                    'R_{9}^{#gamma} < 0.94',
#                    'E_{T}^{#gamma} #in [10,15] GeV',
#                    'Powheg S4',
#                    'New Corr.' ],
#     ),
]

maxIterations = 10
fSigma = 1.5
pullEpsilon = 0.1

## Loop over plots
for fitter in _fits[3:4]:
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
for plot in _fits:
    if not hasattr(plot, 'niter'):
        continue
    ## Extract the bare name w/o the appended iteration index
    m = re.search('(.*_iter)\d+', plot.name)
    if m:
        bareName = 'sFit_' + m.groups()[0]
    else:
        raise RuntimeError, "Failed to parse fit name `%s'" % plot.name
    for i in range (plot.niter):
        ws1.loadSnapshot( bareName + '%d' % i )
        print '%6.2f +/- %4.2f' % ( ws1.var('#Deltas').getVal(),
                                    ws1.var('#Deltas').getError() ),
        print plot.title, i, "%.3g" % plot.chi2s[i]
## <-- loop over plots

ws1.writeToFile('test.root')

if __name__ == "__main__": import user
