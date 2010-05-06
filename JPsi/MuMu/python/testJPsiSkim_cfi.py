import FWCore.ParameterSet.Config as cms

glbMuons = cms.EDFilter("PATMuonSelector",
  src = cms.InputTag("patMuons"),
  cut = cms.string('isGlobalMuon = 1' +
                   '& muonID("GlobalMuonPromptTight") = 1' +
                   '& pt > 1' +
                   '& abs(dB) < 0.05' +
                   '& trackIso < 0.1' +
                   '& hcalIso < 0.1')
)

trkMuons = cms.EDFilter("PATMuonSelector",
  src = cms.InputTag("patMuons"),
  cut = cms.string('isGlobalMuon = 0' +
                   '& isTrackerMuon = 1 &' +
                   'muonID("TMLastStationAngTight") = 1' +
                   '& pt > 1' +
                   '& p > 2.5' +
                   '& abs(dB) < 0.05' +
                   '& trackIso < 0.1' +
                   '& hcalIso < 0.1')
)

dimuonsOS = cms.EDProducer("CandViewShallowCloneCombiner",
    checkCharge = cms.bool(True),
    cut = cms.string('0 < mass'),
    decay = cms.string('patMuons@+ patMuons@-')
)

dimuonsSS = dimuonsOS.clone(decay = cms.string('patMuons@+ patMuons@+') )

dimuonsGlbGlbOS = dimuonsOS.clone(decay = cms.string('glbMuons@+ glbMuons@-') )
dimuonsGlbGlbSS = dimuonsOS.clone(decay = cms.string('glbMuons@+ glbMuons@+') )

dimuonsGlbTrkOS = dimuonsOS.clone(decay = cms.string('glbMuons@+ trkMuons@-') )
dimuonsGlbTrkSS = dimuonsOS.clone(decay = cms.string('glbMuons@+ trkMuons@+') )

dimuonsTrkTrkOS = dimuonsOS.clone(decay = cms.string('trkMuons@+ trkMuons@-') )
dimuonsTrkTrkSS = dimuonsOS.clone(decay = cms.string('trkMuons@+ trkMuons@+') )

from ElectroWeakAnalysis.MultiBosons.Histogramming.muonHistos_cfi import *
muonHistos.src = "patMuons"

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
dimuonsGlbGlbOSHistos = dimuonsOSHistos.clone(src = "dimuonsGlbGlbOS")
dimuonsGlbGlbSSHistos = dimuonsOSHistos.clone(src = "dimuonsGlbGlbSS")
dimuonsGlbTrkOSHistos = dimuonsOSHistos.clone(src = "dimuonsGlbTrkOS")
dimuonsGlbTrkSSHistos = dimuonsOSHistos.clone(src = "dimuonsGlbTrkSS")
dimuonsTrkTrkOSHistos = dimuonsOSHistos.clone(src = "dimuonsTrkTrkOS")
dimuonsTrkTrkSSHistos = dimuonsOSHistos.clone(src = "dimuonsTrkTrkSS")

counts = cms.EDAnalyzer("CandViewCountAnalyzer",
  nbins = cms.untracked.uint32(21),
  histograms = cms.untracked.VPSet(
    #cms.PSet( src = cms.untracked.InputTag("standAloneMuons") ),
    cms.PSet( src = cms.untracked.InputTag("patMuons") ),
    cms.PSet( src = cms.untracked.InputTag("glbMuons") ),
    cms.PSet( src = cms.untracked.InputTag("trkMuons") ),
    cms.PSet( src = cms.untracked.InputTag("dimuonsOS") ),
    cms.PSet( src = cms.untracked.InputTag("dimuonsSS") ),
    cms.PSet( src = cms.untracked.InputTag("dimuonsGlbGlbOS") ),
    cms.PSet( src = cms.untracked.InputTag("dimuonsGlbGlbSS") ),
    cms.PSet( src = cms.untracked.InputTag("dimuonsGlbTrkOS") ),
    cms.PSet( src = cms.untracked.InputTag("dimuonsGlbTrkSS") ),
    cms.PSet( src = cms.untracked.InputTag("dimuonsTrkTrkOS") ),
    cms.PSet( src = cms.untracked.InputTag("dimuonsTrkTrkSS") ),
    #cms.PSet( src = cms.untracked.InputTag("goodTracks") ),
  )
)


jpsiSequence = cms.Sequence(muonHistos +
  ( glbMuons * glbMuonHistos
    + trkMuons * trkMuonHistos
    + dimuonsOS * dimuonsOSHistos
    + dimuonsSS * dimuonsSSHistos
    + dimuonsGlbGlbOS * dimuonsGlbGlbOSHistos
    + dimuonsGlbGlbSS * dimuonsGlbGlbSSHistos
    + dimuonsGlbTrkOS * dimuonsGlbTrkOSHistos
    + dimuonsGlbTrkSS * dimuonsGlbTrkSSHistos
    + dimuonsTrkTrkOS * dimuonsTrkTrkOSHistos
    + dimuonsTrkTrkSS * dimuonsTrkTrkSSHistos )
  + counts
)

#goodTrackHistos = makeHistoAnalyzer("CandViewHistoAnalyzer",
  #histos = leafKineHistos,
  #srcName = "goodTracks",
  #itemsToPlot = 2
#)
