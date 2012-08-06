import FWCore.ParameterSet.Config as cms

from HtoZg.MuonAnalysis.hltFilter_cfi import hltFilter

passHltFilter    = cms.EDProducer('EventCountProducer')
hltFilterSequence = cms.Sequence(hltFilter + passHltFilter)