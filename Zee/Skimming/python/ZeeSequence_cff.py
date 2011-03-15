import FWCore.ParameterSet.Config as cms

dielectrons = cms.EDProducer("CandViewShallowClonePtrCombiner",
    checkCharge = cms.bool(False),
    cut = cms.string("mass > 20"),
    decay = cms.string("cleanPatElectronsTriggerMatch@+ cleanPatElectronsTriggerMatch@-"),
    roles = cms.vstring("electron1", "electron2")
    )

vbtf95Electrons = cms.EDFilter("LazyCandViewRefSelector",
    src = cms.InputTag("cleanPatElectronsTriggerMatch"),
    cut = cms.string("""isElectronIDAvailable('simpleEleId95relIso') & 
                        electronID('simpleEleId95relIso') > 6.5""")
    )

goldenElectrons = cms.EDFilter("LazyCandViewRefSelector",
    src = cms.InputTag("vbtf95Electrons"),
    cut = cms.string("classification == 0")
    )

showeringElectrons = cms.EDFilter("LazyCandViewRefSelector",
    src = cms.InputTag("vbtf95Electrons"),
    cut = cms.string("classification == 4")
    )

goldenDielectrons = cms.EDProducer("CandViewShallowClonePtrCombiner",
    checkCharge = cms.bool(False),
    cut = cms.string("mass > 20"),
    decay = cms.string("goldenElectrons@+ goldenElectrons@-"),
    roles = cms.vstring("electron1", "electron2")
    )

goldenDielectronsSequence = cms.Sequence(
    vbtf95Electrons *
    goldenElectrons *
    goldenDielectrons
    )

ZeeSequence = cms.Sequence(
    dielectrons +
    goldenDielectronsSequence
    )
