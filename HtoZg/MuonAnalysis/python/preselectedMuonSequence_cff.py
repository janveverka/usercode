import FWCore.ParameterSet.Config as cms
from HtoZg.MuonAnalysis.preselectedMuons import *

passMuonPreselections = cms.EDProducer('EventCountProducer')
preselectedMuonSequence = cms.Sequence(preselectedMuons *
                                       hasLooseDimuon)
