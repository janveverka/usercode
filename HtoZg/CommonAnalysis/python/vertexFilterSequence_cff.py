import FWCore.ParameterSet.Config as cms
from HtoZg.CommonAnalysis.vertexFilter_cfi import *

passVertexFilter = cms.EDProducer('EventCountProducer')
vertexFilterSequence = cms.Sequence(vertexFilter + passVertexFilter)