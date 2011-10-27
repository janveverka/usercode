import array
import ROOT
import JPsi.MuMu.common.canvases as canvases
from JPsi.MuMu.datadrivenbinning import DataDrivenBinning
from JPsi.MuMu.vector import vector

nbins = 100
nentries = 1000
minBinContent = 5
maxBinContent = 100

## Define a workspace
ws = ROOT.RooWorkspace('ws', 'test data-driven binning')

## Build a model
model = ws.factory('Gaussian::model(x[-5,5], mean[0], sigma[1])')

## Get the observable from the workspace
x = ws.var('x')

## Generate toy data
data = model.generate(ROOT.RooArgSet(x), nentries)

## Plot the data and the model overlaid
plot = x.frame(nbins)
data.plotOn(plot)
model.plotOn(plot)

## Display the plot
c1 = canvases.next('Default_Binning')
plot.Draw()
c1.Update()

## Create the DataDrivenBinning object
n = data.tree().Draw(x.GetName(), '', 'goff')
bins = DataDrivenBinning(n, data.tree().GetV1(), minBinContent, maxBinContent)

## Use DataDrivenBinning to define a RooBinning
bins.setFraction(1)
xbounds = tuple(bins.bounds())
roobins = ROOT.RooBinning(*xbounds)
for b in bins.binBoundaries():
    roobins.addBoundary(b)

## Plot the data and the model overlaid with the custom binning
plot2 = x.frame()
data.plotOn(plot2, ROOT.RooFit.Binning(roobins))
model.plotOn(plot2)

## Display the plot
c2 = canvases.next('Data_Driven_Binning')
plot2.Draw()
c2.Update()



# print "Data:"
# for i, x in enumerate(data2):
#     print '% 6.3g, ' % x,
#     if (i + 1) % 10 == 0:
#         print
# print
#
# print "Binning range:", tuple(bins.bounds())
#
# boundaries = tuple(bins.binBoundaries())
# print "Bin boundaries:", boundaries
#
# medians = tuple(bins.binMedians())
# print "Bin medians:", medians

## Pring the full range of toy data
# print "[", mi.getLowerBound(), ",", mi.getUpperBound(), "]"

## Print the range corresponding to n effective sigma
# nsigma = 0.5
# fraction = 1 - ROOT.TMath.Prob(nsigma*nsigma, 1)
# mi.setFraction(fraction)
# print "[", mi.getLowerBound(), ",", mi.getUpperBound(), "]"
