import FWCore.ParameterSet.Config as cms

from HtoZg.CommonAnalysis.kt6PFJetsPho_cfi import kt6PFJetsPho
from HtoZg.CommonAnalysis.photonIsolation_cfi import photonIsolation

photonIsolationSequence = cms.Sequence(
    kt6PFJetsPho +
    photonIsolation
    )
