import FWCore.ParameterSet.Config as cms

mumuGammaFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("mumuGammas"),
    minNumber = cms.uint32(1)
)

