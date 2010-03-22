import FWCore.ParameterSet.Config as cms

process = cms.Process("FILTER")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

from Sherpa.Analysis.srcFileNames_cfi import *
process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring(srcFileNames["castorZgNoTau_0j2"]),
   fileNames = cms.untracked.vstring(srcFileNames["castorWgLep_0j1"]),
   duplicateCheckMode = cms.untracked.string("checkEachRealDataFile"),
)

process.TFileService = cms.Service(
  "TFileService",
#   fileName = cms.string("plotsNoFilterZgNoTau_0j2.root")
#   fileName = cms.string("plotsNoFilterWgLep_0j1.root")
#   fileName = cms.string("plotsWithFilterZgNoTau_0j2.root")
  fileName = cms.string("plotsWithFilterWgLep_0j1.root")
)

# from Sherpa.Analysis.genFilter_cfi import *
# from Sherpa.Analysis.genParticles_cfi import *
# from Sherpa.Analysis.drPlots_cfi import *

process.load("Sherpa.Analysis.genFilter_cfi")
process.load("Sherpa.Analysis.genParticles_cfi")
process.load("Sherpa.Analysis.drPlots_cfi")

# process.p = cms.Path(genFilter + genParticles * drPlots)
process.p = cms.Path(
  process.genFilter +
  process.genParticles *
  process.drPlots
)

#process.outpath = cms.EndPath(process.out)
