import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

# setup 'analysis'  options
options = VarParsing.VarParsing ('analysis')

## default options
options.inputFiles = ["file:fastsim.root"]

options.outputFile = "ecalRecHitsTree.root"

## get and parse the command line arguments
options.parseArguments()

process = cms.Process("TREE")

process.load("FWCore.MessageService.MessageLogger_cfi")
## Enable LogDebug for MuMuGammaTree module
process.MessageLogger.cerr.FwkReport.reportEvery = 1
#process.MessageLogger.debugModules = ["tree"]
#process.MessageLogger.cerr.threshold = "DEBUG"

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

process.tree = cms.EDAnalyzer("EcalRecHitTreeMaker",
    name = cms.untracked.string("tree"),
    title = cms.untracked.string("ECAL rec hits tree"),
    src = cms.InputTag("ecalRecHit", "EcalRecHitsEB"),
    #prefix = cms.untracked.string("cand"),
    sizeName = cms.untracked.string("nRecHits"),
    variables = cms.VPSet()
)

for t, q in [ tuple( tq.split() ) for tq in 
                  """energy  energy
                     time    time
                     rawId   id.rawId  """.split("\n") ]:
    process.tree.variables.append(
        cms.PSet( tag = cms.untracked.string(t),
                  quantity = cms.untracked.string(q) )
    )

process.p = cms.Path(process.tree)

if __name__ == "__main__": import user

