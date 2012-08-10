import FWCore.ParameterSet.Config as cms

muonIsolation = cms.EDProducer('RecoMuonIsolationValueMapProducer',
    muonSource = cms.InputTag('muons'),
    rhoSource  = cms.InputTag('kt6PFJetsCentralNeutral', 'rho', 'RECO'),
    )
