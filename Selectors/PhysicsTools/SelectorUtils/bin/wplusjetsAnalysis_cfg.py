import FWCore.ParameterSet.Config as cms

process = cms.Process("FWLitePlots")


process.load('PhysicsTools.SelectorUtils.wplusjetsAnalysis_cfi')

process.inputs = cms.PSet (
    fileNames = cms.vstring(
        # Your data goes here:
#         '/Volumes/MyBook/Data/TTbar/shyft_35x_v3/ljmet_1.root'
#         'file:zmm_pat.root'
        'file:wm_pat.root'
        )
)

process.outputs = cms.PSet (
    outputName = cms.string('wplusjetsPlots.root')
)

process.wplusjetsAnalysis.muonSrc = "cleanPatMuons"
process.wplusjetsAnalysis.electronSrc = "cleanPatElectrons"
process.wplusjetsAnalysis.jetSrc = "cleanPatJets"

process.wplusjetsAnalysis.minJets = 2

