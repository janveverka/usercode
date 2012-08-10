import FWCore.ParameterSet.Config as cms

from HtoZg.MuonAnalysis.filterSequence_cff import *
from HtoZg.MuonAnalysis.patSequence_cff import *
from HtoZg.MuonAnalysis.tightDimuonSequence_cff import *
from HtoZg.MuonAnalysis.isolatedDimuonSequence_cff import *

allInputEvents   = cms.EDProducer('EventCountProducer')

muonsAfterVtx = muonTree.clone()

skimSequence = cms.Sequence(allInputEvents + 
                            filterSequence +
                            patSequence +
                            muonsAfterVtx +
                            tightDimuonSequence +
                            isolatedDimuonSequence)

if __name__ == '__main__':
    import user

