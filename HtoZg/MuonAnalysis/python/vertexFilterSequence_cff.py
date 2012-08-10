import FWCore.ParameterSet.Config as cms
from HtoZg.CommonAnalysis.vertexFilterSequence_cff import *

passVertexFilter = cms.EDProducer('EventCountProducer')
vertexFilterSequence = cms.Sequence(vertexFilter + passVertexFilter)