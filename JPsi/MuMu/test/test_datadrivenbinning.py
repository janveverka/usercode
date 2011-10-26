import array
import ROOT
from JPsi.MuMu.datadrivenbinning import DataDrivenBinning
from JPsi.MuMu.vector import vector

## Get some toy data
n = 100000
data = vector('double')()
data.reserve(n)
for i in range(n):
  data.push_back(ROOT.gRandom.Gaus(0,1))

## Create the ModalInterval object
bins = DataDrivenBinning(data, 1)

## Pring the full range of toy data
# print "[", mi.getLowerBound(), ",", mi.getUpperBound(), "]"

## Print the range corresponding to n effective sigma
# nsigma = 0.5
# fraction = 1 - ROOT.TMath.Prob(nsigma*nsigma, 1)
# mi.setFraction(fraction)
# print "[", mi.getLowerBound(), ",", mi.getUpperBound(), "]"
