import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.patSequences_cff import *
from HtoZg.CommonAnalysis.photonUserData_cff import photonUserFloats
from HtoZg.CommonAnalysis.photonUserData_cff import photonUserInts
from HtoZg.CommonAnalysis.photonUserDataSequence_cff import *
from HtoZg.MuonAnalysis.muonUserData_cff import muonUserFloats
from HtoZg.MuonAnalysis.muonUserDataSequence_cff import *

## Customize the pat defaults
patMuons  .userData.userFloats.src += muonUserFloats
patPhotons.userData.userFloats.src += photonUserFloats
patPhotons.userData.userInts  .src += photonUserInts

## Prepend the user data production
patSequence = cms.Sequence(muonUserDataSequence +
                           photonUserDataSequence +
                           patDefaultSequence)
