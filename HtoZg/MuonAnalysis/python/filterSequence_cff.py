import FWCore.ParameterSet.Config as cms

from HtoZg.CommonAnalysis.vertexFilterSequence_cff import *
from HtoZg.MuonAnalysis.hltFilterSequence_cff import *

filterSequence = cms.Sequence(hltFilterSequence +
                              vertexFilterSequence)
