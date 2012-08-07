import FWCore.ParameterSet.Config as cms

looseDimuons = cms.EDProducer('CandViewShallowCloneCombiner',
    decay = cms.string('looseMuons@+ looseMuons@-'),
    checkCharge = cms.bool(True),
    cut = cms.string('mass > 0'),
    )

