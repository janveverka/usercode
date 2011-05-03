import FWCore.ParameterSet.Config as cms

dielectrons = cms.EDProducer("CandViewShallowClonePtrCombiner",
    checkCharge = cms.bool(False),
    cut = cms.string("mass > 20"),
    decay = cms.string("cleanPatElectronsTriggerMatch@+ cleanPatElectronsTriggerMatch@-"),
    roles = cms.vstring("electron1", "electron2")
    )

vbtf95Electrons = cms.EDFilter("PATElectronSelector",
    src = cms.InputTag("cleanPatElectronsTriggerMatch"),
    cut = cms.string("""isElectronIDAvailable('simpleEleId95relIso') & 
                        electronID('simpleEleId95relIso') > 6.5""")
    )

#goldenElectrons = cms.EDFilter("PATElectronSelector",
    #src = cms.InputTag("vbtf95Electrons"),
    #cut = cms.string("classification == 0")
    #)

#showeringElectrons = cms.EDFilter("PATElectronSelector",
    #src = cms.InputTag("vbtf95Electrons"),
    #cut = cms.string("classification == 4")
    #)

#nonShoweringElectrons = cms.EDFilter("PATElectronSelector",
    #src = cms.InputTag("vbtf95Electrons"),
    #cut = cms.string("classification != 4")
    #)

#goldenDielectrons = cms.EDProducer("CandViewShallowClonePtrCombiner",
    #checkCharge = cms.bool(False),
    #cut = cms.string("mass > 20"),
    #decay = cms.string("goldenElectrons@+ goldenElectrons@-"),
    #roles = cms.vstring("electron1", "electron2")
    #)

#showeringDielectrons = cms.EDProducer("CandViewShallowClonePtrCombiner",
    #checkCharge = cms.bool(False),
    #cut = cms.string("mass > 20"),
    #decay = cms.string("showeringElectrons@+ showeringElectrons@-"),
    #roles = cms.vstring("electron1", "electron2")
    #)

#nonShoweringDielectrons = cms.EDProducer("CandViewShallowClonePtrCombiner",
    #checkCharge = cms.bool(False),
    #cut = cms.string("mass > 20"),
    #decay = cms.string("nonShoweringElectrons@+ nonShoweringElectrons@-"),
    #roles = cms.vstring("electron1", "electron2")
    #)

inclusiveDielectrons = cms.EDProducer("CandViewShallowClonePtrCombiner",
    checkCharge = cms.bool(False),
    cut = cms.string("mass > 20"),
    decay = cms.string("vbtf95Electrons@+ vbtf95Electrons@-"),
    roles = cms.vstring("electron1", "electron2")
    )

#goldenDielectronsSequence = cms.Sequence(
    #goldenElectrons +
    #goldenDielectrons +
    #)

#showeringDielectronsSequence = cms.Sequence(
    #showeringElectrons +
    #showeringDielectrons +
    #)

#nonShoweringDielectronsSequence = cms.Sequence(
    #nonShoweringElectrons +
    #nonShoweringDielectrons +
    #)

ZeeSequence = cms.Sequence(
    dielectrons +
    vbtf95Electrons +
    inclusiveDielectrons #+
    #showeringDielectronsSequence +
    #nonShoweringDielectronSequence +
    #goldenDielectronsSequence
    )
