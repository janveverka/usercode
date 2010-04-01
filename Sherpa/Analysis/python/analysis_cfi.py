import FWCore.ParameterSet.Config as cms

from SimGeneral.HepPDTESSource.pythiapdt_cfi import *
from RecoJets.Configuration.GenJetParticles_cff import *
from PhysicsTools.HepMCCandAlgos.genParticles_cfi import *

genParticles.abortOnUnknownPDGCode = False

isLepton="(abs(pdgId)=11 || abs(pdgId)=13)"
isPhoton="pdgId=22"
isStable="status=1"
isPrompt="mother(0).mother(0).status=3"
isMeLevel="status=3"
isPromptPhoton = isPhoton + "&" + isStable + "&" + isPrompt
hasLeptonMother = "6 < abs(mother(0).pdgId()) < 22"
hasPhotonMother = "mother(0).pdgId()=22"
isPhotonDaughterPromptPhoton = isPromptPhoton + "&" + hasPhotonMother
isLeptonDaughterPromptPhoton = isPromptPhoton + "&" + hasLeptonMother
isOtherDaughterPromptPhoton = isPromptPhoton + "&!" + hasPhotonMother + "&!" + hasLeptonMother

meLeptons = cms.EDFilter("GenParticleSelector",
    filter = cms.bool(False),
    src = cms.InputTag("genParticles"),
    cut = cms.string(isLepton + "&" + isMeLevel)
)

mePhotons = cms.EDFilter("GenParticleSelector",
    filter = cms.bool(False),
    src = cms.InputTag("genParticles"),
    cut = cms.string(isPhoton + "&" + isMeLevel)
)

promptLeptons = cms.EDFilter("GenParticleSelector",
    filter = cms.bool(False),
    src = cms.InputTag("genParticles"),
    cut = cms.string(isLepton + "&" + isStable + "&" + isPrompt)
)

promptPhotons = cms.EDFilter("GenParticleSelector",
    filter = cms.bool(False),
    src = cms.InputTag("genParticles"),
    cut = cms.string(isPromptPhoton)
)

photonDaughterPromptPhotons = cms.EDFilter("GenParticleSelector",
    filter = cms.bool(False),
    src = cms.InputTag("genParticles"),
    cut = cms.string(isPhotonDaughterPromptPhoton)
)

leptonDaughterPromptPhotons = cms.EDFilter("GenParticleSelector",
    filter = cms.bool(False),
    src = cms.InputTag("genParticles"),
    cut = cms.string(isLeptonDaughterPromptPhoton)
)

otherDaughterPromptPhotons = cms.EDFilter("GenParticleSelector",
    filter = cms.bool(False),
    src = cms.InputTag("genParticles"),
    cut = cms.string(isOtherDaughterPromptPhoton)
)

meLgPairs = cms.EDFilter("CandViewShallowCloneCombiner",
    checkCharge = cms.bool(False),
    cut = cms.string("mass > 0"),
    decay = cms.string("meLeptons mePhotons")
)

analysis = cms.Sequence(genParticles*(meLeptons+
                                      mePhotons+
                                      promptLeptons+
                                      promptPhotons+
                                      photonDaughterPromptPhotons+
                                      leptonDaughterPromptPhotons+
                                      otherDaughterPromptPhotons
                                      )*meLgPairs
                       )

