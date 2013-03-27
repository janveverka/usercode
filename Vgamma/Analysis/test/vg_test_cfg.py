import copy
import os
import socket
import getpass
import FWCore.ParameterSet.Config as cms

from Vgamma.Analysis.histos_cff import fullSelection
from Vgamma.Analysis.histos_cff import noSelection
from Vgamma.Analysis.activeBranches_cff import activeBranchesMC

process = cms.Process('VgammaAnalysis')

#______________________________________________________________________________
process.inputs = cms.PSet(
    fileNames = cms.vstring(),
    treeName = cms.string('EventTree'),
    version = cms.string('V14MC'),
    activeBranches = copy.deepcopy(activeBranchesMC),
    )

dataset_path = os.path.join(os.environ['CMSSW_BASE'],
                            'src/Vgamma/Analysis/data')
for filename in [
    #'ZGammaToMuMuGamma_2Jet_MG5_TuneZ2_mmgSkim_test10.root',
    'ZGammaToMuMuGamma_2Jet_MG5_TuneZ2_mmgSkim_test1000.root',
    #'DoubleMu_Run2011A-05Aug2011-v1_mmgSkim_5kevt.root',
    ]:
    process.inputs.fileNames.append(
        os.path.join(dataset_path, filename)
        )

#______________________________________________________________________________
process.outputs = cms.PSet(
    outputName = cms.string('vg_test.root')
    )
    
#______________________________________________________________________________
process.maxEvents = cms.PSet(
    toProcess = cms.untracked.int64(-1),
    reportEvery = cms.untracked.int64(100)
    )
    
#______________________________________________________________________________
allEvents = copy.deepcopy(noSelection)
allMuons = copy.deepcopy(fullSelection)
selectedMuons = copy.deepcopy(fullSelection)
selectedDimuons = copy.deepcopy(fullSelection)
selectedPhotons = copy.deepcopy(fullSelection)
selectedZgs = copy.deepcopy(fullSelection)
FullSelection = copy.deepcopy(fullSelection)


allMuons.selection.cutsToIgnore = ['selectMuons', 'selectPhoton',
                                   'selectDimuons', 'selectZg']
allMuons.do = ['Muons']

selectedMuons.selection.cutsToIgnore = ['selectPhoton', 'selectZg']
selectedMuons.do = ['Muons']

selectedDimuons.selection.cutsToIgnore = ['selectMuons', 'selectPhoton',
                                          'selectZg']
selectedDimuons.do = ['Dimuons']

selectedPhotons.selection.cutsToIgnore = ['selectMuons', 'selectDimuons',
                                          'selectZg']
selectedPhotons.do = ['Photons']

selectedZgs.selection.cutsToIgnore =  ['selectMuons', 'selectPhoton',
                                       'selectDimuons']
selectedZgs.do = ['mmgCands']

histograms = cms.PSet(
    isMC = cms.bool(True),
    #AllEvents = copy.deepcopy(allEvents),
#    allMuons = copy.deepcopy(allMuons),
    #selectedMuons = copy.deepcopy(selectedMuons),
    #selectedDimuons = copy.deepcopy(selectedDimuons),
    #selectedPhotons = copy.deepcopy(selectedPhotons),
    #selectedZgs = copy.deepcopy(selectedZgs),
    FullSelection = copy.deepcopy(FullSelection),
    )


## Histograms configuration
process.histograms = copy.deepcopy(histograms)

#______________________________________________________________________________
## Event weight
process.eventWeight = cms.PSet(
    crossSectionInPicoBarns = cms.double(45.2),
    scaleToLumiInInverseFemtoBarns = cms.double(4.9989),
    totalProcessedEvents = cms.int64(472380),
    )

#______________________________________________________________________________
process.options = cms.PSet(
    verbosity = cms.int64(1)
    )
    
if __name__ == '__main__':
    import user
    
