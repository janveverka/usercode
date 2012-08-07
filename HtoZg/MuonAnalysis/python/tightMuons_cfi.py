import FWCore.ParameterSet.Config as cms

from HtoZg.MuonAnalysis.looseMuons_cfi import looseMuons
## These are muons that pass all the cuts for the Tight ID [1] that
## can be implemented by the string parser. 
## [1] https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId

tightMuons = cms.EDFilter('PATMuonSelector',
    src = cms.InputTag('selectedPatMuons'),
    cut = cms.string(looseMuons.cut.value() + '''&&
        abs(userFloat("muonVertexing:dxy")) < 0.2 &&
        abs(userFloat("muonVertexing:dz")) < 0.5
        '''),
    filter = cms.bool(True)                                
    )

