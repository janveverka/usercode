import FWCore.ParameterSet.Config as cms

genJPsis = cms.EDFilter("GenParticleSelector",
  filter = cms.bool(False),
  src = cms.InputTag("genParticles"),
  cut = cms.string("pdgId=443 & status=2")
)

genJPsiDaughters = genJPsis.clone(
  cut = "numberOfMothers>0 & mother(0).pdgId=443 & mother(0).status=2"
)

genJPsiGrandDaughters = genJPsis.clone(
  cut = "numberOfMothers>0 & mother(0).numberOfMothers>0 &" +
        "mother(0).mother(0).pdgId=443 &" +
        "mother(0).mother(0).status=2"
)

genPhotons = genJPsis.clone(cut = "pdgId=22 & status=1")

jpsiMuons = genJPsis.clone(
  cut = "status=1 & abs(pdgId)=13 & mother(0).pdgId=443"
)

jpsiPhotons = genJPsis.clone(
  cut = "status=1 & pdgId=22 & mother(0).pdgId=443"
)

jpsiDimuons = cms.EDProducer("CandViewShallowCloneCombiner",
    checkCharge = cms.bool(True),
    cut = cms.string('mass > 0'),
    decay = cms.string('jpsiMuons@+ jpsiMuons@-')
)

jpsiMmgs = jpsiDimuons.clone(decay = "jpsiDimuons jpsiPhotons")

goodMuons = genJPsis.clone(cut = "status=1 & abs(pdgId)=13 & pt>1 & p>2.5")
goodPhotons = genJPsis.clone(cut = "status=1 & pdgId=22 & pt>1")
goodDimuons = jpsiDimuons.clone(decay = "goodMuons@+ goodMuons@-")
goodMmgs = jpsiMmgs.clone(decay = "goodDimuons goodPhotons")

# jpsiMuMuDimuons = cms.EDProducer("CandViewShallowCloneCombiner",
#     checkCharge = cms.bool(True),
#     cut = cms.string('mass > 0'),
#     decay = cms.string('jpsiMuons@+ jpsiMuons@-')
# )

from Sherpa.Analysis.basicHistos_cfi import *
def histos(srcName, n=-1):
  histoAnalyzer = cms.EDAnalyzer("CandViewHistoAnalyzer",
    simpleKineGenHistos,
    src = cms.InputTag(srcName)
  )
  for histo in histoAnalyzer.histograms:
    histo.itemsToPlot = n
  histoAnalyzer.histograms[0].max = 30
  return histoAnalyzer

genJPsiHistos = cms.EDAnalyzer("CandViewHistoAnalyzer",
  histograms = cms.VPSet(
    ptHisto.clone(max=30), etaHisto, phiHisto,
    pdgIdHisto.clone(min=-1000.5, max=1000.5, nbins=2001),
    statusHisto, motherCountHisto,
    motherPdgIdHisto.clone(min=-1000.5, max=1000.5, nbins=2001),
    motherStatusHisto,
    grandmotherCountHisto,
    grandmotherPdgIdHisto.clone(min=-1000.5, max=1000.5, nbins=2001),
    grandmotherStatusHisto,
    sisterCountHisto,
    sisterPdgIdHisto.clone(min=-1000.5, max=1000.5, nbins=2001),
    daughterCountHisto, daughter0PdgIdHisto, daughter0StatusHisto,
    rapidityHisto, massHisto.clone(min=3.096916-0.001, max=3.096916+0.001)
  ).copy(),
  src = cms.InputTag("genJPsis")
)

genPhotonHistos = cms.EDAnalyzer("CandViewHistoAnalyzer",
  histograms = cms.VPSet(
    ptHisto.clone(max=30), etaHisto, phiHisto,
    pdgIdHisto,
    statusHisto, motherCountHisto,
    motherPdgIdHisto.clone(min=-1000.5, max=1000.5, nbins=2001),
    motherStatusHisto,
    grandmotherCountHisto,
    grandmotherPdgIdHisto.clone(min=-1000.5, max=1000.5, nbins=2001),
    grandmotherStatusHisto,
    sisterCountHisto,
    sisterPdgIdHisto.clone(min=-1000.5, max=1000.5, nbins=2001),
    rapidityHisto, massHisto.clone(min=3.096916-0.001, max=3.096916+0.001)
  ).copy(),
  src = cms.InputTag("genPhotons")
)

genJPsiDaughterHistos = cms.EDAnalyzer("CandViewHistoAnalyzer",
  histograms = cms.VPSet(ptHisto.clone(max=30), etaHisto, phiHisto,
    pdgIdHisto.clone(min=-1000.5, max=1000.5, nbins=2001),
    statusHisto,
    motherCountHisto,
    motherPdgIdHisto.clone(min=-1000.5, max=1000.5, nbins=2001),
    motherStatusHisto,
    grandmotherCountHisto,
    grandmotherPdgIdHisto.clone(min=-1000.5, max=1000.5, nbins=2001),
    grandmotherStatusHisto,
    sisterCountHisto, sisterPdgIdHisto,
    rapidityHisto, massHisto.clone(max=0.3),
    daughterCountHisto
  ).copy(),
  src = cms.InputTag("genJPsiDaughters")
)

jpsiPhotonHistos = genPhotonHistos.clone(src = "jpsiPhotons")
jpsiMuonHistos = genPhotonHistos.clone(src = "jpsiMuons")

from ElectroWeakAnalysis.MultiBosons.Histogramming.compositeKineHistos_cff import *

jpsiDimuonHistos = cms.EDAnalyzer("CandViewHistoAnalyzer",
  histograms = compositeKineHistos.copy() +
    [massHisto.clone(min=0, max=10, name="massJPsi")],
  src = cms.InputTag("jpsiDimuons"),
)

jpsiMmgHistos = jpsiDimuonHistos.clone(src = "jpsiMmgs")

goodPhotonHistos = genPhotonHistos.clone(src = "goodPhotons")
goodMuonHistos = genPhotonHistos.clone(src = "goodMuons")
goodDimuonHistos = jpsiDimuonHistos.clone(src = "goodDimuons")
goodMmgHistos = jpsiMmgHistos.clone(src = "goodMmgs")

jpsiDrHistos  = cms.EDAnalyzer("DeltaRAnalyzer",
  srcA = cms.untracked.InputTag("jpsiPhotons"),
  srcB = cms.untracked.InputTag("jpsiMuons"),
  histoCount = cms.untracked.uint32(4),
  max = cms.untracked.double(10),
  nbins = cms.untracked.int32(400),
)

goodDrHistos = jpsiDrHistos.clone(
  srcA = "goodPhotons",
  srcB = "goodMuons"
)

jpsiLlgHistos = cms.EDAnalyzer("LLGammaAnalyzer",
  srcLeptons = cms.untracked.InputTag("jpsiMuons"),
  srcPhotons = cms.untracked.InputTag("jpsiPhotons")
)

goodLlgHistos = jpsiLlgHistos.clone(
  srcLeptons = "goodMuons",
  srcPhotons = "goodPhotons"
)

genProducers = cms.Sequence(genJPsis +
  genJPsiDaughters +
  genPhotons +
  (jpsiMuons + jpsiPhotons) * jpsiDimuons * jpsiMmgs +
  (goodMuons + goodPhotons) * goodDimuons * goodMmgs
)

genHistos = cms.Sequence(genJPsiHistos +
  genJPsiDaughterHistos +
  genPhotonHistos +
  jpsiPhotonHistos +
  jpsiMuonHistos +
  jpsiDimuonHistos +
  jpsiMmgHistos +
  goodPhotonHistos +
  goodMuonHistos +
  goodDimuonHistos +
  goodMmgHistos +
  jpsiDrHistos +
  goodDrHistos +
  jpsiLlgHistos +
  goodLlgHistos
)

makeGenJPsiHistos = cms.Sequence(genProducers * genHistos)
