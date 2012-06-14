import FWCore.ParameterSet.Config as cms
import os

process = cms.Process('VecBosAnalysis')

process.inputs = cms.PSet(fileNames = cms.vstring())

tier2_path = '/mnt/tier2/store/user/veverka/'
dataset_path = (
    'DYToMuMu_M_20_FSRFilter_8_TuneZ2star_8TeV_pythia6_GEN_SIM_v1/'
    'veverka-_step3_RAW2DIGI_L1Reco_RECO_PU_v1-'
    '90a3c643a4855c1621ba3bfcbef2e742_VecBosV16-5_2_X/v1/'
    )
for filename in '''default_MC_1_1_9FG.root  
                   default_MC_2_1_7oZ.root  
                   default_MC_3_2_Q4f.root  
          
          default_MC_4_1_B7D.root'''.split():
    process.inputs.fileNames.append(
        os.path.join(tier2_path, dataset_path, filename)
        )

process.outputs = cms.PSet(
    outputName = cms.string('vecbos_private.root')
    )
    
process.maxEvents = cms.PSet(
    input = cms.untracked.int64(-1),
    reportEvery = cms.untracked.int64(500)
    )

