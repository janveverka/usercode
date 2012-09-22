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

dataset_path = '/home/cms/veverka/data_mmgSkim'
for filename in '''
    DoubleMu_Run2011A-May10ReReco-v1_mmgSkim.root      
    DoubleMu_Run2011A-05Aug2011-v1_mmgSkim.root        
    DoubleMu_Run2011A-03Oct2011-v1_mmgSkim.root        
    DoubleMu_Run2011A-PromptReco-v4_mmgSkim.root
    DoubleMu_Run2011B-PromptReco-v1_run175860_178078_mmgSkim.root
    DoubleMu_Run2011B-PromptReco-v1_run178098_178677_mmgSkim.root
    DoubleMu_Run2011B-PromptReco-v1_run178703_179431_mmgSkim.root
    DoubleMu_Run2011B-PromptReco-v1_run179434_180252_mmgSkim.root
    '''.split():
    process.inputs.fileNames.append(
        os.path.join(dataset_path, filename)
        )

process.outputs = cms.PSet(
    outputName = cms.string('vg_data.root')
    )
    
process.maxEvents = cms.PSet(
    input = cms.untracked.int64(-1),
    reportEvery = cms.untracked.int64(1000)
    )
    

## Default dimuon selection
dimuonCuts = cms.PSet(
    charge = cms.int32(0),
    minMass = cms.double(50),
    )

from Vgamma.Analysis.cuts.muon import muon_cuts_sep2012 as muonCuts
from Vgamma.Analysis.cuts.photon import photon_barrel_cuts_sep2012
from Vgamma.Analysis.cuts.photon import photon_endcap_cuts_sep2012

## Default dimuon selection
ZgCuts = cms.PSet(
    minDeltaR = cms.double(0.7),
    )

## Default histo manager setup
histos = cms.PSet(
    do = cms.vstring('Muons', 'Photons', 'Dimuons', 'mmgCands', 'Pileup'),
    selection = cms.PSet(
        selectMuons = cms.bool(True),
        selectDimuons = cms.bool(True),
        selectPhoton = cms.bool(True),
        selectZg = cms.bool(True),
        cutsToIgnore = cms.vstring(),
        muonCuts = copy.deepcopy(muonCuts),
        dimuonCuts = copy.deepcopy(dimuonCuts),
        photonBarrelCuts = copy.deepcopy(photon_barrel_cuts_sep2012),
        photonEndcapCuts = copy.deepcopy(photon_endcap_cuts_sep2012),
        ZgCuts = copy.deepcopy(ZgCuts)
        ),
    )

No_Selection = copy.deepcopy(histos)
No_Selection.selection.cutsToIgnore = ['selectMuons', 'selectPhoton',
                                       'selectDimuons', 'selectZg']

## Histograms configuration
process.histograms = cms.PSet(
    isMC = cms.bool(False),
    No_Selection = No_Selection,
    Full_Selection = copy.deepcopy(histos),
    )


if __name__ == '__main__':
    import user
    
