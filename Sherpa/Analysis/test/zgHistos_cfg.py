import FWCore.ParameterSet.Config as cms

process = cms.Process("HISTO")

from Sherpa.Analysis.srcFileNames_cfi import castorFilesFilterJet10 as srcFileNames
process.source = cms.Source("PoolSource",
  #fileNames = cms.untracked.vstring(srcFileNames["ZgEle_0j2"]),
  #fileNames = cms.untracked.vstring(srcFileNames["ZgEleMu_0j2"]),
  #fileNames = cms.untracked.vstring(srcFileNames["ZgMu_0j2"][2]),
  #fileNames = cms.untracked.vstring(srcFileNames["ZgNu_0j2"]),
  fileNames = cms.untracked.vstring(
#     "file:/afs/cern.ch/cms/cit/veverka/data/mc/Spring10/Sherpa/ZgMu_0j2/GEN/sherpack_lib3/outputGEN_3.root",
#     "rfio:/castor/cern.ch/user/v/veverka/mc/Spring10/Sherpa/ZgEle_0j2/GEN/sherpack_lib3/outputGEN_5.root",
#     "rfio:/castor/cern.ch/user/v/veverka/mc/Spring10/Sherpa/ZgMu_0j2/GEN/sherpack_lib3/outputGEN_5.root",
#     "rfio:/castor/cern.ch/user/v/veverka/mc/Spring10/Sherpa/ZgTau_0j2/GEN/sherpack_lib3/outputGEN_5.root",
    "rfio:/afs/cern.ch/cms/cit/veverka/vgamma/sherpa/CMSSW_3_5_8/src/Sherpa/ZgNu_0j/test/sherpa_out.root",

  ),
  duplicateCheckMode = cms.untracked.string("checkEachRealDataFile"),
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.TFileService = cms.Service(
  "TFileService",
#   fileName = cms.string("histos_ZgEle_0j2_filter.root")
#   fileName = cms.string("histos_ZgMu_0j2_filter.root")
#   fileName = cms.string("histos_ZgTau_0j2_filter.root")
  fileName = cms.string("zgHistos_test.root")
  #fileName = cms.string("histos_ZgEle_0j2.root")
  #fileName = cms.string("histos_ZgEleMu_0j2_Jet10.root")
  #fileName = cms.string("histos_ZgMu_0j2_Jet10.root")
)

process.load("Sherpa.Analysis.genFilter_cfi")
process.load("Sherpa.Analysis.genParticles_cfi")
process.load("Sherpa.Analysis.zgHistos_cfi")

process.p = cms.Path(
  process.genFilter *
  process.genParticles *
  process.zgHistos
)

#process.out = cms.OutputModule("PoolOutputModule",
                               #fileName = cms.untracked.string('sherpa_test.root'),
                               ## save only events passing the full path
                               #SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
                               ##outputCommands = cms.untracked.vstring(
                              ##'drop *',
                              ##'keep *_prompt*_*_*',
                              ##'keep *_me*_*_*',
                              ##'keep *_genParticles_*_*' )
                               #)

#process.outpath = cms.EndPath(process.out)
