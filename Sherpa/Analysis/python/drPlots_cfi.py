import FWCore.ParameterSet.Config as cms

# needs genParticles (!)
drPlotsL = cms.EDAnalyzer("GenParticleAnalyzer",
  genSrc = cms.untracked.InputTag("genParticles")
)

drPlotsQ = cms.EDAnalyzer("DeltaRPhotonQuark",
  genSrc = cms.untracked.InputTag("genParticles")
)

drPlots = cms.Sequence(drPlotsL + drPlotsQ)