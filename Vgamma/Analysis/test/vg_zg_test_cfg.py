import copy
import os
import socket
import getpass
import FWCore.ParameterSet.Config as cms
import Vgamma.Analysis.cuts as cuts

from Vgamma.Analysis.activeBranches_cff import activeBranchesData
from Vgamma.Analysis.histos_cff import fullSelection
from Vgamma.Analysis.histos_cff import noSelection
from Vgamma.Analysis.tools import load_input_files

process = cms.Process('VgammaAnalysis')

process.inputs = cms.PSet(
    fileNames = cms.vstring(),
    treeName = cms.string('EventTree'),
    version = cms.string('V15MC'),
    activeBranches = copy.deepcopy(activeBranchesData),
    )

process.inputs.fileNames = [
    '/mnt/hadoop/store/user/veverka/Vgamma2011/VgKitV15/MC_mmgSkim/ZGammaToMuMuGamma_2Jet_MG5_TuneZ2_mmgSkim.root'
    ]

process.outputs = cms.PSet(
    outputName = cms.string('vg_zg_test.root')
    )
    
process.maxEvents = cms.PSet(
    toProcess = cms.untracked.int64(int(1e7)),
    reportEvery = cms.untracked.int64(10000)
    )
    

## Histograms configuration
process.histograms = cms.PSet(
    isMC = cms.bool(False),
    #NoSelection   = copy.deepcopy(noSelection  ),
    FullSelection = copy.deepcopy(fullSelection),
    )



if __name__ == '__main__':
    import user
