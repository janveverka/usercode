import FWCore.ParameterSet.Config as cms

process = cms.Process("DimuonNtuple")

## Message logger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

## Geometry, Detector Conditions and Pythia Decay Tables (needed for the vertexing)
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = "GR_R_36X_V12A::All"
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")


# process.maxEvents = cms.untracked.PSet(output = cms.untracked.int32(100) )
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1) )

pathPrefix = "rfio:/castor/cern.ch/user/v/veverka/data/DimuonPhotonSkim_v2/Mu_Run2010A-PromptReco-v4_140160-140399/"
fileNames = """
DimuonPhotonSkim_v2_10_1_EwL.root
DimuonPhotonSkim_v2_11_1_T4y.root
DimuonPhotonSkim_v2_12_1_n2w.root
DimuonPhotonSkim_v2_13_1_hNi.root
DimuonPhotonSkim_v2_14_1_av9.root
DimuonPhotonSkim_v2_15_1_Ktq.root
DimuonPhotonSkim_v2_16_1_J5b.root
DimuonPhotonSkim_v2_17_1_7TS.root
DimuonPhotonSkim_v2_18_1_U6e.root
DimuonPhotonSkim_v2_19_1_BNX.root
DimuonPhotonSkim_v2_1_1_DRE.root
DimuonPhotonSkim_v2_20_1_I5f.root
DimuonPhotonSkim_v2_21_1_hxR.root
DimuonPhotonSkim_v2_2_1_A34.root
DimuonPhotonSkim_v2_3_1_etM.root
DimuonPhotonSkim_v2_4_1_ODX.root
DimuonPhotonSkim_v2_5_1_7dq.root
DimuonPhotonSkim_v2_6_1_o3l.root
DimuonPhotonSkim_v2_7_1_YYD.root
DimuonPhotonSkim_v2_8_1_7jn.root
DimuonPhotonSkim_v2_9_1_CUX.root
""".split()

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
    *[pathPrefix + f for f in fileNames]
  )
)

process.TFileService = cms.Service("TFileService",
  fileName = cms.string('dimuonsNtuple_Mu_Run2010A-PromptReco-v4_140160-140399.root')
)

process.load("JPsi.MuMu.goodMuons_cfi")
process.load("JPsi.MuMu.glbMuons_cfi")
process.load("JPsi.MuMu.trkMuons_cfi")
process.load("JPsi.MuMu.dimuons_cfi")
process.load("JPsi.MuMu.dimuonsCountFilters_cfi")

process.goodDimuonsCountFilter = process.dimuonsCountFilter.clone(src = "goodDimuons")

process.dimuonsNtuple = cms.EDAnalyzer("DimuonsNtupelizer",
  photonSrc   = cms.untracked.InputTag("selectedPatPhotons"),
  muonSrc     = cms.untracked.InputTag("selectedPatMuons"),
  dimuonSrc   = cms.untracked.InputTag("vertexedDimuons"),
  beamSpotSrc = cms.untracked.InputTag("offlineBeamSpot"),
  primaryVertexSrc = cms.untracked.InputTag("offlinePrimaryVertices"),
)


process.p = cms.Path(
  process.goodMuons *
  process.goodDimuons *
  process.goodDimuonsCountFilter *
  process.vertexedDimuons *
  process.dimuonsNtuple
)

