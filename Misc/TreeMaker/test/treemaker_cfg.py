import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

# setup 'analysis'  options
options = VarParsing.VarParsing ('analysis')

## default options
options.inputFiles = [
    "file:/mnt/hadoop/user/veverka/DimuonVGammaSkim_v3/Mu/Run2010A-Nov4ReReco_v1-DimuonVGammaSkim_v3/f81f6ec801d687f509099b4fa4a3c90c/"
    + f for f in """
        merge_10_1_xJE.root  merge_13_1_ndW.root  merge_1_1_f6L.root
        merge_11_1_BKq.root  merge_14_1_wuM.root  merge_2_1_1Me.root
        merge_12_1_8F1.root  merge_15_1_PDX.root  merge_3_1_RXC.root
        merge_4_1_unc.root  merge_7_1_s8z.root
        merge_5_1_aPx.root  merge_8_1_gdx.root
        merge_6_1_ran.root  merge_9_1_RlG.root
        """.split()
]

options.outputFile = "tree.root"

## get and parse the command line arguments
options.parseArguments()

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")
## Enable LogDebug for MuMuGammaTree module
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.MessageLogger.debugModules = ["tree"]
process.MessageLogger.cerr.threshold = "DEBUG"

process.maxEvents = cms.untracked.PSet(
  input = cms.untracked.int32(options.maxEvents)
)

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring() + options.inputFiles
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string(options.outputFile)
)

process.tree = cms.EDAnalyzer('TreeMaker',
  name = cms.untracked.string("tree2"),
  title = cms.untracked.string("testing TreeMaker"),
  src = cms.InputTag("cleanPatPhotonsTriggerMatch"),
  prefix = cms.untracked.string("cand"),
  sizeName = cms.untracked.string("nPhotons"),
  variables = cms.VPSet(
    cms.PSet(
      tag = cms.untracked.string("Pt"),
      quantity = cms.untracked.string("pt")
    ),
    cms.PSet(
      tag = cms.untracked.string("Eta"),
      quantity = cms.untracked.string("eta")
    ),
    cms.PSet(
      tag = cms.untracked.string("Phi"),
      quantity = cms.untracked.string("phi")
    ),
  )
)

process.testTree = cms.EDAnalyzer('TestTreeMaker',
  candSrc = cms.untracked.InputTag("cleanPatPhotonsTriggerMatch")
)

process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring('ProductNotFound')
)

process.p = cms.Path(process.tree + process.testTree)


if __name__ == "__main__": import user
