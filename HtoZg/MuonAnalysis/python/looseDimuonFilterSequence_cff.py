import FWCore.ParameterSet.Config as cms

from HtoZg.MuonAnalysis.looseMuons_cfi import looseMuons
from HtoZg.MuonAnalysis.looseDimuons_cfi import looseDimuons
from HtoZg.MuonAnalysis.looseDimuonFilter_cfi import looseDimuonFilter

hasLooseDimuon = cms.EDProducer('EventCountProducer')

looseDimuonFilterSequence = cms.Sequence(looseMuons +
                                         looseDimuons +
                                         looseDimuonFilter +
                                         hasLooseDimuon)
