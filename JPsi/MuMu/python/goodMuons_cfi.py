import FWCore.ParameterSet.Config as cms

goodMuons = cms.EDFilter("PATMuonSelector",
  src = cms.InputTag("selectedPatMuons"),
  cut = cms.string(" ".join("""
    abs(eta) < 2.4 &
    (
      (abs(eta) < 1.3 & pt > 3.3) |
      (1.3 < abs(eta) & abs(eta) < 2.2 & p > 2.9) |
      (2.2 < abs(eta) & pt > 0.8)
    ) &
    innerTrack.found > 11 &
    abs(innerTrack.d0) < 5.0 &
    abs(innerTrack.dz) < 20.0 &
    (
      isGlobalMuon &
      globalTrack.ndof > 0 &
      globalTrack.chi2 / globalTrack.ndof < 20.0
    )
    ||
    (
      !isGlobalMuon &
      isTrackerMuon &
      innerTrack.ndof > 0 &
      innerTrack.chi2 / innerTrack.ndof < 5.0 &
      muonID("TMLastStationAngTight")
    )
                            """.split())
  )
)

