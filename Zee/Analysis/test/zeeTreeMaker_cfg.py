import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

## setup 'analysis'  options
options = VarParsing.VarParsing ('analysis')

## setup any defaults you want
options.inputFiles = ["file:/mnt/tier2/store/user/veverka/" +
    "DYToEE_M-20_TuneZ2_7TeV-pythia6/" +
    "Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1-" +
    "DielectronVGammaSkim_v4/26d056ff207141b564c225524777064e/" +
    "VGammaPAT_DielectronSkim_90_1_roP.root"]
options.outputFile = "zeeTree.root"

## get and parse the command line arguments
options.parseArguments()

process = cms.Process("TREE")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles)
)

process.TFileService = cms.Service("TFileService",
  fileName = cms.string(options.outputFile)
)

process.zeeAll = cms.EDAnalyzer("ZeeTreeMaker",
    eeSrc = cms.InputTag("dielectrons"),
    photonSrc = cms.InputTag("cleanPatPhotonsTriggerMatch"),
)

process.zeeGolden = cms.EDAnalyzer("ZeeTreeMaker",
    eeSrc = cms.InputTag("goldenDielectrons"),
    photonSrc = cms.InputTag("cleanPatPhotonsTriggerMatch"),
)

process.zeeShowering = cms.EDAnalyzer("ZeeTreeMaker",
    eeSrc = cms.InputTag("showeringDielectrons"),
    photonSrc = cms.InputTag("cleanPatPhotonsTriggerMatch"),
)

process.p = cms.Path(
    process.zeeAll *
    process.zeeGolden *
    process.zeeShowering
)
