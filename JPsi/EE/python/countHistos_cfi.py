import FWCore.ParameterSet.Config as cms

countHistos = cms.EDAnalyzer("CountHistoAnalyzer",
  nbins = cms.untracked.uint32(10),
  histograms = cms.untracked.VPSet(
    cms.PSet(src = cms.untracked.InputTag("gsfElectrons")),
    cms.PSet(src = cms.untracked.InputTag("particleFlow", "electrons")),
  )
)