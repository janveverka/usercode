import FWCore.ParameterSet.Config as cms

from HtoZg.MuonAnalysis.zgCands_cfi import zgCands

hasZgCand = cms.EDProducer('EventCountProducer')

zgCandSequence = cms.Sequence(zgCands + hasZgCand)
