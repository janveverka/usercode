import FWCore.ParameterSet.Config as cms

process = cms.Process("electronSkim")

## Message logger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Define the source
process.source = cms.Source("PoolSource",
     fileNames = cms.untracked.vstring(
      '/store/data/Run2010A/EG/RECO/Jun14thReReco_v1/0001/FE96AFA9-C678-DF11-9E4C-003048F0E7FC.root'
    )
)

process.maxEvents = cms.untracked.PSet( output = cms.untracked.int32(-1) )

## Define the TFileService
process.TFileService = cms.Service("TFileService",
  fileName = cms.string("histograms.root")
)

## Define the output module
process.out = cms.OutputModule("PoolOutputModule",
  fileName = cms.untracked.string("electronSkim.root"),
  ## save only events passing the filter(s) in the filterSequnce
  SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring("p")
  ),
  outputCommands = cms.untracked.vstring("keep *")
)

## Add the output to the ouput path
process.outPath = cms.EndPath(process.out)

## Tab complete during inspection
if __name__ == "__main__": import user

