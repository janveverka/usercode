'''
Defines default configuration for a module that creates a flat ROOT tree
of photon variables used in the H->Zg analysis.

Jan Veverka, Caltech, 11 Aug 2012
'''
import FWCore.ParameterSet.Config as cms

from Misc.TreeMaker.kinematicVariables_cff import kinematicVariables
from HtoZg.CommonAnalysis.photonIdVariables_cff import photonIdVariables
from HtoZg.CommonAnalysis.photonIsolationVariables_cff import photonIsolationVariables

photonTree = cms.EDAnalyzer('CandViewTreeMaker',
  name      = cms.untracked.string('photons'),
  title     = cms.untracked.string('Photon variables for the H->Zg analysis'),
  src       = cms.InputTag('selectedPatPhotons'),
  prefix    = cms.untracked.string(''),
  sizeName  = cms.untracked.string('n'),
  variables = cms.VPSet(),
)

photonTree.variables.extend(kinematicVariables)
photonTree.variables.extend(photonIdVariables)
photonTree.variables.extend(photonIsolationVariables)
