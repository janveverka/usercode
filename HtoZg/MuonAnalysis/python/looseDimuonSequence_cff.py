import FWCore.ParameterSet.Config as cms
from HtoZg.MuonAnalysis.looseMuons_cfi import *
from HtoZg.MuonAnalysis.looseDimuons_cfi import *
from HtoZg.MuonAnalysis.looseDimuonFilter_cfi import *

hasLooseDimuon = cms.EDProducer('EventCountProducer')
looseDimuonSequence = cms.Sequence(looseMuons *
                                   looseDimuons *
                                   looseDimuonFilter *
                                   hasLooseDimuon)
