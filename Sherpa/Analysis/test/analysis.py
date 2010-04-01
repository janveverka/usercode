import FWCore.ParameterSet.Config as cms

process = cms.Process("mcAnalysis")

process.source = cms.Source("PoolSource",
#    skipEvents = cms.untracked.uint32(5),
   fileNames = cms.untracked.vstring('file:sherpa_out.root')
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.load("Sherpa.Analysis.analysis_cfi")

process.p = cms.Path(process.analysis)

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('sherpa_ana_1K.root'),
                               # save only events passing the full path
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
                               #outputCommands = cms.untracked.vstring(
												#'drop *', 
												#'keep *_prompt*_*_*', 
						 						#'keep *_me*_*_*',
						 						#'keep *_genParticles_*_*' ) 
                               )

process.outpath = cms.EndPath(process.out)
