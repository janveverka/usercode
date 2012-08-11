import FWCore.ParameterSet.Config as cms

zgCands = cms.EDFilter('CandViewSelector',
    src = cms.InputTag('mmgCands'),
    cut = cms.string('''
        daughter("dimuon").mass > 50 &&
        max(daughter("dimuon").daughter(0).pt,
            daughter("dimuon").daughter(1).pt) > 20
        '''),
    filter = cms.bool(True)
    )
