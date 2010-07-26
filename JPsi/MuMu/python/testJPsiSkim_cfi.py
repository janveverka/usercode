import FWCore.ParameterSet.Config as cms

from JPsi.MuMu.glbMuons_cfi import *
from JPsi.MuMu.trkMuons_cfi import *
from JPsi.MuMu.dimuons_cfi import *


from ElectroWeakAnalysis.MultiBosons.Histogramming.muonHistos_cfi import *
muonHistos.src = "selectedPatMuons"

muonHistos5 = muonHistos.clone()

setItemsToPlot(muonHistos5,
  itemsToPlot = 5,
  namePostfix = "_%d",
  titlePrefix = "%d. hardest muon "
)

glbMuonHistos = muonHistos.clone(src = "glbMuons")
trkMuonHistos = muonHistos.clone(src = "trkMuons")


from ElectroWeakAnalysis.MultiBosons.Histogramming.histoTools_cff import *
from ElectroWeakAnalysis.MultiBosons.Histogramming.compositeKineHistos_cff import *

dimuonsOSHistos = makeHistoAnalyzer("CandViewHistoAnalyzer",
  histos = compositeKineHistos +
    [massHisto.clone(min=2, max=4, nbins=1000, name="massJpsi")],
  srcName = "dimuonsOS",
)

dimuonsSSHistos = dimuonsOSHistos.clone(src = "dimuonsSS")
dimuonsGGOSHistos = dimuonsOSHistos.clone(src = "dimuonsGGOS")
dimuonsGGSSHistos = dimuonsOSHistos.clone(src = "dimuonsGGSS")
dimuonsGTOSHistos = dimuonsOSHistos.clone(src = "dimuonsGTOS")
dimuonsGTSSHistos = dimuonsOSHistos.clone(src = "dimuonsGTSS")
dimuonsTTOSHistos = dimuonsOSHistos.clone(src = "dimuonsTTOS")
dimuonsTTSSHistos = dimuonsOSHistos.clone(src = "dimuonsTTSS")

counts = cms.EDAnalyzer("CandViewCountAnalyzer",
  nbins = cms.untracked.uint32(21),
  histograms = cms.untracked.VPSet(
    #cms.PSet( src = cms.untracked.InputTag("standAloneMuons") ),
    cms.PSet( src = cms.untracked.InputTag("selectedPatMuons") ),
    cms.PSet( src = cms.untracked.InputTag("glbMuons") ),
    cms.PSet( src = cms.untracked.InputTag("trkMuons") ),
    cms.PSet( src = cms.untracked.InputTag("dimuonsOS") ),
    cms.PSet( src = cms.untracked.InputTag("dimuonsSS") ),
    cms.PSet( src = cms.untracked.InputTag("dimuonsGGOS") ),
    cms.PSet( src = cms.untracked.InputTag("dimuonsGGSS") ),
    cms.PSet( src = cms.untracked.InputTag("dimuonsGTOS") ),
    cms.PSet( src = cms.untracked.InputTag("dimuonsGTSS") ),
    cms.PSet( src = cms.untracked.InputTag("dimuonsTTOS") ),
    cms.PSet( src = cms.untracked.InputTag("dimuonsTTSS") ),
    #cms.PSet( src = cms.untracked.InputTag("goodTracks") ),
  )
)


jpsiSequence = cms.Sequence(muonHistos +
  ( glbMuons * glbMuonHistos
    + trkMuons * trkMuonHistos
    + dimuonsOS * dimuonsOSHistos
    + dimuonsSS * dimuonsSSHistos
    + dimuonsGGOS * dimuonsGGOSHistos
    + dimuonsGGSS * dimuonsGGSSHistos
    + dimuonsGTOS * dimuonsGTOSHistos
    + dimuonsGTSS * dimuonsGTSSHistos
    + dimuonsTTOS * dimuonsTTOSHistos
    + dimuonsTTSS * dimuonsTTSSHistos ) +
  counts
)

#goodTrackHistos = makeHistoAnalyzer("CandViewHistoAnalyzer",
  #histos = leafKineHistos,
  #srcName = "goodTracks",
  #itemsToPlot = 2
#)
