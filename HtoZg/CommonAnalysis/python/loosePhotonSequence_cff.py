import FWCore.ParameterSet.Config as cms

from HtoZg.CommonAnalysis.loosePhotons_cfi import loosePhotons
from HtoZg.CommonAnalysis.photonTree_cfi import photonTree

photonsBeforeId  = photonTree.clone(
    src = cms.InputTag('selectedPatPhotons')
    )

hasLoosePhoton = cms.EDProducer('EventCountProducer')

loosePhotonSequence = cms.Sequence(photonsBeforeId +
                                   loosePhotons + 
                                   hasLoosePhoton)
