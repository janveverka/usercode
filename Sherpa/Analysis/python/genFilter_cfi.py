import FWCore.ParameterSet.Config as cms

genVeto = cms.EDFilter("MCParticlePairFilter",
  ParticleID1 = cms.untracked.vint32(11, 13, 15),
  ParticleID2 = cms.untracked.vint32(22, 22, 22),
  Status = cms.untracked.vint32(3, 3),
  MaxDeltaR = cms.untracked.double(0.3),
)

genFilter = cms.Sequence(~genVeto)