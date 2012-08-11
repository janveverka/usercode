import FWCore.ParameterSet.Config as cms

HtoZgCands = cms.EDFilter('CandViewSelector',
    src = cms.InputTag('zgCands'),
    cut = cms.string('mass > 110'),
    filter = cms.bool(True)
    )
