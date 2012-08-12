import FWCore.ParameterSet.Config as cms

from HtoZg.CommonAnalysis.photon_selection import htozg_id

loosePhotons = cms.EDFilter('PATPhotonSelector',
    src = cms.InputTag('selectedPatPhotons'),
    cut = cms.string('pt > 15 && ' + htozg_id),
    filter = cms.bool(True)                                
    )

