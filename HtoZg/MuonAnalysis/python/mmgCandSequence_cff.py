import FWCore.ParameterSet.Config as cms

from HtoZg.MuonAnalysis.mmgCands_cfi import mmgCands
from HtoZg.MuonAnalysis.mmgCandFilter_cfi import mmgCandFilter
from HtoZg.MuonAnalysis.mmgTree_cfi import mmgTree

hasMmgCand = cms.EDProducer('EventCountProducer')
mmgAfterDR = mmgTree.clone()

mmgCandSequence = cms.Sequence(mmgCands + 
                               mmgCandFilter + 
                               hasMmgCand + 
                               mmgAfterDR)
