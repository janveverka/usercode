import FWCore.ParameterSet.Config as cms

process = cms.Process("HISTO")

#from Sherpa.Analysis.srcFileNames_cfi import castorFilesFilterJet10 as srcFileNames
from Sherpa.Analysis.srcFileNames_cfi import castorFilesFilter as srcFileNames
process.source = cms.Source("PoolSource",
#    skipEvents = cms.untracked.uint32(5),
  #fileNames = cms.untracked.vstring(srcFileNames["WgEle_0j2"]),
  #fileNames = cms.untracked.vstring(srcFileNames["WgMu_0j2"]),
  #fileNames = cms.untracked.vstring(srcFileNames["WgTau_0j2"]),
  #fileNames = cms.untracked.vstring(srcFileNames["WgLep_0j2"]),
  #fileNames = cms.untracked.vstring(srcFileNames["WgEle_0j3"]),
  #fileNames = cms.untracked.vstring(srcFileNames["WgMu_0j3"]),
  #fileNames = cms.untracked.vstring(srcFileNames["WgTau_0j3"]),
  #fileNames = cms.untracked.vstring("file:WgEle_0j2_300evts.root"),
  #fileNames = cms.untracked.vstring("file:sherpa_out.root"),
  #fileNames = cms.untracked.vstring(srcFileNames["WgEle_0j"][0:2]),
  #fileNames = cms.untracked.vstring(srcFileNames["WgEle_0j"][2:4]),
  #fileNames = cms.untracked.vstring(srcFileNames["WgEle_0j"][4:6]),
  #fileNames = cms.untracked.vstring(srcFileNames["WgEle_0j"][6:8]),
  #fileNames = cms.untracked.vstring(srcFileNames["WgEle_0j"][9]),
  fileNames = cms.untracked.vstring(
#     "rfio:/castor/cern.ch/user/v/veverka/mc/Spring10/Sherpa/WgEle_0j2/GEN/sherpack_lib3/outputGEN_5.root",
#     "rfio:/castor/cern.ch/user/v/veverka/mc/Spring10/Sherpa/WgMu_0j2/GEN/sherpack_lib3/outputGEN_5.root",
    "rfio:/castor/cern.ch/user/v/veverka/mc/Spring10/Sherpa/WgTau_0j2/GEN/sherpack_lib3/outputGEN_5.root",
#     "rfio:/castor/cern.ch/user/v/veverka/mc/Spring10/Sherpa/WgEle_0j2/RECO/sherpack_lib3/reco_1.root",
  ),
  duplicateCheckMode = cms.untracked.string("checkEachRealDataFile"),
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.TFileService = cms.Service(
  "TFileService",
#   fileName = cms.string("histos_WgEle_0j2_filter.root")
#   fileName = cms.string("histos_WgMu_0j2_filter.root")
  fileName = cms.string("histos_WgTau_0j2_filter.root")
#   fileName = cms.string("histos_WgEle_0j2_RECO_2.root")
  #fileName = cms.string("histos_WgEle_0j2_Jet10.root")
  #fileName = cms.string("histos_WgMu_0j2_Jet10.root")
  #fileName = cms.string("histos_WgTau_0j2_Jet10.root")
  #fileName = cms.string("histos_WgLep_0j2_Jet10.root")
  #fileName = cms.string("histos_WgEle_0j3.root")
  #fileName = cms.string("histos_WgMu_0j3.root")
  #fileName = cms.string("histos_WgTau_0j3.root")
  #fileName = cms.string("histos_WgEle_0j_filter_part1-2.root")
  #fileName = cms.string("histos_WgEle_0j_filter_part3-4.root")
  #fileName = cms.string("histos_WgEle_0j_filter_part5-6.root")
  #fileName = cms.string("histos_WgEle_0j_filter_part7-8.root")
  #fileName = cms.string("histos_WgEle_0j_filter_part10.root")
)

process.load("Sherpa.Analysis.genFilter_cfi")
process.load("Sherpa.Analysis.genParticles_cfi")
process.load("Sherpa.Analysis.wgHistos_cfi")

process.p = cms.Path(
  process.genFilter *
  process.genParticles *
  process.wgHistos
)
