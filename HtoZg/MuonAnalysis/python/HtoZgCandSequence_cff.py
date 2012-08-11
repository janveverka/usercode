import FWCore.ParameterSet.Config as cms

from HtoZg.MuonAnalysis.HtoZgCands_cfi import HtoZgCands

hasHtoZgCand = cms.EDProducer('EventCountProducer')

HtoZgCandSequence = cms.Sequence(HtoZgCands + hasHtoZgCand)
