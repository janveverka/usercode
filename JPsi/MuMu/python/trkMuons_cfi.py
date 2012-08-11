import FWCore.ParameterSet.Config as cms

trkMuons = cms.EDFilter("PATMuonSelector",
  src = cms.InputTag("selectedPatMuons"),
  cut = cms.string('isGlobalMuon = 0 &' +
                   'isTrackerMuon = 1 &' +
                   'muonID("TMLastStationAngTight") = 1 &' +
                   'pt > 1 &' +
                   'p > 2.5 &' +
                   'abs(dB) < 0.05 &' +
                   'trackIso < 0.1 &' +
                   'hcalIso < 0.1 &')
)

