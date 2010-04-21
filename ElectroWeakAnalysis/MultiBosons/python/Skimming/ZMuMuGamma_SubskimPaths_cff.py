import FWCore.ParameterSet.Config as cms

from ElectroWeakAnalysis.MultiBosons.Skimming.mumuGammas_cfi import *
from ElectroWeakAnalysis.MultiBosons.Skimming.mumuGammaFilter_cfi import *

mumuGammaPath = cms.Path(
  mumuGammas *
  mumuGammaFilter
)
