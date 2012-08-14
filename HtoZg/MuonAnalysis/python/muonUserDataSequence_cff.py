import FWCore.ParameterSet.Config as cms

from HtoZg.CommonAnalysis.goodVertices_cfi import goodVertices
from HtoZg.MuonAnalysis.muonVertexing_cfi import muonVertexing
from HtoZg.MuonAnalysis.muonIsolation_cfi import muonIsolation

muonUserDataSequence = cms.Sequence(
    goodVertices + 
    muonVertexing #+
    #muonIsolation
    )

