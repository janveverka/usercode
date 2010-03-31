import FWCore.ParameterSet.Config as cms


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
isMeIncoming = "mother(0).status!=3"
isMeOutgoing = "mother(0).status=3"
mePartons = mePhotons.clone( cut = cms.string(isParton) )
meInPartons = mePhotons.clone( cut = cms.string(isMeIncoming + "&" + isParton) )
meOutPartons = mePhotons.clone( cut = cms.string(isMeOutgoing + "&" + isParton) )

# now the prompt particles
isPrompt="(status=1 & mother(0).mother(0).status=3)"
promptParticles = cms.EDFilter("GenParticleSelector",
  filter = cms.bool(False),
  src = cms.InputTag("genParticles"),
  cut = cms.string(isPrompt)
)


promptLeptons = cms.EDFilter("GenParticleSelector",
  filter = cms.bool(False),
  src = cms.InputTag("promptParticles"),
  cut = cms.string(isLepton)
)

promptMePartons = promptLeptons.clone( cut = cms.string(isParton) )
promptPhotons = promptLeptons.clone( cut = cms.string("pdgId=22") )

promptMePhotons = cms.EDFilter("GenParticleSelector",
  filter = cms.bool(False),
  src = cms.InputTag("promptPhotons"),
  cut = cms.string("mother(0).pdgId=22")
)

hasLeptonMother0 = "(abs(mother(0).pdgId)=11 |" + \
                   " abs(mother(0).pdgId)=13 |" + \
                   " abs(mother(0).pdgId)=15)"
hasPartonMother0 = "(abs(mother(0).pdgId)<6 |" + \
                   " abs(mother(0).pdgId)=21)"
promptFsrPhotons = promptMePhotons.clone( cut=cms.string(hasLeptonMother0) )
promptIsrPhotons = promptMePhotons.clone( cut=cms.string(hasPartonMother0) )

allPhotons = mePhotons.clone( cut = cms.string("status=1&pdgId=22") )

from Sherpa.Analysis.basicHistos_cfi import *

def histos(srcName, n=-1):
  histoAnalyzer = cms.EDAnalyzer("CandViewHistoAnalyzer",
    simpleKineGenHistos,
    src = cms.InputTag(srcName)
  )
  for histo in histoAnalyzer.histograms:
    histo.itemsToPlot = n
  return histoAnalyzer

mePhotonHistos = histos("mePhotons")
meLeptonHistos = histos("meLeptons", 2)
meNeutrinoHistos = histos("meNeutrinos", 2)
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
meOutPartonHistos = histos("meOutPartons", 2)
promptPhotonHistos = histos("promptPhotons")
promptMePhotonHistos = histos("promptMePhotons")
promptFsrPhotonHistos = histos("promptFsrPhotons")
promptIsrPhotonHistos = histos("promptIsrPhotons")
allPhotonHistos = histos("allPhotons")
# extend the range of mother pdg id
if len(allPhotonHistos.histograms) > 6:
  allPhotonHistos.histograms[6].nbins = 2001
  allPhotonHistos.histograms[6].min = -1000.5
  allPhotonHistos.histograms[6].max = 1000.5
promptLeptonHistos = histos("promptLeptons")
promptMePartonHistos = histos("promptMePartons")


drMePhotonHistos = cms.EDAnalyzer("DeltaRAnalyzer",
  srcA = cms.untracked.InputTag("mePhotons"),
  srcB = cms.untracked.InputTag("meParticles"),
  histoCount = cms.untracked.uint32(7)
)

drMePhotonLeptonHistos = drMePhotonHistos.clone(
  srcB = cms.untracked.InputTag("meLeptons"),
  histoCount = cms.untracked.uint32(2),
  max = cms.untracked.double(10),
  nbins = cms.untracked.int32(400),
)

drMePhotonPartonHistos = drMePhotonLeptonHistos.clone(
  srcB = cms.untracked.InputTag("mePartons"),
  histoCount = cms.untracked.uint32(4),
)

drMePhotonOutPartonHistos = drMePhotonLeptonHistos.clone(
  srcB = cms.untracked.InputTag("meOutPartons"),
)

drMePhotonInPartonHistos = drMePhotonLeptonHistos.clone(
  srcB = cms.untracked.InputTag("meInPartons"),
)

drMePhotonNeutrinoHistos = drMePhotonLeptonHistos.clone(
  srcB = cms.untracked.InputTag("meNeutrinos"),
)

llgHistos = cms.EDAnalyzer("LLGammaAnalyzer",
  srcLeptons = cms.untracked.InputTag("meLeptons"),
  srcPhotons = cms.untracked.InputTag("mePhotons")
)

nngHistos = cms.EDAnalyzer("LLGammaAnalyzer",
  srcLeptons = cms.untracked.InputTag("meNeutrinos"),
  srcPhotons = cms.untracked.InputTag("mePhotons")
)

jetCountHisto = cms.EDAnalyzer("CandViewCountAnalyzer",
  src = cms.untracked.InputTag("meOutPartons")
)




#########################################################
# SEQUENCES
#########################################################

allMeParticles = cms.Sequence(meParticles * meParticlesPtSorted *
    (mePhotons+meLeptons+meNeutrinos+mePartons+meInPartons+meOutPartons)
)

allPromptPhotons = cms.Sequence(promptPhotons*
      (promptMePhotons+promptFsrPhotons+promptIsrPhotons)
)

allPromptParticles = cms.Sequence(promptParticles *
    (promptLeptons+promptMePartons+allPromptPhotons)
)


allHistoSources = cms.Sequence(
  allMeParticles
#   +allPromptParticles
#   +allPhotons
)

allHistos = cms.Sequence(
  mePhotonHistos+
  meLeptonHistos+
  meNeutrinoHistos+
  meInPartonHistos+
  meOutPartonHistos+
#   promptLeptonHistos+
#   promptMePartonHistos+
#   promptPhotonHistos+
#   promptMePhotonHistos+
#   promptFsrPhotonHistos+
#   promptIsrPhotonHistos+
#   allPhotonHistos+
#   drMePhotonHistos+
  drMePhotonLeptonHistos+
#   drMePhotonPartonHistos+
#   drMePhotonInPartonHistos+
  drMePhotonOutPartonHistos+
  drMePhotonNeutrinoHistos+
  llgHistos+
  nngHistos
  +jetCountHisto
)

zgHistos = cms.Sequence(allHistoSources * allHistos)

