import FWCore.ParameterSet.Config as cms

electronCountFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("gsfElectrons"),
    minNumber = cms.uint32(2)
    )

dielectronSkimFilterSequence = cms.Sequence(
    electronCountFilter
    )
