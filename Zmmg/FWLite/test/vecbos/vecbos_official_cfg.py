import FWCore.ParameterSet.Config as cms
import os

process = cms.Process('VecBosAnalysis')

process.inputs = cms.PSet(fileNames = cms.vstring())

tier2_path = '/mnt/tier2/store/user/veverka/'
dataset_path = (
    'DYToMuMu_M_20_TuneZ2star_8TeV_pythia6/'
    'Summer12-PU_S7_START52_V9-v1_AOD_VecBosV16-5_2_X/v1/'
    )
for filename in '''default_MC_1_1_DaX.root  
                   default_MC_3_1_wPQ.root  
                   default_MC_4_1_zjx.root'''.split():
    process.inputs.fileNames.append(
        os.path.join(tier2_path, dataset_path, filename)
        )

process.outputs = cms.PSet(
    outputName = cms.string('vecbos_official.root')
    )
    
process.maxEvents = cms.PSet(
    input = cms.untracked.int64(-1),
    reportEvery = cms.untracked.int64(500)
    )

