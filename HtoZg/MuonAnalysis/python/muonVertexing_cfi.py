import FWCore.ParameterSet.Config as cms

muonVertexing = cms.EDProducer('RecoMuonVertexingValueMapProducer',
    muonSource = cms.InputTag('muons'),
    vertexSource = cms.InputTag('goodVertices'),
    )
