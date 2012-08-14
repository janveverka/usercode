import FWCore.ParameterSet.Config as cms

from HtoZg.CommonAnalysis.photonId_cfi import photonId

CaloTowerConstituentsMapBuilder = cms.ESProducer(
    "CaloTowerConstituentsMapBuilder",
    MapFile = cms.untracked.string(
        'Geometry/CaloTopology/data/CaloTowerEEGeometric.map.gz'
        )
    )

photonIdSequence = cms.Sequence(
    photonId
    )
