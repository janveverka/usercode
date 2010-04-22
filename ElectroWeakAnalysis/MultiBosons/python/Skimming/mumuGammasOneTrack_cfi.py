import FWCore.ParameterSet.Config as cms

mumuGammasOneTrack = cms.EDFilter("CandViewShallowCloneCombiner",
    checkCharge = cms.bool(False),
    cut = cms.string('mass > 0'),
    decay = cms.string('dimuonsOneTrack selectedPatPhotons')
)
