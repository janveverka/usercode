import FWCore.ParameterSet.Config as cms

from HtoZg.MuonAnalysis.looseDimuons_cfi import looseDimuons
from HtoZg.MuonAnalysis.looseDimuonFilter_cfi import looseDimuonFilter

selectedDimuons = looseDimuons.clone(
    src   = cms.InputTag('selectedPatMuons'),
    decay = cms.string('selectedPatMuons@+ selectedPatMuons@-')
    )

selectedDimuonFilter = looseDimuonFilter.clone(
    src = cms.InputTag('selectedDimuons')
    )

hasSelectedDimuon = cms.EDProducer('EventCountProducer')

selectedDimuonSequence = cms.Sequence(selectedDimuons +
                                      selectedDimuonFilter +
                                      hasSelectedDimuon)
