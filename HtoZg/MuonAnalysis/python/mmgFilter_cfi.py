import FWCore.ParameterSet.Config as cms

looseDimuonFilter = cms.EDFilter('CandViewCountFilter',
    src = cms.InputTag('looseDimuons'),
    minNumber = cms.uint32(1)
    )

