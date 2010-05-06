import FWCore.ParameterSet.Config as cms

process = cms.Process("JPsiMuMuGammaGenAnalysis")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        ## J/Psi @ 7 TeV, two muons both with |eta|<2.5, pt > 1, p > 3
	'/store/relval/CMSSW_3_5_7/RelValJpsiMM/GEN-SIM-RECO/START3X_V26-v1/0012/DA27C180-4649-DF11-B276-0030486791F2.root',
    )
)

logicalPath = "/store/relval/CMSSW_3_5_7/RelValJpsiMM/GEN-SIM-RECO/START3X_V26-v1/0012/"

fileList = ["048A8D5B-4549-DF11-8DE7-00304867C1BC.root",
  "3875CEE1-4549-DF11-B5C4-003048678B7E.root",
  "3E5CAA71-4749-DF11-8696-003048679296.root",
  "8AF7970C-6949-DF11-A46B-003048D15D22.root",
  "8EF0F0CB-4449-DF11-9895-003048678FC4.root",
  "DA27C180-4649-DF11-B276-0030486791F2.root",
]

process.source.fileNames = [logicalPath + aFile for aFile in fileList]

### number of events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.TFileService = cms.Service("TFileService",
  fileName = cms.string("genPlots_all.root")
)

process.load("HeavyFlavorAnalysis.Onia2MuMu.genAnalysis_cfi")

process.p = cms.Path(process.makeGenJPsiHistos)

if __name__ == "__main__":
  import user

