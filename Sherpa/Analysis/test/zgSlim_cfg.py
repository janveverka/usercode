import sys
import FWCore.ParameterSet.Config as cms

## Job name can be passed as a command-line argument
if len(sys.argv) > 0 and 'Zgg' in sys.argv[-1]:
    jobs = sys.argv[-1]
else:
    job = '7TeV_Zgg_h3z_h4z_v2'

process = cms.Process("HISTO")

## Load process attributes
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("Sherpa.Analysis.zgSlimSequence_cff")

## MessageLogger
process.MessageLogger.cerr.FwkReport.reportEvery = 10

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
    "rfio:/cms/veverka/Sherpa/%s/test/sherpa_10k_out.root" % job,
  ),
  duplicateCheckMode = cms.untracked.string("checkEachRealDataFile"),
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.TFileService = cms.Service(
  "TFileService",
  fileName = cms.string("zgSlim_%s.root" % job)
)

process.p = cms.Path( process.zgSlimSequence )

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string(
        '/cms/veverka/Sherpa/Slims/sherpa_%s_10k_slim.root' % job
        #'sherpa_slim_test.root'
        ),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep *_prunedGenParticles_*_*'
        )
    )

process.outpath = cms.EndPath(process.out)
