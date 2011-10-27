import array
import ROOT
import JPsi.MuMu.common.canvases as canvases
from JPsi.MuMu.datadrivenbinning import DataDrivenBinning
from JPsi.MuMu.vector import vector


nbins = 100
nentries = 5000
minBinContent = 5
maxBinContent = 500

canvases.wwidth = 400
canvases.wheight = 800

## Define a workspace
ws = ROOT.RooWorkspace('ws', 'test data-driven binning')

## Build a model
model = ws.factory('CBShape::model(x[-15,5], m[0], s[1], a[1.5], n[3])')

## Get the observable from the workspace
x = ws.var('x')

## Generate toy data
data = model.generate(ROOT.RooArgSet(x), nentries)

## Plot the data and the model overlaid
plot = x.frame(nbins)
plot.SetTitle('Default Binning')
data.plotOn(plot)
model.plotOn(plot)

## Display the plot
c1 = canvases.next('DataDrivenBinning')
c1.Divide(1,2)
c1.cd(1).SetLogy()
plot.Draw()

## Create the DataDrivenBinning object
n = data.tree().Draw(x.GetName(), '', 'goff')
bins = DataDrivenBinning(n, data.tree().GetV1(), minBinContent, maxBinContent)

## Use DataDrivenBinning to define a RooBinning
binning = bins.binning(ROOT.RooBinning())
ubinning = bins.uniformBinning(ROOT.RooUniformBinning())

## Make a second plot for comparison.
plot2 = x.frame()
plot2.SetTitle('Data-Driven Binning')

## First plot the data with uniform binning to set the per bin density
data.plotOn(plot2, ROOT.RooFit.Binning(ubinning), ROOT.RooFit.Invisible())

## Plot the data with the custom binning.
data.plotOn(plot2, ROOT.RooFit.Binning(binning))

## Get the histogram of data and set the bin centers equal to medians
hist = plot2.getHist('h_' + data.GetName())
bins.applyTo(hist)

## Overlay the data with the model
model.plotOn(plot2)

## Display the plot with the data-driven binning.
c1.cd(2).SetLogy()
plot2.Draw()
c1.Update()
