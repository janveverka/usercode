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

    
## Default muon selection
muonCuts = cms.PSet(
    isGlobalMuon = cms.bool(True),
    maxNormChi2 = cms.double(10),
    minMuonHits = cms.uint32(1),
    isTrackerMuon = cms.bool(True),
    )

## Default dimuon selection
dimuonCuts = cms.PSet(
    minMass = cms.double(50),
    )

## Default photon selection
photonCuts = cms.PSet(
    minPt = cms.double(15),
    maxAbsEtaSC = cms.double(2.4),
    )

## Default histo manager setup
histos = cms.PSet(
    do = cms.vstring('Muons', 'Photons', 'Dimuons', 'mmgCands', 'Pileup'),
    selection = cms.PSet(
        selectMuons = cms.bool(True),
        selectDimuons = cms.bool(True),
        selectPhoton = cms.bool(True),
        cutsToIgnore = cms.vstring(),
        muonCuts = copy.deepcopy(muonCuts),
        dimuonCuts = copy.deepcopy(dimuonCuts),
        photonCuts = copy.deepcopy(photonCuts),
        ),
    )

allEvents = copy.deepcopy(histos)
allMuons = copy.deepcopy(histos)
selectedMuons = copy.deepcopy(histos)
selectedDimuons = copy.deepcopy(histos)
selectedPhotons = copy.deepcopy(histos)

allEvents.selection.cutsToIgnore = ['selectMuons', 'selectPhoton',
                                    'selectDimuons']

allMuons.selection.cutsToIgnore = ['selectMuons', 'selectPhoton',
                                   'selectDimuons']
allMuons.do = ['Muons']

selectedMuons.selection.cutsToIgnore = ['selectPhoton']
selectedMuons.do = ['Muons']

selectedDimuons.selection.cutsToIgnore = ['selectMuons', 'selectPhoton']
selectedDimuons.do = ['Dimuons']

selectedPhotons.selection.cutsToIgnore = ['selectMuons', 'selectDimuons']
selectedPhotons.do = ['Photons']

histograms = cms.PSet(
    isMC = cms.bool(True),
   allEvents = copy.deepcopy(allEvents),
#    allMuons = copy.deepcopy(allMuons),
    selectedMuons = copy.deepcopy(selectedMuons),
    selectedDimuons = copy.deepcopy(selectedDimuons),
    selectedPhotons = copy.deepcopy(selectedPhotons),
    )


## Histograms configuration
process.histograms = copy.deepcopy(histograms)

if __name__ == '__main__':
    import user
    