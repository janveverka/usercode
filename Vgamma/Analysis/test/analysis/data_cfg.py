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
    fileNames = load_input_files('RealData/2011AB_susy.dat'),
    treeName = cms.string('EventTree'),
    version = cms.string('V14Data'),
    activeBranches = copy.deepcopy(activeBranchesData),
    )

process.outputs = cms.PSet(
    outputName = cms.string('data.root')
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
