import FWCore.ParameterSet.Config as cms


###############################################################################
# SOURCE COLLECTIONS
###############################################################################
meParticles = cms.EDFilter("GenParticleSelector",
  filter = cms.bool(False),
  src = cms.InputTag("genParticles"),
  cut = cms.string("status=3")
)

meParticlesPtSorted = cms.EDProducer("GenParticlePtSlicer",
  src = cms.InputTag("meParticles")
)

mePhotons = cms.EDFilter("GenParticleSelector",
  filter = cms.bool(False),
  src = cms.InputTag("meParticlesPtSorted"),
  cut = cms.string("pdgId=22")
)

isLepton = "(abs(pdgId)=11 | abs(pdgId)=13 | abs(pdgId)=15)"
meLeptons = mePhotons.clone( cut = cms.string(isLepton) )

isNeutrino = "(abs(pdgId)=12 | abs(pdgId)=14 | abs(pdgId)=16)"
meNeutrinos = mePhotons.clone( cut = cms.string(isNeutrino) )

isParton = "(abs(pdgId)<6 | pdgId=21)"
isIncoming = "mother(0).status!=3"
isOutgoing = "mother(0).status=3"
mePartons = mePhotons.clone( cut = cms.string(isParton) )
meInPartons = mePhotons.clone( 
  src = cms.InputTag("mePartons"),
  cut = cms.string(isIncoming) 
)
meOutPartons = meInPartons.clone( cut = cms.string(isOutgoing) )


###############################################################################
# HISTOGRAMS
###############################################################################

from Sherpa.Analysis.basicHistos_cfi import *

maxNJets = 2

def histos(srcName, n=-1):
  histoAnalyzer = cms.EDAnalyzer("CandViewHistoAnalyzer",
    simpleKineGenHistos,
    src = cms.InputTag(srcName)
  )
  for histo in histoAnalyzer.histograms:
    histo.itemsToPlot = n
  return histoAnalyzer

mePhotonHistos = histos("mePhotons")
meLeptonHistos = histos("meLeptons")
meNeutrinoHistos = histos("meNeutrinos")
meInPartonHistos = histos("meInPartons", 2)
# customize the pt histogram
if len(meInPartonHistos.histograms)>0:
  meInPartonHistos.histograms[0].max = 10
# customize the eta histogram
if len(meInPartonHistos.histograms)>1:
  meInPartonHistos.histograms[1].nbins = 300
  meInPartonHistos.histograms[1].min = -15
  meInPartonHistos.histograms[1].max = 15
# customize the y histogram
if len(meInPartonHistos.histograms)>3:
  meInPartonHistos.histograms[3].nbins = 300
  meInPartonHistos.histograms[3].min = -15
  meInPartonHistos.histograms[3].max = 15
meOutPartonHistos = histos("meOutPartons", maxNJets)

drMePhotonHistos = cms.EDAnalyzer("DeltaRAnalyzer",
  srcA = cms.untracked.InputTag("mePhotons"),
  srcB = cms.untracked.InputTag("meParticles"),
  histoCount = cms.untracked.uint32(7)
)

drMePhotonLeptonHistos = drMePhotonHistos.clone(
  srcB = cms.untracked.InputTag("meLeptons"),
  histoCount = cms.untracked.uint32(1),
  max = cms.untracked.double(10),
  nbins = cms.untracked.int32(400),
)

drMePhotonNeutrinoHistos = drMePhotonLeptonHistos.clone(
  srcB = cms.untracked.InputTag("meNeutrinos"),
)

drMePhotonOutPartonHistos = drMePhotonLeptonHistos.clone(
  srcB = cms.untracked.InputTag("meOutPartons"),
  histoCount = cms.untracked.uint32(maxNJets),
)

#drMePhotonInPartonHistos = drMePhotonInPartonsHistos.clone(
  #srcB = cms.untracked.InputTag("meInPartons"),
#)

lngHistos = cms.EDAnalyzer("LNGammaAnalyzer",
  srcLeptons = cms.untracked.InputTag("meLeptons"),
  srcNeutrinos = cms.untracked.InputTag("meNeutrinos"),
  srcPhotons = cms.untracked.InputTag("mePhotons")
)

jetCountHisto = cms.EDAnalyzer("CandViewCountAnalyzer",
  src = cms.untracked.InputTag("meOutPartons")
)


###############################################################################
# SEQUENCES
###############################################################################

allMeCollections = cms.Sequence(meParticles * meParticlesPtSorted *
    (mePhotons+meLeptons+meNeutrinos+mePartons*(meInPartons+meOutPartons) )
)

allHistos = cms.Sequence(
  mePhotonHistos
  +meLeptonHistos
  +meNeutrinoHistos
  +meInPartonHistos
  +meOutPartonHistos
  +drMePhotonLeptonHistos
  +drMePhotonNeutrinoHistos
  +drMePhotonOutPartonHistos
  +lngHistos
  +jetCountHisto
)

wgHistos = cms.Sequence(allMeCollections * allHistos)

