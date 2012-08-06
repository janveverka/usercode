import FWCore.ParameterSet.Config as cms
import HtoZg.MuonAnalysis.looseMuons_cfi as preselection

from PhysicsTools.PatAlgos.patSequences_cff import *
from HtoZg.MuonAnalysis.muonUserData_cff import muonUserFloats
from HtoZg.MuonAnalysis.muonUserDataSequence_cff import *

## Customize the pat defaults
patMuons.userData.userFloats.src += muonUserFloats

selectedPatMuons.cut = preselection.looseMuons.cut.value() + '''&& 
    abs(userFloat("muonVertexing:dxy")) < 0.2 &&
    abs(userFloat("muonVertexing:dz")) < 0.5
    '''

countPatMuons.minNumber = 2

## Prepend the user data production
patSequence = cms.Sequence(muonUserDataSequence +
                           patDefaultSequence)
