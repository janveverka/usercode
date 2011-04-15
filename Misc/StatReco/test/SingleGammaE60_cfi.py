import FWCore.ParameterSet.Config as cms

generator = cms.EDProducer("FlatRandomEGunProducer",
    PGunParameters = cms.PSet(
        PartID = cms.vint32(22),
        # ieta, iphi = -3, 3 
        MaxEta = cms.double(-4.88368e-2),
        MaxPhi = cms.double(-1.29658e-1),
        MinEta = cms.double(-4.88369e-2),
        MinE = cms.double(59.999),
        MinPhi = cms.double(-1.29659e-1), ## in radians

        MaxE = cms.double(60.001)
    ),
    Verbosity = cms.untracked.int32(0), ## set to 1 (or greater)  for printouts

    psethack = cms.string('single gamma E 60'),
    AddAntiParticle = cms.bool(True),
    firstRun = cms.untracked.uint32(1)
)
