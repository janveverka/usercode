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

process.wplusjetsAnalysis.minJets = 1

## Convert cms.EDAnalyzer to cms.PSet
from ElectroWeakAnalysis.MultiBosons.Histogramming.muonHistos_cfi import muonHistos
process.muonHistosAll = cms.PSet(
  src = cms.InputTag(muonHistos.src.value() ),
  histograms = muonHistos.histograms.copy(),
  outputDirectory = cms.string('allMuons')
)

process.muonHistosSel = process.muonHistosAll.clone(
  outputDirectory = "selMuons"
)



