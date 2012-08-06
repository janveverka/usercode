import FWCore.ParameterSet.Config as cms

goodVertices = cms.EDFilter('VertexSelector',
    src = cms.InputTag('offlinePrimaryVertices'),
    cut = cms.string('''
        !isFake &&
        ndof > 4 &&
        abs(z) <= 24 &&
        position.Rho <= 2
        '''),
    filter = cms.bool(False),
    )

