import FWCore.ParameterSet.Config as cms

from HtoZg.MuonAnalysis.tightMuons_cfi import tightMuons
from HtoZg.MuonAnalysis.tightDimuonSequence_cff import tightDimuons
from HtoZg.MuonAnalysis.tightDimuonSequence_cff import tightDimuonFilter
from HtoZg.MuonAnalysis.muonTree_cfi import muonTree
from HtoZg.MuonAnalysis.muon_selection import htozg_isolation

isolatedMuons = tightMuons.clone(
    src = cms.InputTag('tightMuons'),
    cut = cms.string(htozg_isolation)
    )

isolatedDimuons = tightDimuons.clone(
    src = cms.InputTag('isolatedMuons'),
    decay = cms.string('isolatedMuons@+ isolatedMuons@-')
    )
    
isolatedDimuonFilter = tightDimuonFilter.clone(
    src = cms.InputTag('isolatedDimuons')
    )
    
hasIsolatedDimuon = cms.EDProducer('EventCountProducer')

#muonsAfterIso = muonTree.clone(
    #src = cms.InputTag('isolatedMuons')
    #)

isolatedDimuonSequence = cms.Sequence(isolatedMuons +
                                      isolatedDimuons +
                                      isolatedDimuonFilter +
                                      hasIsolatedDimuon #+ 
                                      #muonsAfterIso
                                      )
