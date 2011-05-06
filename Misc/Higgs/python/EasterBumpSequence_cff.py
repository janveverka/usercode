import FWCore.ParameterSet.Config as cms

from ElectroWeakAnalysis.MultiBosons.Selectors.photonSelector_cfi \
    import photonSelection_egammaTight2011May6 as photonSelection
from Misc.Higgs.EasterBumpTreeMaker_cfi import tree

egTightPhotons = cms.EDFilter("VGammaPhotonFilter",
    filterParams = photonSelection,
    src = cms.InputTag("cleanPatPhotonsTriggerMatch"),
    filter = cms.bool(True),
    verbosity = cms.untracked.uint32(2)
)

egTightPhotons.filterParams.minPt = 20

vbtf95Electrons = cms.EDFilter("PATElectronSelector",
    src = cms.InputTag("cleanPatElectronsTriggerMatch"),
    cut = cms.string("""isElectronIDAvailable('simpleEleId95relIso') &
                        electronID('simpleEleId95relIso') > 6.5 &
                        pt > 20""")
)

egammas = cms.EDProducer("CandViewShallowClonePtrCombiner",
    checkCharge = cms.bool(False),
    cut = cms.string("mass > 60"),
    decay = cms.string("vbtf95Electrons egTightPhotons"),
    roles = cms.vstring("electron", "photon") ## dummy roles, real ones are specified below
)

EasterBumpSequence = cms.Sequence(
    egTightPhotons *
    vbtf95Electrons *
    egammas *
    tree
)


