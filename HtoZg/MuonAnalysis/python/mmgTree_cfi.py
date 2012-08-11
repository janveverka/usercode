'''
Defines default configuration for a module that creates a flat ROOT tree
of mmg candidate kinematice variables used in the H->Zg analysis.

Jan Veverka, Caltech, 11 Aug 2012
'''
import FWCore.ParameterSet.Config as cms

import Misc.TreeMaker.tools as tools
from Misc.TreeMaker.kinematicVariables_cff import kinematicVariables

mmgTree = cms.EDAnalyzer('CandViewTreeMaker',
  name      = cms.untracked.string('mmg'),
  title     = cms.untracked.string('MMG variables for the H->Zg analysis'),
  src       = cms.InputTag('mmgCands'),
  prefix    = cms.untracked.string(''),
  sizeName  = cms.untracked.string('n'),
  variables = cms.VPSet(),
)

mmgTree.variables += kinematicVariables
mmgTree.variables += tools.get_variables_from_map([
    ('mmMass', 'daughter("dimuon").mass'),
    ('deltaR1', '''deltaR(daughter("dimuon").daughter(0).eta,
                          daughter("dimuon").daughter(0).phi,
                          daughter("photon").eta,
                          daughter("photon").phi)'''),
    ('deltaR2', '''deltaR(daughter("dimuon").daughter(1).eta,
                          daughter("dimuon").daughter(1).phi,
                          daughter("photon").eta,
                          daughter("photon").phi)'''),
    ('mu1Pt', 'daughter("dimuon").daughter(0).pt'),
    ('mu2Pt', 'daughter("dimuon").daughter(1).pt'),
    ('phoPt', 'daughter("photon").pt'),
    ('mu1Eta', 'daughter("dimuon").daughter(0).eta'),
    ('mu2Eta', 'daughter("dimuon").daughter(1).eta'),
    ('phoEta', 'daughter("photon").eta'),
    ('mu1Q', 'daughter("dimuon").daughter(0).charge'),
    ('mu2Q', 'daughter("dimuon").daughter(1).charge'),
    ])
