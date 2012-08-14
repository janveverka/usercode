import FWCore.ParameterSet.Config as cms

photonId = cms.EDProducer('PhotonIdValueMapProducer',
    src = cms.InputTag('photons'),
    )
