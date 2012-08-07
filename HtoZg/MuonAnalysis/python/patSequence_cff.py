import FWCore.ParameterSet.Config as cms
import HtoZg.MuonAnalysis.looseMuons_cfi as preselection

from PhysicsTools.PatAlgos.patSequences_cff import *
from HtoZg.MuonAnalysis.muonUserData_cff import muonUserFloats
from HtoZg.MuonAnalysis.muonUserDataSequence_cff import *

## Customize the pat defaults
patMuons.userData.userFloats.src += muonUserFloats

## Prepend the user data production
patSequence = cms.Sequence(muonUserDataSequence +
                           patDefaultSequence)
