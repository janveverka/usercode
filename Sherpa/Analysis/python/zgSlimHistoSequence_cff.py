import FWCore.ParameterSet.Config as cms

import Sherpa.Analysis.basicHistos_cfi as histos

#______________________________________________________________________________
## Accounting of source collections
genParticleHistos = histos.make_histo_analyzer(
    source = 'genParticles',
    configurations = histos.simpleKineGenHistos,
    )

prunedGenParticleHistos = histos.make_histo_analyzer(
    source = 'prunedGenParticles',
    configurations = histos.simpleKineGenHistos,
    )


#______________________________________________________________________________
## Build prompt llg candidates from opposite-sign leptons and
## leading photons
promptParticles = cms.EDFilter('GenParticleSelector',
  filter = cms.bool(False),
  src = cms.InputTag('prunedGenParticles'),
  cut = cms.string('''
      status = 1 &
      (abs(pdgId) = 11 | abs(pdgId) = 13 | pdgId = 22) &
      numberOfMothers > 0 &
      mother(0).numberOfMothers > 0 &
      mother(0).mother(0).status = 3
      '''),
)

promptPhotons = cms.EDFilter('GenParticleSelector',
    filter = cms.bool(False),
    src = cms.InputTag('promptParticles'),
    cut = cms.string('pdgId = 22'),
    )

leadingPromptPhotons = cms.EDProducer('GenParticlePtSlicer',
    src = cms.InputTag('promptPhotons'),
    last = cms.untracked.int32(0),
    )

promptLeptons = cms.EDFilter('GenParticleSelector',
    filter = cms.bool(False),
    src = cms.InputTag('promptParticles'),
    cut = cms.string('abs(pdgId) = 11 | abs(pdgId) = 13')
    )

sortedPromptLeptons = cms.EDProducer('GenParticlePtSlicer',
    src = cms.InputTag('promptLeptons'),
    )

promptDileptons = cms.EDProducer('CandViewShallowClonePtrCombiner',
    checkCharge = cms.bool(True),
    cut = cms.string("abs(daughter(0).pdgId) = abs(daughter(1).pdgId)"),
    decay = cms.string("sortedPromptLeptons@+ sortedPromptLeptons@-"),
    )

llgCands = cms.EDProducer('CandViewShallowClonePtrCombiner',
    decay = cms.string("promptDileptons leadingPromptPhotons"),
    cut = cms.string('')
    )

#______________________________________________________________________________
## Histogram the selected llg candidates and their constituents
photonHistos = histos.make_histo_analyzer(
    source = 'leadingPromptPhotons',
    configurations = histos.simpleKineGenHistos,
    items_to_plot = -1,
    )

leptonHistos = histos.make_histo_analyzer(
    source = 'sortedPromptLeptons',
    configurations = histos.simpleKineGenHistos,
    items_to_plot = 2,
    )

dileptonHistos = cms.EDAnalyzer("CandViewHistoAnalyzer",
    histograms = cms.VPSet(
        histos.massHisto.clone(),
        histos.chargeHisto.clone(),
        ),
    src = cms.InputTag("promptDileptons")
)


llgMass = cms.EDAnalyzer("CandViewHistoAnalyzer",
    histograms = cms.VPSet(
        histos.massHisto.clone(
            min = 0,
            max = 500,
            nbins = 200,
            description = ';Mass (GeV);Events / 2.5 GeV',
            )
        ),
    src = cms.InputTag("llgCands")
)

llgHistos = cms.EDAnalyzer("LLGammaAnalyzer",
    srcLeptons = cms.untracked.InputTag("sortedPromptLeptons"),
    srcPhotons = cms.untracked.InputTag("leadingPromptPhotons")
)
#______________________________________________________________________________
## Build the sequence

llgCandsSequence = cms.Sequence(
    promptParticles *
    promptPhotons *
    leadingPromptPhotons *
    promptLeptons *
    sortedPromptLeptons *
    promptDileptons *
    llgCands
    )

llgHistosSequence = cms.Sequence(
    photonHistos *
    leptonHistos *
    dileptonHistos *
    llgMass *
    llgHistos
    )

zgSlimHistoSequence = cms.Sequence(
    genParticleHistos *
    prunedGenParticleHistos *
    llgCandsSequence *
    llgHistosSequence
    )
