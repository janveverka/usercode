import copy
import os
import socket
import getpass
import FWCore.ParameterSet.Config as cms


process = cms.Process('VgammaAnalysis')

process.inputs = cms.PSet(
    fileNames = cms.vstring(),
    treeName = cms.string('EventTree'),
    )

dataset_path = os.path.join(os.environ['CMSSW_BASE'],
                            'src/Vgamma/Analysis/data')
for filename in '''
                ZGammaToMuMuGamma_2Jet_MG5_TuneZ2_mmgSkim_test10.root
                '''.split():
    process.inputs.fileNames.append(
        os.path.join(dataset_path, filename)
        )

process.outputs = cms.PSet(
    outputName = cms.string('vg_test.root')
    )
    
process.maxEvents = cms.PSet(
    input = cms.untracked.int64(-1),
    reportEvery = cms.untracked.int64(100)
    )
    
process.options = cms.PSet(
    titleStyle = cms.string("mpl")
    )

    
## Default muuon selection
muonCuts = cms.PSet(
    isGlobalMuon = cms.bool(True),
    maxNormChi2 = cms.double(10),
    minMuonHits = cms.uint32(1),
    isTrackerMuon = cms.bool(True),
    )

## Default histo manager setup
histos = cms.PSet(
    do = cms.vstring('Muons', 'Photons', 'Pileup'),
    selection = cms.PSet(
        selectMuons = cms.bool(True),
        selectPhoton = cms.bool(False),
        muonCuts = muonCuts.copy(),
        ),
    )

histograms = cms.PSet(
    isMC = cms.bool(True),
    allEvents = copy.deepcopy(histos),
    allMuons = copy.deepcopy(histos),
    selectedMuons = copy.deepcopy(histos),
    )

histograms.allEvents.selection.selectMuons = False

histograms.allMuons.selection.selectMuons = False
histograms.allMuons.do = ['Muons']

histograms.selectedMuons.do = ['Muons']

## Histograms configuration
process.histograms = histograms.copy()

if __name__ == '__main__':
    import user
    