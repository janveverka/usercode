import FWCore.ParameterSet.Config as cms

from HtoZg.MuonAnalysis.selectedMuons_cfi import selectedMuons
from HtoZg.MuonAnalysis.looseDimuons_cfi import looseDimuons
from HtoZg.MuonAnalysis.looseDimuonFilter_cfi import looseDimuonFilter


selectedDimuons = looseDimuons.clone(
    src   = cms.InputTag('selectedMuons'),
    decay = cms.string('selectedMuons@+ selectedMuons@-')
    )

selectedDimuonFilter = looseDimuonFilter.clone(
    src = cms.InputTag('selectedDimuons')
    )

hasSelectedDimuon = cms.EDProducer('EventCountProducer')

selectedDimuonSequence = cms.Sequence(selectedMuons + 
                                      selectedDimuons +
                                      selectedDimuonFilter +
                                      hasSelectedDimuon)
