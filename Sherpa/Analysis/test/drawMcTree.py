import FWCore.ParameterSet.Config as cms

process = cms.Process("DrawMC")

process.source = cms.Source("PoolSource",
   skipEvents = cms.untracked.uint32(1),
   fileNames = cms.untracked.vstring('file:sherpa_out.root')
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.genParticles.abortOnUnknownPDGCode = False

process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
   src = cms.InputTag("genParticles"),
   printP4 = cms.untracked.bool(False),
   printPtEtaPhi = cms.untracked.bool(False),
   printVertex = cms.untracked.bool(False),
   printStatus = cms.untracked.bool(True),
   printIndex = cms.untracked.bool(True)
)


process.p = cms.Path(process.genParticles * process.printTree)
