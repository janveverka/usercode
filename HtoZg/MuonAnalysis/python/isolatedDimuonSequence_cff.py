import FWCore.ParameterSet.Config as cms

from HtoZg.MuonAnalysis.tightMuons_cfi import tightMuons
from HtoZg.MuonAnalysis.tightDimuonSequence_cff import tightDimuons
from HtoZg.MuonAnalysis.tightDimuonSequence_cff import tightDimuonFilter
from HtoZg.MuonAnalysis.muonTree_cfi import muonTree

isolatedMuons = tightMuons.clone(
    src = cms.InputTag('tightMuons'),
    cut = cms.string('userFloat("muonIsolation:combIso")/pt < 0.12')
    )

isolatedDimuons = tightDimuons.clone(
    src = cms.InputTag('isolatedMuons'),
    decay = cms.string('isolatedMuons@+ isolatedMuons@-')
    )
    
isolatedDimuonFilter = tightDimuonFilter.clone(
    src = cms.InputTag('isolatedDimuons')
    )
    
hasIsolatedDimuon = cms.EDProducer('EventCountProducer')

muonsAfterIso = muonTree.clone(
    src = cms.InputTag('isolatedMuons')
    )

isolatedDimuonSequence = cms.Sequence(isolatedMuons +
                                      isolatedDimuons +
                                      isolatedDimuonFilter +
                                      hasIsolatedDimuon + 
                                      muonsAfterIso)
