import os
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.energyScaleChains as esChains

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *
from JPsi.MuMu.common.plotData import PlotData

class ScaleFitter(PlotData):
    '''Fits the Crystal Ball line shape to s = Ereco / Ekin - 1'''
    def __init__(self, name, title, source, expression, cuts, labels):
        PlotData.__init__(self, name, title, source, expression, cuts, labels)
        self.xTitle = 's = E_{RECO}/E_{KIN} - 1'
        self.nBins = 40
        self.xRange = (-30, 50)
    ## <-- __init__

    def fit(self, workspace):
        ## Pull fitted variable x, its weight w, the model
        ## and its parameters from the workspace
        x = workspace.var('s')
        w = workspace.var('w')
        model = workspace.pdf('model')
        parameters = workspace.set('parameters')

        ## Initialize latex label
        latexLabel = TLatex()
        latexLabel.SetNDC()
        latexLabel.SetTextSize(0.045)

        x.SetTitle( self.expression )
        data = dataset.get(
            tree = self.source,
            variable = x,
            weight = w,
            cuts = self.cuts
        )
        data.SetName( 'data_' + self.name )
        workspace.Import(data)

        ## Fit data
        self.fitResult = model.fitTo( data, Save(),
                                      SumW2Error(kTRUE), PrintLevel(-1) )
        workspace.saveSnapshot( self.name, parameters, True )

        ## Make a frame
        x.SetTitle(self.xTitle)
        x.setBins(self.nBins)
        frame = x.frame( Range( *self.xRange ) )

        ## Add the data and model to the frame
        data.SetTitle( self.title )
        data.plotOn( frame )
        model.plotOn( frame )
        model.paramOn( frame,
                      Format('NEU', AutoPrecision(2) ),
                      Parameters( parameters ),
                      Layout(.57, 0.92, 0.92) )

        ## Make a canvas
        self.canvas = TCanvas( self.name, self.title )
        i = len( gROOT.GetListOfCanvases() )
        self.canvas.SetWindowPosition( 20*i, 20*i )

        ## Customize
        frame.SetTitle('')

        ## Draw the frame
        frame.Draw()

        ## Add labels
        for i in range( len( self.labels ) ):
            latexLabel.DrawLatex( 0.59, 0.6 - i * 0.055, self.labels[i] )

        ## Save the plot
        self.canvas.Print( 'sFit_' + self.name + '.png' )
    ## <-- fit
## <-- ScaleFitter

if __name__ == "__main__": import user
