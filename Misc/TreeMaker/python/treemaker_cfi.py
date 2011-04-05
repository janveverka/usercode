import FWCore.ParameterSet.Config as cms

tree = cms.EDAnalyzer("TreeMaker",
  name = cms.untracked.string("tree"),
  title = cms.untracked.string("testing TreeMaker"),
  src = cms.InputTag("cleanPatPhotonsTriggerMatch"),
  prefix = cms.untracked.string("cand"),
  sizeName = cms.untracked.string("ncands"),
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
