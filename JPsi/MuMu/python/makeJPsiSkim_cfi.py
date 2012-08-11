import FWCore.ParameterSet.Config as cms

process = cms.Process("JPSISKIM")

## Message logger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

pathPrefix = "file:/uscms/home/veverka/work/jpsi/CMSSW_3_7_0_patch3/src/JPsi/MuMu/test/crab/crab_0_100701_095456/res/"
process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(pathPrefix + "DimuonSkim_merge156.root")
)

process.load("JPsi.MuMu.glbMuons_cfi")
process.load("JPsi.MuMu.trkMuons_cfi")
process.load("JPsi.MuMu.dimuons_cfi")
process.load("JPsi.MuMu.jpsiCands_cfi")

process.jpsiGGOSPath = cms.Path(process.glbMuons * process.dimuonsGGOS * process.jpsisGGOS)
process.jpsiGGSSPath = cms.Path(process.glbMuons * process.dimuonsGGSS * process.jpsisGGSS)

process.jpsiGTOSPath = cms.Path( (process.glbMuons + process.trkMuons) * process.dimuonsGTOS * process.jpsisGTOS)
process.jpsiGTSSPath = cms.Path( (process.glbMuons + process.trkMuons) * process.dimuonsGTSS * process.jpsisGTSS)

process.jpsiTTOSPath = cms.Path(process.trkMuons * process.dimuonsTTOS * process.jpsisTTOS)
process.jpsiTTSSPath = cms.Path(process.trkMuons * process.dimuonsTTSS * process.jpsisTTSS)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.TFileService = cms.Service("TFileService",
  fileName = cms.string("jpsiSkim_%devts.root" % process.maxEvents.input.value() ),
  selectEvents = cms.PSet(
    selectEvents = cms.string("jpsiGGOSPath")
  )
)

process.out = cms.OutputModule("PoolOutputModule",
  outputCommands = cms.untracked.vstring('keep *'),
  SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring(
      'jpsiGGOSPath',
      'jpsiGGSSPath',
      'jpsiGTOSPath',
      'jpsiGTSSPath',
      'jpsiTTOSPath',
      'jpsiTTSSPath',
    )
  ),
  fileName = cms.untracked.string("jpsiSkim.root")
)

process.outPath= cms.EndPath(process.out)
