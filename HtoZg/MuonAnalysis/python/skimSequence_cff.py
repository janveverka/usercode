import FWCore.ParameterSet.Config as cms
from HtoZg.MuonAnalysis.hltFilter_cfi import hltFilter
from HtoZg.CommonAnalysis.vertexFilterSequence_cff import *

allInputEvents   = cms.EDProducer('EventCountProducer')
passHltFilter    = cms.EDProducer('EventCountProducer')

skimSequence = cms.Sequence(allInputEvents + 
                            hltFilter + passHltFilter +
                            vertexFilterSequence)
                            