import FWCore.ParameterSet.Config as cms

## Default muon selection
muon_cuts_sep2012 = cms.PSet(
    minPt = cms.double(20),
    maxAbsEta = cms.double(2.4),
    isGlobalMuon = cms.bool(True),
    maxNormChi2 = cms.double(10),
    minChamberHits = cms.uint32(1),
    minStations = cms.uint32(2),
    maxAbsDxy = cms.double(0.02),
    maxAbsDz = cms.double(0.1),
    minPixelHits = cms.uint32(1),
    minTkHits = cms.uint32(11),
    maxCombRelIso = cms.double(0.1),
    )
