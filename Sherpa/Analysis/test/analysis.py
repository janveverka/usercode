import FWCore.ParameterSet.Config as cms

process = cms.Process("mcAnalysis")

process.source = cms.Source("PoolSource",
#    skipEvents = cms.untracked.uint32(5),
   fileNames = cms.untracked.vstring('file:sherpa_out.root')
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.genParticles.abortOnUnknownPDGCode = False
process.load("Sherpa.Analysis.analysis_cfi")


process.p = cms.Path(process.genParticles * process.printTree)
