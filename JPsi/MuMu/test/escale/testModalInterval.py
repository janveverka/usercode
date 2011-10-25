import array
import ROOT
from JPsi.MuMu.common.modalinterval import ModalInterval, VDouble

## Get some toy data
n = 100000
data = VDouble()
data.reserve(n)
for i in range(n):
  data.push_back(ROOT.gRandom.Gaus(0,1))

## Create the ModalInterval object
mi = ModalInterval(data, 1)

## Pring the full range of toy data
print "[", mi.getLowerBound(), ",", mi.getUpperBound(), "]"

## Print the range corresponding to n effective sigma
nsigma = 0.5
mi.setSigmaLevel(nsigma)
print "[", mi.getLowerBound(), ",", mi.getUpperBound(), "]"
