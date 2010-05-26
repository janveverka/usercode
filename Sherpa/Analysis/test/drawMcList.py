import FWCore.ParameterSet.Config as cms

process = cms.Process("DrawMC")

process.source = cms.Source("PoolSource",
   skipEvents = cms.untracked.uint32(0),
   fileNames = cms.untracked.vstring(
#     'file:sherpa_out.root',
    "file:/afs/cern.ch/cms/cit/veverka/vgamma/sherpa/CMSSW_3_5_8/src/Sherpa/ZgNu_0j/test/sherpa_out.root",
   )
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.genParticles.abortOnUnknownPDGCode = False

process.printTree = cms.EDAnalyzer("ParticleListDrawer",
  maxEventsToPrint = cms.untracked.int32(10),
  printVertex = cms.untracked.bool(False),
  src = cms.InputTag("genParticles")
)


process.p = cms.Path(process.genParticles * process.printTree)
