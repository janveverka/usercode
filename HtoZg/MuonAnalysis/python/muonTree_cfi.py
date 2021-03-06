'''
Defines default configuration for a module that creates a flat ROOT tree
of muon variables used in the H->Zg analysis.

Jan Veverka, Caltech, 6 Aug 2012 - 8 Aug 2012
'''
import FWCore.ParameterSet.Config as cms

from Misc.TreeMaker.kinematicVariables_cff import kinematicVariables
from HtoZg.MuonAnalysis.muonIdVariables_cff import muonIdVariables
from HtoZg.MuonAnalysis.muonIsolationVariables_cff import muonIsolationVariables

muonTree = cms.EDAnalyzer('CandViewTreeMaker',
  name      = cms.untracked.string('muons'),
  title     = cms.untracked.string('Muon variables for the H->Zg analysis'),
  src       = cms.InputTag('selectedPatMuons'),
  prefix    = cms.untracked.string(''),
  sizeName  = cms.untracked.string('n'),
  variables = cms.VPSet(),
)

muonTree.variables.extend(kinematicVariables)
muonTree.variables.extend(muonIdVariables)
muonTree.variables.extend(muonIsolationVariables)
