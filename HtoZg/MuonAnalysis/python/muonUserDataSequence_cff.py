import FWCore.ParameterSet.Config as cms

from HtoZg.CommonAnalysis.goodVertices_cfi import * 
from HtoZg.MuonAnalysis.muonVertexing_cfi import *

muonUserDataSequence = cms.Sequence(goodVertices + muonVertexing)

