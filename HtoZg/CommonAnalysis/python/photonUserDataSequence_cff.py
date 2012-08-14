import FWCore.ParameterSet.Config as cms

from HtoZg.CommonAnalysis.conversionTools_cfi import conversionTools
from HtoZg.CommonAnalysis.photonIdSequence_cff import *
from HtoZg.CommonAnalysis.photonIsolationSequence_cff import *

photonUserDataSequence = cms.Sequence(
    conversionTools + 
    photonIdSequence +
    photonIsolationSequence
    )

