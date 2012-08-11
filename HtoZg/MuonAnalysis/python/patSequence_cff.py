import FWCore.ParameterSet.Config as cms
import HtoZg.MuonAnalysis.looseMuons_cfi as preselection

from PhysicsTools.PatAlgos.patSequences_cff import *
from HtoZg.MuonAnalysis.muonUserData_cff import muonUserFloats
from HtoZg.MuonAnalysis.muonUserDataSequence_cff import *
from HtoZg.CommonAnalysis.photonUserData_cff import photonUserFloats
from HtoZg.CommonAnalysis.photonUserDataSequence_cff import *

## Customize the pat defaults
patMuons.userData.userFloats.src += muonUserFloats
patPhotons.userData.userFloats.src += photonUserFloats

## Prepend the user data production
patSequence = cms.Sequence(muonUserDataSequence +
                           photonUserDataSequence +
                           patDefaultSequence)
