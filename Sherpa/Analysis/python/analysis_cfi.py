import FWCore.ParameterSet.Config as cms

from SimGeneral.HepPDTESSource.pythiapdt_cfi import *
from RecoJets.Configuration.GenJetParticles_cff import *
from PhysicsTools.HepMCCandAlgos.genParticles_cfi import *
isLepton="(pdgId=11 || pdgId=13)"
isPhoton="pdgId=22"
isStable="status=1"
isPrompt="mother(0).mother(0).status=3"
promptLeptons = cms.EDFilter("GenParticleSelector",
    filter = cms.bool(False),
    src = cms.InputTag("genParticles"),
    cut = cms.string(isLepton + "&" + isStable + "&" + isPrompt)
)

chargeParticles = cms.EDFilter("GenParticleSelector",
    filter = cms.bool(False),
    src = cms.InputTag("genParticles"),
    cut = cms.string('charge != 0 & pt > 0.29 & status = 1')
)

SherpaAnalysis = cms.Sequence(genParticles*promptLeptons*chargeParticles)
