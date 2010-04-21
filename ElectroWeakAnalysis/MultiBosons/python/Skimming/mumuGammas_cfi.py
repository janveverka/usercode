import FWCore.ParameterSet.Config as cms

mumuGammas = cms.EDFilter("CandViewShallowCloneCombiner",
    checkCharge = cms.bool(False),
    cut = cms.string('mass > 0'),
    decay = cms.string('dimuons selectedPatPhotons')
)
