import FWCore.ParameterSet.Config as cms
from HtoZg.CommonAnalysis.vertexFilterSequence_cff import *
from HtoZg.MuonAnalysis.hltFilter_cfi import hltFilter
from HtoZg.MuonAnalysis.looseDimuonSequence_cff import *
from HtoZg.MuonAnalysis.patSequence_cff import *

allInputEvents   = cms.EDProducer('EventCountProducer')
passHltFilter    = cms.EDProducer('EventCountProducer')


selectedDimuons = looseDimuons.clone(
    src = cms.InputTag('selectedPatMuons')
    )

selectedDimuonFilter = looseDimuonFilter.clone(
    src = cms.InputTag('selectedDimuons')
    )

hasSelectedDimuon = cms.EDProducer('EventCountProducer')

selectedDimuonSequence = cms.Sequence(selectedDimuons +
                                      selectedDimuonFilter +
                                      hasSelectedDimuon)

skimSequence = cms.Sequence(allInputEvents + 
                            hltFilter + passHltFilter +
                            vertexFilterSequence +
                            looseDimuonSequence + 
                            patSequence +
                            selectedDimuonSequence)

# print repr(patMuons)
                            
if __name__ == '__main__':
    import user

