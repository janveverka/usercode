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
    version = cms.string('V14Data'),
    activeBranches = copy.deepcopy(activeBranchesData),
    )

process.inputs.fileNames = load_input_files('files_mmg_data_susy.dat')

process.outputs = cms.PSet(
    outputName = cms.string('vg_data.root')
    )
    
process.maxEvents = cms.PSet(
    input = cms.untracked.int64(-1),
    reportEvery = cms.untracked.int64(5000)
    )
    

## Histograms configuration
process.histograms = cms.PSet(
    isMC = cms.bool(False),
    NoSelection   = copy.deepcopy(noSelection  ),
    FullSelection = copy.deepcopy(fullSelection),
    )


if __name__ == '__main__':
    import user
