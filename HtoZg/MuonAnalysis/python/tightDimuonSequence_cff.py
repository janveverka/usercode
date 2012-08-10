import FWCore.ParameterSet.Config as cms

from HtoZg.MuonAnalysis.tightMuons_cfi import tightMuons
from HtoZg.MuonAnalysis.looseDimuons_cfi import looseDimuons
from HtoZg.MuonAnalysis.looseDimuonFilter_cfi import looseDimuonFilter
from HtoZg.MuonAnalysis.muonTree_cfi import muonTree


tightDimuons = looseDimuons.clone(
    src   = cms.InputTag('tightMuons'),
    decay = cms.string('tightMuons@+ tightMuons@-')
    )

tightDimuonFilter = looseDimuonFilter.clone(
    src = cms.InputTag('tightDimuons')
    )

hasTightDimuon = cms.EDProducer('EventCountProducer')

muonsAfterId  = muonTree.clone(
    src = cms.InputTag('tightMuons')
    )

tightDimuonSequence = cms.Sequence(tightMuons + 
                                   tightDimuons +
                                   tightDimuonFilter +
                                   hasTightDimuon +
                                   muonsAfterId)
