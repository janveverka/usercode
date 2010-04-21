## This is based on ElectroWeakAnalysis.Skimming.zMuMu_SubskimSequences_cfi
## It should be replaced by using it and converting the paths into sequences

import FWCore.ParameterSet.Config as cms

from ElectroWeakAnalysis.Skimming.dimuonsHLTFilter_cfi import *
from ElectroWeakAnalysis.Skimming.patCandidatesForZMuMuSubskim_cff import *
from ElectroWeakAnalysis.Skimming.dimuons_cfi import *
from ElectroWeakAnalysis.Skimming.dimuonsOneTrack_cfi import *
from ElectroWeakAnalysis.Skimming.dimuonsGlobal_cfi import *
from ElectroWeakAnalysis.Skimming.dimuonsOneStandAloneMuon_cfi import *
from ElectroWeakAnalysis.Skimming.dimuonsFilter_cfi import *
from ElectroWeakAnalysis.Skimming.dimuonsOneTrackFilter_cfi import *

dimuonSequence = cms.Sequence(
    dimuonsHLTFilter *
    goodMuonRecoForDimuon *
    dimuons *
    dimuonsGlobal *
    dimuonsOneStandAloneMuon *
    dimuonsFilter    
)

dimuonOneTrackSequence = cms.Sequence(dimuonsHLTFilter+
                               goodMuonRecoForDimuon+
                               dimuonsOneTrack+
                               dimuonsOneTrackFilter
)


