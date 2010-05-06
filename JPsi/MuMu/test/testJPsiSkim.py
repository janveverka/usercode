import FWCore.ParameterSet.Config as cms

process = cms.Process("ANALYSIS")

## Message logger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
    'file:testZMuMuGammaSubskim.root'
  )
)

# pathPrefix = "rfio:/castor/cern.ch/user/g/gpetrucc/7TeV/DATA/"
pathPrefix = "file:/tmp/veverka/"
fileNames = """
DATA_skimJPsiLoose_fromApr20MuonSkim-v2.root
DATA_skimJPsiLoose_fromMuonSkimV9_upToApr28-v2.root
""".split()
process.source.fileNames = [pathPrefix + fileName for fileName in fileNames]

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.TFileService = cms.Service("TFileService",
  fileName = cms.string("histo_jpsi_full.root")
)

process.load("JPsi.MuMu.testJPsiSkim_cfi")

process.p = cms.Path(process.jpsiSequence)
