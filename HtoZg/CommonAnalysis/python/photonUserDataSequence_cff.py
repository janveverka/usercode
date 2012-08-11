import FWCore.ParameterSet.Config as cms

from HtoZg.CommonAnalysis.photonIsolation_cfi import photonIsolation

photonUserDataSequence = cms.Sequence(photonIsolation)

