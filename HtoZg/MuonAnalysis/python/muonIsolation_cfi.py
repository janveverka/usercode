import FWCore.ParameterSet.Config as cms

muonIsolation = cms.EDProducer('RecoMuonIsolationValueMapProducer',
    muonSource = cms.InputTag('muons'),
    ## FIXME: Make sure this is correct.
    rhoSource  = cms.InputTag('kt6PFJets', 'rho'),
    )
