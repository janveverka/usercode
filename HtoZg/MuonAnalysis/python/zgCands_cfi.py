import FWCore.ParameterSet.Config as cms

zgCands = cms.EDFilter('CandViewSelector',
    src = cms.InputTag('mmgCands'),
    cut = cms.string('daughter("dimuon").mass > 50'),
    filter = cms.bool(True)
    )
