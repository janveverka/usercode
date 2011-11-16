## Usual boiler plate
import copy
import sys
## Switch to ROOT's batch mode
#sys.argv.append("-b")
import JPsi.MuMu.common.roofit as roofit
import JPsi.MuMu.common.dataset as dataset

from math import log
from math import sqrt

from ROOT import gSystem
from ROOT import kRed
from ROOT import kDashed
from ROOT import RooArgSet
from ROOT import RooDataSet
from ROOT import RooFFTConvPdf
from ROOT import RooKeysPdf
from ROOT import RooRealVar
from ROOT import RooWorkspace
from ROOT import TCanvas

from JPsi.MuMu.common.roofit import AutoPrecision
from JPsi.MuMu.common.roofit import Format
from JPsi.MuMu.common.roofit import Layout
from JPsi.MuMu.common.roofit import LineColor
from JPsi.MuMu.common.roofit import LineStyle
from JPsi.MuMu.common.roofit import NumCPU
from JPsi.MuMu.common.roofit import Range
from JPsi.MuMu.common.roofit import RenameAllVariables

from JPsi.MuMu.common.energyScaleChains import getChains

gSystem.Load('libJPsiMuMu')

setattr(RooWorkspace, "Import", getattr(RooWorkspace, "import"))

## Here starts the meat.

nentries = 1000

chains = getChains('v11')
mcTree = chains['z']

w = RooWorkspace('w')

mmgMass = w.factory('mmgMass[60, 120]')
mmMass = w.factory('mmMass[0, 120]')
m1gMass = w.factory('m1gMass[0, 120]')
m2gMass = w.factory('m2gMass[0, 120]')
weight = w.factory('weight[1]')
weight.SetTitle('pileup.weight')

cuts = ['Entry$ < %d' % nentries,
        '%f < mmgMass & mmgMass < %f' % (mmgMass.getMin(), mmgMass.getMax()),
        '%f < mmMass & mmMass < %f' % (mmMass.getMin(), mmMass.getMax()),
        '%f < m1gMass & m1gMass < %f' % (m1gMass.getMin(), m1gMass.getMax()),
        '%f < m2gMass & m2gMass < %f' % (m2gMass.getMin(), m2gMass.getMax()), ]

mmgData = dataset.get(tree=mcTree, variable=mmgMass, weight=weight, cuts=cuts)
mmData = dataset.get(variable=mmMass)
m1gData = dataset.get(variable=m1gMass)
m2gData = dataset.get(variable=m2gMass)

data = mmgData
data.merge(mmData, m1gData, m2gData)

if __name__ == "__main__":
    import user

