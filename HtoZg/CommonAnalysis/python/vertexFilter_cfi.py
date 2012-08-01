import FWCore.ParameterSet.Config as cms

## Require at least one good reconstructed vertex.
## https://twiki.cern.ch/twiki/bin/view/CMS/Collisions2010Recipes#Good_Vertex_selection
## https://hypernews.cern.ch/HyperNews/CMS/get/gaugeCoupling/349/1.html
vertexFilter = cms.EDFilter("GoodVertexFilter",
  vertexCollection = cms.InputTag('offlinePrimaryVertices'),
  minimumNDOF = cms.uint32(4),
  maxAbsZ = cms.double(24),
  maxd0 = cms.double(2)
)
