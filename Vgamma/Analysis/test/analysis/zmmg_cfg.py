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
from Vgamma.Analysis.bookkeeping.samples import mumugamma as samples

sample = samples['zmmg']
data = samples['mm2011AB']

process = cms.Process('VgammaAnalysis')

process.inputs = cms.PSet(
    fileNames = cms.vstring() + sample.skim_filenames,
    treeName = cms.string('EventTree'),
    version = cms.string('V15MC'),
    activeBranches = copy.deepcopy(activeBranchesMC),
    )

process.outputs = cms.PSet(
    outputName = cms.string(sample.name + '.root')
    )
    
process.maxEvents = cms.PSet(
    toProcess = cms.untracked.int64(int(-1)),
    reportEvery = cms.untracked.int64(10000)
    )
    

## Histograms configuration
process.histograms = cms.PSet(
    isMC = cms.bool(True),
    #NoSelection   = copy.deepcopy(noSelection  ),
    FullSelection = copy.deepcopy(fullSelection),
    )

#______________________________________________________________________________
## Event weight
process.eventWeight = cms.PSet(
    crossSectionInPicoBarns = cms.double(sample.cross_section_in_pb),
    scaleToLumiInInverseFemtoBarns = cms.double(1e-3 * data.lumi_per_pb),
    totalProcessedEvents = cms.int64(sample.total_processed_events),
    )

if __name__ == '__main__':
    import user
