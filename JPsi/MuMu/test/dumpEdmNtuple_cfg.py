import FWCore.ParameterSet.Config as cms

process = cms.Process("NTUPLEDUMP")

## Message logger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

#process.maxEvents = cms.untracked.PSet(output = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(50000) )

import JPsi.MuMu.Mu_Run2010A_PromptReco_v4_DimuonPhotonSkim_v1_json137437_139375_cff as promptReco_v4
pathPrefix = "rfio:" + promptReco_v4.crabOutputPath + "/"

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(pathPrefix + "Mu_Run2010A-CS_Onia-Jun14thSkim_v1_DimuonSkimPAT.root")
)
process.source.fileNames = [pathPrefix + file for file in promptReco_v4.crabOutputFileList]

process.load("JPsi.MuMu.glbMuons_cfi")
process.load("JPsi.MuMu.trkMuons_cfi")
process.load("JPsi.MuMu.dimuons_cfi")
process.load("JPsi.MuMu.dimuonsCountFilters_cfi")
process.load("JPsi.MuMu.jpsiEdmNtuples_cfi")

process.ggosPath = cms.Path(
  process.glbMuons *
  process.dimuonsGGOS *
  process.ggosJPsiEdmNtuple *
  process.dimuonsGGOSCountFilter
)

process.ggssPath = cms.Path(
  process.glbMuons *
  process.dimuonsGGSS *
  process.ggssJPsiEdmNtuple *
  process.dimuonsGGSSCountFilter
)

process.gtosPath = cms.Path(
  process.glbMuons *
  process.trkMuons *
  process.dimuonsGTOS *
  process.gtosJPsiEdmNtuple *
  process.dimuonsGTOSCountFilter
)

process.gtssPath = cms.Path(
  process.glbMuons *
  process.trkMuons *
  process.dimuonsGTSS *
  process.gtssJPsiEdmNtuple *
  process.dimuonsGTSSCountFilter
)

process.ttosPath = cms.Path(
  process.trkMuons *
  process.dimuonsTTOS *
  process.ttosJPsiEdmNtuple *
  process.dimuonsTTOSCountFilter
)

process.ttssPath = cms.Path(
  process.trkMuons *
  process.dimuonsTTSS *
  process.ttssJPsiEdmNtuple *
  process.dimuonsTTSSCountFilter
)

process.out = cms.OutputModule("PoolOutputModule",
  outputCommands = cms.untracked.vstring('drop *',
    "keep *_ggosJPsiEdmNtuple_*_*",
    "keep *_ggssJPsiEdmNtuple_*_*",
    "keep *_gtosJPsiEdmNtuple_*_*",
    "keep *_gtssJPsiEdmNtuple_*_*",
    "keep *_ttosJPsiEdmNtuple_*_*",
    "keep *_ttssJPsiEdmNtuple_*_*",
  ),
  SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring(
      '*Path',
    )
  ),
  fileName = cms.untracked.string("ntuplePromptReco_50k.root")
#   fileName = cms.untracked.string("minimumBiasNtuples.root")
)

process.outPath= cms.EndPath(process.out)
