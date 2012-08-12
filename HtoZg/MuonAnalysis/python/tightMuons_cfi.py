import FWCore.ParameterSet.Config as cms

from HtoZg.MuonAnalysis.muon_selection import htozg_id

tightMuons = cms.EDFilter('PATMuonSelector',
    src = cms.InputTag('selectedPatMuons'),
    cut = cms.string('pt > 10 &&' + htozg_id),
    filter = cms.bool(True)                                
    )

