import copy
import os
import socket
import getpass
import FWCore.ParameterSet.Config as cms
import Vgamma.Analysis.cuts as cuts

from Vgamma.Analysis.activeBranches_cff import activeBranchesMC
from Vgamma.Analysis.histos_cff import fullSelection
from Vgamma.Analysis.histos_cff import noSelection
from Vgamma.Analysis.tools import load_input_files

process = cms.Process('VgammaAnalysis')

process.inputs = cms.PSet(
    fileNames = load_input_files('MC/mmg_zjets_susy.dat'),
    treeName = cms.string('EventTree'),
    version = cms.string('V14MC'),
    activeBranches = copy.deepcopy(activeBranchesMC),
    )

process.outputs = cms.PSet(
    outputName = cms.string('zjets.root')
    )
    
process.maxEvents = cms.PSet(
    input = cms.untracked.int64(int(-1)),
    reportEvery = cms.untracked.int64(10000)
    )
    

## Histograms configuration
process.histograms = cms.PSet(
    isMC = cms.bool(True),
    #NoSelection   = copy.deepcopy(noSelection  ),
    FullSelection = copy.deepcopy(fullSelection),
    )


if __name__ == '__main__':
    import user
