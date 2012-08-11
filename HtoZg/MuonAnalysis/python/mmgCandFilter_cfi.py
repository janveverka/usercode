import FWCore.ParameterSet.Config as cms

mmgCandFilter = cms.EDFilter('CandViewCountFilter',
    src = cms.InputTag('mmgCands'),
    minNumber = cms.uint32(1)
    )

