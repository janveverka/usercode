import FWCore.ParameterSet.Config as cms

genJPsis = cms.EDFilter("GenParticleSelector",
  filter = cms.bool(False),
  src = cms.InputTag("genParticles"),
  cut = cms.string("pdgId=443 & status=2")
)

genJPsiDaughters = cms.EDFilter("GenParticleSelector",
  filter = cms.bool(False),
  src = cms.InputTag("genParticles"),
  cut = cms.string("numberOfMothers>0 & mother(0).pdgId=443 & mother(0).status=2")
)

genJPsiGrandDaughters = cms.EDFilter("GenParticleSelector",
  filter = cms.bool(False),
  src = cms.InputTag("genParticles"),
  cut = cms.string("numberOfMothers>0 & mother(0).numberOfMothers>0 & mother(0).mother(0).pdgId=443 & mother(0).mother(0).status=2")
)

genPhotons = cms.EDFilter("GenParticleSelector",
  filter = cms.bool(False),
  src = cms.InputTag("genParticles"),
  cut = cms.string("pdgId=22 & status=1")
)

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

genProducers = cms.Sequence(genJPsis +
  genJPsiDaughters +
  genPhotons
)

genHistos = cms.Sequence(genJPsiHistos +
  genJPsiDaughterHistos +
  genPhotonHistos
)

makeGenJPsiHistos = cms.Sequence(genProducers * genHistos)
