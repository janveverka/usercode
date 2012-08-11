import FWCore.ParameterSet.Config as cms

glbMuons = cms.EDFilter("PATMuonSelector",
  src = cms.InputTag("selectedPatMuons"),
  cut = cms.string('isGlobalMuon = 1' +
                   '& muonID("GlobalMuonPromptTight") = 1' +
                   '& pt > 1' +
                   '& abs(dB) < 0.05' +
                   '& trackIso < 0.1' +
                   '& hcalIso < 0.1')
)

