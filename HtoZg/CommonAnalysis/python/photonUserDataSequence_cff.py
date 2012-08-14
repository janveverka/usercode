import FWCore.ParameterSet.Config as cms

from HtoZg.CommonAnalysis.conversionTools_cfi import conversionTools
from HtoZg.CommonAnalysis.kt6PFJetsPho_cfi import kt6PFJetsPho
from HtoZg.CommonAnalysis.photonIsolation_cfi import photonIsolation

photonUserDataSequence = cms.Sequence(
    conversionTools + 
    kt6PFJetsPho + 
    photonIsolation
    )

