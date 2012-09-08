import FWCore.ParameterSet.Config as cms
import os

process = cms.Process('VgammaAnalysis')

process.inputs = cms.PSet(fileNames = cms.vstring())

dataset_path = '/tmp/veverka/Vgamma2011/VgKitV14/MC'
for filename in '''
                DYJetsToLL_TuneZ2_M50_Madgraph_Fall11.root  
                '''.split():
    process.inputs.fileNames.append(
        os.path.join(dataset_path, filename)
        )

process.outputs = cms.PSet(
    outputName = cms.string('vg_test.root')
    )
    
process.maxEvents = cms.PSet(
    input = cms.untracked.int64(1000),
    reportEvery = cms.untracked.int64(100)
    )
    
process.options = cms.PSet(
    titleStyle = cms.string("mpl")
    )

