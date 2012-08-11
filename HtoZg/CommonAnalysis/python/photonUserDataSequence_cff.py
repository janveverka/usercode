import FWCore.ParameterSet.Config as cms

from HtoZg.CommonAnalysis.conversionTools_cfi import conversionTools
from HtoZg.CommonAnalysis.photonIsolation_cfi import photonIsolation

photonUserDataSequence = cms.Sequence(conversionTools + photonIsolation)

