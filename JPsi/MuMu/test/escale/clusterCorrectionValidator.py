import os
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.energyScaleChains as esChains

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *
from JPsi.MuMu.common.plotData import PlotData

## Get the data
_chains = esChains.getChains('v7')

## Cuts common to all plots
_commonCuts = [
    'abs(1/kRatio - 1) < 0.5',
    'abs(mmgMass-91.2) < 4',
]

## Add common data
class SFitPlotData(PlotData):
    def __init__(self, name, title, source, expression, cuts, labels):
        PlotData.__init__(self, name, title, source, expression, cuts, labels)
        self.xTitle = 's = E_{RECO}/E_{KIN} - 1'
        self.nBins = 40
        self.xRange = (-30, 50)


## ----------------------------------------------------------------------------
## Customize below
_plots = [
    ## Barrel, Data
    SFitPlotData(
        name = 'EB_highR9_data',
        title = 'Barrel, R9 > 0.94, data',
        source = _chains['data'],
        expression = '100 * (1/kRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 > 0.94'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} > 0.94', 'L = 750 pb^{-1}' ],
    ),
    SFitPlotData(
        name = 'EB_lowR9_data_default',
        title = 'Barrel, R9 < 0.94, data, default corrections',
        source = _chains['data'],
        expression = '100 * (1/kRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 < 0.94'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'L = 750 pb^{-1}',
                   'Default Corr.' ],
    ),
    SFitPlotData(
        name = 'EB_lowR9_data_default_closure',
        title = 'Barrel, R9 < 0.94, data, default corrections, closure test',
        source = _chains['data'],
        expression = '100 * (1/corrKRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 < 0.94'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'L = 750 pb^{-1}',
                   'Default Corr.', 'Closure Test' ],
    ),
    SFitPlotData(
        name = 'EB_lowR9_data_new',
        title = 'Barrel, R9 < 0.94, data, new corrections',
        source = _chains['data'],
        expression = '100 * (1/newCorrKRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 < 0.94'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'L = 750 pb^{-1}',
                   'New Corr.' ],
    ),

    ## Barrel, MC
    SFitPlotData(
        name = 'EB_highR9_mc',
        title = 'Barrel, R9 > 0.94, Pythia S3',
        source = _chains['z'],
        expression = '100 * (1/kRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 > 0.94'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} > 0.94', 'Pythia S3' ],
    ),
    SFitPlotData(
        name = 'EB_lowR9_mc_default',
        title = 'Barrel, R9 < 0.94, Pythia S3, default corrections',
        source = _chains['z'],
        expression = '100 * (1/kRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 < 0.94'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'Pythia S3',
                   'Default Corr.' ],
    ),
    SFitPlotData(
        name = 'EB_lowR9_mc_default_closure',
        title = 'Barrel, R9 < 0.94, Pythia S3, default corrections, closure test',
        source = _chains['z'],
        expression = '100 * (1/corrKRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 < 0.94'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'Pythia S3',
                   'Default Corr.', 'Closure Test' ],
    ),
    SFitPlotData(
        name = 'EB_lowR9_mc_new',
        title = 'Barrel, R9 < 0.94, Pythia S3, new corrections',
        source = _chains['z'],
        expression = '100 * (1/newCorrKRatio - 1)',
        cuts = _commonCuts + ['phoIsEB', 'phoR9 < 0.94'],
        labels = [ 'Barrel', 'R_{9}^{#gamma} < 0.94', 'Pythia S3',
                   'New Corr.' ],
    ),
]



## Define the workspace
ws1 = RooWorkspace( 'ws1', 'mmg energy scale' )

## Define the quantity to be fitted
x = RooRealVar( 's', '100 * (1/kRatio - 1)', -50, 50, '%' )

w = RooRealVar( 'w', '1', 0, 99 )

xw = RooArgSet(x, w)
ws1.Import(xw)

model = ws1.factory("""CBShape::crystalBall( s,
                                             #Deltas[0, -50, 50],
                                             #sigma[20, 0.001, 100],
                                             #alpha[-1.5, -10, 0],
                                             n[1.5, 0.1, 10] )""")

## Define observables and parameters
observables = RooArgSet(x)
parameters = model.getParameters(observables)
ws1.defineSet("parameters", parameters)
ws1.saveSnapshot("initial", parameters, True)

## Initialize latex label
latexLabel = TLatex()
latexLabel.SetNDC()
latexLabel.SetTextSize(0.045)

## Loop over plots
for plot in _plots:
    ## Get the RooDataset
    x.SetTitle( plot.expression )
    data = dataset.get(
        tree = plot.source,
        variable = x,
        weight = w,
        cuts = plot.cuts
    )
    data.SetName( 'data_' + plot.name )
    ws1.Import(data)

    ## Fit data
    plot.fitResult = model.fitTo( data, Save(), SumW2Error(kTRUE), PrintLevel(-1) )
    ws1.saveSnapshot( plot.name, parameters, True )

    ## Make a frame
    x.SetTitle(plot.xTitle)
    x.setBins(plot.nBins)
    frame = x.frame( Range( *plot.xRange ) )

    ## Add the data and model to the fram
    data.SetTitle( plot.title )
    data.plotOn( frame )
    model.plotOn( frame )
    model.paramOn( frame,
                   Format('NEU', AutoPrecision(2) ),
                   Parameters( parameters ),
                   Layout(.57, 0.92, 0.92) )

    ## Make a canvas
    plot.canvas = TCanvas( plot.name, plot.title )
    i = _plots.index( plot )
    plot.canvas.SetWindowPosition( 20*i, 20*i )

    ## Customize
    frame.SetTitle('')

    ## Draw the frame
    frame.Draw()

    ## Add labels
    for i in range( len( plot.labels ) ):
        latexLabel.DrawLatex( 0.59, 0.6 - i * 0.055, plot.labels[i] )

    ## Save the plot
    plot.canvas.Print( 'sFit_' + plot.name + '.png' )

## <-- loop over plots

if __name__ == "__main__": import user
