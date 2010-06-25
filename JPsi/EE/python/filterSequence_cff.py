import FWCore.ParameterSet.Config as cms

from JPsi.EE.electronCountFilter_cfi import *

filterSequence = cms.Sequence(electronCountFilter)