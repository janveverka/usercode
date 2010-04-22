import FWCore.ParameterSet.Config as cms

mumuGammaOneTrackFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("mumuGammasOneTrack"),
    minNumber = cms.uint32(1)
)

