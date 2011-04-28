import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

# setup 'analysis'  options
options = VarParsing.VarParsing ('analysis')

## default options
options.inputFiles = ["file:fastsim.root"]

options.outputFile = "famosTree.root"

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

process.tree = cms.EDAnalyzer("FastSimTreeMaker",
    name = cms.untracked.string("tree"),
    title = cms.untracked.string("famos analysis tree"),
    src = cms.InputTag("reducedEcalRecHitsEB"),
    sizeName = cms.untracked.string("nRecHits"),
    prefix = cms.untracked.string("rh"),
    variables = cms.VPSet(),
    simTrackBranches = cms.PSet(
        src = cms.InputTag("famosSimHits",""),
        sizeName = cms.untracked.string("nSimTracks"),
        prefix = cms.untracked.string("simTrack"),
        variables = cms.VPSet(
            cms.PSet( tag = cms.untracked.string("Charge"),
                      quantity = cms.untracked.string("charge") ),
            cms.PSet( tag = cms.untracked.string("PID"),
                      quantity = cms.untracked.string("type") ),
            cms.PSet( tag = cms.untracked.string("Pt"),
                      quantity = cms.untracked.string("momentum.pt") ),
            cms.PSet( tag = cms.untracked.string("Eta"),
                      quantity = cms.untracked.string("momentum.eta") ),
            cms.PSet( tag = cms.untracked.string("Phi"),
                      quantity = cms.untracked.string("momentum.phi") ),
        )
    )
)

for t, q in [ tuple( tq.split() ) for tq in
                  """Energy  energy
                     Time    time
                     RawId   id.rawId  """.split("\n") ]:
    process.tree.variables.append(
        cms.PSet( tag = cms.untracked.string(t),
                  quantity = cms.untracked.string(q) )
    )

process.p = cms.Path(process.tree)

if __name__ == "__main__": import user

