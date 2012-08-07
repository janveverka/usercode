import FWCore.ParameterSet.Config as cms

from HtoZg.MuonAnalysis.filterSequence_cff import *
from HtoZg.MuonAnalysis.patSequence_cff import *
from HtoZg.MuonAnalysis.tightDimuonSequence_cff import *

allInputEvents   = cms.EDProducer('EventCountProducer')

skimSequence = cms.Sequence(allInputEvents + 
                            filterSequence +
                            patSequence +
                            tightDimuonSequence)

if __name__ == '__main__':
    import user

