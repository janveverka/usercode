###############################################################################
## This is the VGamma PAT configuration + Skim for Spring10 MC full sim samples
###############################################################################

import copy
import FWCore.ParameterSet.Config as cms
import ElectroWeakAnalysis.MultiBosons.Skimming.VgEventContent as vgEventContent

from PhysicsTools.PatAlgos.patTemplate_cfg import * ## Default PAT process skeleton
from PhysicsTools.PatAlgos.tools.coreTools import *
from PhysicsTools.PatAlgos.tools.metTools import *
from PhysicsTools.PatAlgos.tools.trigTools import *
from PhysicsTools.PatAlgos.tools.cmsswVersionTools import *
from ElectroWeakAnalysis.MultiBosons.Skimming.egammaUserDataProducts_cff import *
from ElectroWeakAnalysis.MultiBosons.Skimming.jobOptions import *
from ElectroWeakAnalysis.MultiBosons.Skimming.matchHltPaths import *
from ElectroWeakAnalysis.MultiBosons.Skimming.options import options as defaultOptions
from ElectroWeakAnalysis.MultiBosons.tools.skimmingTools import *


## See link below for the definition of the selection
## https://twiki.cern.ch/twiki/bin/view/CMS/VGammaFirstPaper#Vgamma_Group_skims
skimVersion = 3  # Do we need this?
basePath = "ElectroWeakAnalysis.MultiBosons.Skimming." # shorthand

options = copy.deepcopy(defaultOptions)

## Define default options specific to this configuration file
#options.jobType = "testSummer10"
#options.jobType = "testPOWHEG"
#options.jobType = "testRealData"
#options.jobType = "testJetRealData"
#options.jobType = "testMC"

## Parse (command-line) arguments - this overrides the options given above
applyJobOptions(options)

## Input
process.source.fileNames = options.inputFiles

process.maxEvents.input = -1
if options.outEvents >= 0:
    process.maxEvents.output = cms.untracked.int32(options.outEvents)
    #process.maxEvents = cms.untracked.PSet( output = cms.untracked.int32(options.outEvents) )
if options.maxEvents >= 0:
    process.maxEvents.input = options.maxEvents

## Global tag
process.GlobalTag.globaltag = options.globalTag


## Remove MC matching and apply cleaning if we run on data
## (No need to remove pfMET and tcMET explicitly if this is done first
if options.isRealData:
    removeMCMatching(process)

## Add non-default MET flavors
addPfMET(process , 'PF')
addTcMET(process , 'TC')

## Spring10 MC was produced with CMSS_3_5_6 - make sure we can run on it
if options.use35XInput:
    run36xOn35xInput(process, genJets = "ak5GenJets")

## Embed lepton tracks
process.patMuons.embedTrack = True
process.patElectrons.embedTrack = True

## Keep only global and tracker muons
process.selectedPatMuons.cut = cms.string("isGlobalMuon | isTrackerMuon")

## Reject soft jets to reduce event content
process.selectedPatJets.cut = cms.string("pt > 30")

## Overlap of photons and electrons
##+ Set to True to remove overlapping photons from the event, False to embed
##+ embed the overlap information
process.cleanPatPhotons.checkOverlaps.electrons.requireNoOverlaps = False

## Add photon user data
## TODO: rename photon(electron)UserData to photon(electron)ClusterShape
process.load(basePath + "photonUserData_cfi")
process.patDefaultSequence.replace(process.patPhotons,
    process.photonUserData * process.patPhotons
    )
process.patPhotons.userData.userFloats.src = egammaUserDataFloats(
    moduleName = "photonUserData"
    )
process.patPhotons.userData.userInts.src = egammaUserDataInts(
    moduleName = "photonUserData"
    )

process.load("RecoEcal.EgammaClusterProducers.preshowerClusterShape_cfi")
process.load("EgammaAnalysis.PhotonIDProducers.piZeroDiscriminators_cfi")

process.load("ElectroWeakAnalysis.MultiBosons.Skimming.pi0Discriminator_cfi")

if not options.isRealData:
    process.photonGenMatch = cms.EDProducer("PhotonGenMatchUserDataProducer",
        src = cms.InputTag("photons"),
        match = cms.InputTag("photonMatch")
        )
    process.patDefaultSequence.replace(process.patPhotons,
        process.photonGenMatch *
        process.patPhotons
        )
    process.patPhotons.userData.userInts.src.extend([
        cms.InputTag("photonGenMatch", "motherPdgId"),
        cms.InputTag("photonGenMatch", "motherStatus"),
        cms.InputTag("photonGenMatch", "grandMotherPdgId"),
        cms.InputTag("photonGenMatch", "grandMotherStatus"),
        ])

process.patDefaultSequence.replace(process.patPhotons,
    process.preshowerClusterShape *
    process.piZeroDiscriminators  *
    process.pi0Discriminator      *
    process.patPhotons
    )
process.patPhotons.userData.userFloats.src.append(
    cms.InputTag("pi0Discriminator")
    )

## Add electron user data
process.load(basePath + "electronUserData_cfi")
process.patDefaultSequence.replace(process.patElectrons,
    process.electronUserData * process.patElectrons
    )
process.patElectrons.userData.userFloats.src = egammaUserDataFloats(
    moduleName = "electronUserData"
    )
process.patElectrons.userData.userInts.src = egammaUserDataInts(
    moduleName = "electronUserData"
    )

## Add electron official electron ID from the Egamma / VBTF
process.load("ElectroWeakAnalysis.WENu.simpleEleIdSequence_cff")
process.patDefaultSequence.replace(process.patElectrons,
    process.simpleEleIdSequence * process.patElectrons
    )
process.patElectrons.addElectronID = cms.bool(True)
process.patElectrons.electronIDSources = cms.PSet(
    simpleEleId95relIso = cms.InputTag("simpleEleId95relIso"),
    simpleEleId90relIso = cms.InputTag("simpleEleId90relIso"),
    simpleEleId85relIso = cms.InputTag("simpleEleId85relIso"),
    simpleEleId80relIso = cms.InputTag("simpleEleId80relIso"),
    simpleEleId70relIso = cms.InputTag("simpleEleId70relIso"),
    simpleEleId60relIso = cms.InputTag("simpleEleId60relIso"),
    simpleEleId95cIso   = cms.InputTag("simpleEleId95cIso"),
    simpleEleId90cIso   = cms.InputTag("simpleEleId90cIso"),
    simpleEleId85cIso   = cms.InputTag("simpleEleId85cIso"),
    simpleEleId80cIso   = cms.InputTag("simpleEleId80cIso"),
    simpleEleId70cIso   = cms.InputTag("simpleEleId70cIso"),
    simpleEleId60cIso   = cms.InputTag("simpleEleId60cIso"),
    )

## PAT Trigger
process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff")
switchOnTrigger(process)
process.patTrigger.processName = options.hltProcessName
process.patTriggerEvent.processName = options.hltProcessName



## Drop matched target collections from the event content to only keep the trigger matched versions
for collection in matchHltPaths.keys():
    vgEventContent.extraSkimEventContent.append("drop *_%s_*_*" % collection)
## Drop default patTriggerObjectsedmAssociation
vgEventContent.extraSkimEventContent.append(
    "drop patTriggerObjectsedmAssociation_patTriggerEvent_*_*"
    )


## HLT trigger
process.load(basePath + "hltFilter_cfi")
process.hltFilter.TriggerResultsTag = \
    "TriggerResults::" + options.hltProcessName

## Add cleaning of collision data (no scraping events etc.)
##+ https://twiki.cern.ch/twiki/bin/viewauth/CMS/Collisions2010Recipes
process.load(basePath + "goodCollisionDataSequence_cff")
## Remove the hltPhysicsDeclared - it kills some good events, reference?
process.goodCollisionDataSequence.remove(process.hltPhysicsDeclared)
## Run the hltPhysicsDeclared filter in a separate path to
##+ store its result in the triggerEvent product.
process.hltPhysicsDeclaredPath = cms.Path(process.hltPhysicsDeclared)

## Define the path that's used to select events
process.skimFilterSequence = cms.Sequence(
    process.hltFilter +
    process.goodCollisionDataSequence
    ) # Extend below
process.skimFilterPath = cms.Path(process.skimFilterSequence)

#removeTriggerPathsForAllBut(matchHltPaths, ["cleanPatElectrons"])
removeTriggerPathsForAllBut(matchHltPaths, ["cleanPatElectrons"])
## Don't require any triggers.
process.skimFilterSequence.remove(process.hltFilter)
## Require the Muon PD
# process.hltFilter.HLTPaths = ["*Mu*"]
if not options.ignoreSkimFilter:
    process.load("Zee.Skimming.dielectronSkimFilterSequence_cff")
    process.skimFilterSequence += process.dielectronSkimFilterSequence
## Add the photon re-reco.
addPhotonReReco(process)
## Now change the photon reco to much looser settings.
process.photonCore.minSCEt = 2.0
process.photons.minSCEtBarrel = 2.0
process.photons.minSCEtEndcap = 2.0
process.photons.maxHoverEBarrel = 10.0
process.photons.maxHoverEEndcap = 10.0
## Remove the pi0 discriminator
## (currently doesn't work with extremely loose photons)
## FIXME: make the pi0Discriminator work for these weird photons too
for module in [process.preshowerClusterShape,
                process.piZeroDiscriminators,
                process.pi0Discriminator]:
    process.patDefaultSequence.remove( module )
while cms.InputTag("pi0Discriminator") in process.patPhotons.userData.userFloats.src:
    process.patPhotons.userData.userFloats.src.remove(
        cms.InputTag("pi0Discriminator")
        )

## Add more photon-related event content (super clusters, clusters)
vgEventContent.extraSkimEventContent += \
    vgEventContent.vgExtraPhotonEventContent

embedTriggerMatches(process, matchHltPaths)

if options.isRealData:
    process.defaultSequence = cms.Sequence(
        process.skimFilterSequence +
        process.patDefaultSequence
    )
else:
    process.primaryVertexFilterPath = cms.Path(process.primaryVertexFilter)
    process.noScrapingPath = cms.Path(process.noScraping)
    process.load(basePath + "prunedGenParticles_cfi")
    if not options.applyCollisionDataCleaningToMC \
        and repr(process.skimFilterSequence) != repr(cms.Sequence()):
        process.skimFilterSequence.remove(process.goodCollisionDataSequence)
    process.defaultSequence = cms.Sequence(
        process.skimFilterSequence +
        process.prunedGenParticles *
        process.patDefaultSequence
    )
# if options.isRealData <-----------------------------------------------------


process.load("Zee.Skimming.ZeeSequence_cff")
process.ZeePath   = cms.Path(
    process.defaultSequence * process.ZeeSequence
    )

## Output configuration (add event content, select events, output file name)
process.out.outputCommands += vgEventContent.extraSkimEventContent + [
    "keep *_%s_*_PAT" % collection for collection in """vbtf95Electrons
                                                        goldenElectrons
                                                        goldenDielectrons""".split()
    ]

if not options.isRealData:
    process.out.outputCommands += ["keep *_prunedGenParticles_*_PAT"]

process.out.SelectEvents.SelectEvents = ["skimFilterPath"]

process.out.fileName = options.outputFile

## Logging
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery
if not options.isRealData:
    ## Suppress many warnings about missing HLT prescale tables
    process.MessageLogger.categories += ["hltPrescaleTable"]
    process.MessageLogger.cerr.hltPrescaleTable = cms.untracked.PSet(
        limit = cms.untracked.int32(5)
        )

process.options.wantSummary = options.wantSummary

## Check for an empty path in the output
if str(process.skimFilterPath) == "None":
    del process.out.SelectEvents


## Add tab completion + history during inspection
if __name__ == "__main__": import user
