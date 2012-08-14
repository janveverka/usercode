import FWCore.ParameterSet.Config as cms

photonIsolation = cms.EDProducer('RecoPhotonIsolationValueMapProducer',
    photonSource = cms.InputTag('photons'),
    rhoSource    = cms.InputTag('kt6PFJetsPho', 'rho'),
    vertexSource = cms.InputTag('offlinePrimaryVertices'),
    pfSource     = cms.InputTag('particleFlow', '')
    )
