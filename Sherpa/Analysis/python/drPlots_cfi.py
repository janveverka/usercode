import FWCore.ParameterSet.Config as cms

# needs genParticles (!)
drPlots = cms.EDAnalyzer("GenParticleAnalyzer",
  genSrc = cms.untracked.InputTag("genParticles")
)
