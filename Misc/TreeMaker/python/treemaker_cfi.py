import FWCore.ParameterSet.Config as cms

tree = cms.EDAnalyzer("CandViewTreeMaker",
    name = cms.untracked.string("tree"),
    title = cms.untracked.string("testing TreeMaker"),
    src = cms.InputTag("cleanPatPhotonsTriggerMatch"),
    prefix = cms.untracked.string("cand"),
    sizeName = cms.untracked.string("ncands"),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("Pt"),
            quantity = cms.untracked.string("pt")
        ),
        cms.PSet(
            tag = cms.untracked.string("Eta"),
            quantity = cms.untracked.string("eta")
        ),
        cms.PSet(
            tag = cms.untracked.string("Phi"),
            quantity = cms.untracked.string("phi")
        ),
        cms.PSet(
            tag = cms.untracked.string("ZSide"),
            conditionalQuantity = cms.untracked.PSet(
                ifCondition = cms.untracked.string("eta > 0"),
                thenQuantity = cms.untracked.string("1"),
                elseQuantity = cms.untracked.string("-1")
            )
        ),
    )
)
