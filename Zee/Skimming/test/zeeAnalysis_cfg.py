import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

## setup 'analysis'  options
options = VarParsing.VarParsing ('analysis')

## setup any defaults you want
options.inputFiles = ["file:VGammaPAT_DielectronSkim_Winter10_numEvent1000.root"]
options.maxEvents = -1 # -1 means all events
options.outputFile = "testHistos.root"
## get and parse the command line arguments
options.parseArguments()


## define the process
process = cms.Process("Test")

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring() + options.inputFiles
)

process.maxEvents = cms.untracked.PSet(
  input = cms.untracked.int32(options.maxEvents)
)

## Detector Conditions (needed for a EcalChannelStatusRcd)
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.PyReleaseValidation.autoCond import autoCond
process.GlobalTag.globaltag = cms.string( autoCond[ 'startup' ] )


## Message logger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.load("Zee.Skimming.ZeeSequence_cff")
process.load("Zee.Skimming.testAnalyzer_cfi")
process.goldenZee = process.testAnalyzer.clone( src = cms.InputTag("goldenDielectrons") )
process.p = cms.Path(
    process.ZeeSequence * (process.testAnalyzer + process.goldenZee)
    )

process.TFileService = cms.Service("TFileService",
  fileName = cms.string(options.outputFile)
)

process.options.wantSummary = True

## Enable LogDebug for analyzeMmgFsr module
# process.MessageLogger.debugModules = ["analyzeMmgFsr"]
# process.MessageLogger.cerr.threshold = "DEBUG"

if __name__ == "__main__": import user

