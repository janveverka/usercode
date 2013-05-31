import FWCore.ParameterSet.Config as cms

from Sherpa.Analysis.genParticles_cfi import *
from Sherpa.Analysis.prunedGenParticles_cfi import *
from Sherpa.Analysis.zgSlimHistoSequence_cff import *

zgSlimSequence = cms.Sequence(
    genParticles *
    prunedGenParticles *    
    zgSlimHistoSequence
    )
