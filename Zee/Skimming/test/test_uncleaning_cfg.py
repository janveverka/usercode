import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

# setup 'analysis'  options
options = VarParsing.VarParsing ('analysis')



# setup any defaults you want
options.inputFiles = 'file:foo.root'
options.outputFile = 'bar'
options.maxEvents = 10 # -1 means all events

# get and parse the command line arguments
options.parseArguments()


process = cms.Process('UNCLEAN')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32( options.maxEvents )
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring() + options.inputFiles
    )

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string( options.outputFile ),
    outputCommands = cms.untracked.vstring( 'drop *' )
)

process.endpath = cms.EndPath(process.out)

#---Needed to Reconsctruct on the fly from uncleaned SCs without timing cut for slpikes
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('RecoEgamma.EgammaPhotonProducers.conversionTracks_cff')
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("RecoEcal.Configuration.RecoEcal_cff")
from Configuration.StandardSequences.Reconstruction_cff import *
from RecoEcal.Configuration.RecoEcal_cff import *
from RecoEcal.EgammaClusterProducers.hybridSuperClusters_cfi import *
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## global tag for data
process.GlobalTag.globaltag = cms.string('GR_R_42_V12::All')


## Clean PAT photons with user data   -----------------------------------------
from ElectroWeakAnalysis.MultiBosons.Skimming.egammaUserDataProducts_cff import *
basePath = "ElectroWeakAnalysis.MultiBosons.Skimming." # shorthand
process.load(basePath + "photonUserData_cfi")
process.load('PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff')

process.photonUserData.src = cms.InputTag("photons", "", "RECO")
process.patPhotons.photonSource = cms.InputTag("photons", "", "RECO")

process.patPhotons.userData.userFloats.src = egammaUserDataFloats(
    moduleName = "photonUserData"
)
process.patPhotons.userData.userInts.src = egammaUserDataInts(
    moduleName = "photonUserData"
)

## Remove MC matching by hand------------------------------------
process.patPhotons.addGenMatch = False
process.patPhotons.embedGenMatch = False
process.patPhotons.genParticleMatch = ''

#--------For Uncleaned Photon-----
process.load("RecoEcal.EgammaClusterProducers.uncleanSCRecovery_cfi")
process.uncleanSCRecovered.cleanScCollection = cms.InputTag("correctedHybridSuperClusters")
process.photonCore.scHybridBarrelProducer = cms.InputTag("uncleanSCRecovered:uncleanHybridSuperClusters")
photons.barrelEcalHits = cms.InputTag("reducedEcalRecHitsEB")
photons.endcapEcalHits = cms.InputTag("reducedEcalRecHitsEE")

from RecoEgamma.PhotonIdentification.isolationCalculator_cfi import *
newisolationSumsCalculator = isolationSumsCalculator.clone()
newisolationSumsCalculator.barrelEcalRecHitProducer = cms.string('reducedEcalRecHitsEB')
newisolationSumsCalculator.endcapEcalRecHitProducer = cms.string('reducedEcalRecHitsEE')
newisolationSumsCalculator.barrelEcalRecHitCollection = cms.InputTag('reducedEcalRecHitsEB')
newisolationSumsCalculator.endcapEcalRecHitCollection = cms.InputTag('reducedEcalRecHitsEE')

photons.isolationSumsCalculatorSet = newisolationSumsCalculator

#Sequence for ucleaned photon re-reco
process.uncleanPhotons = cms.Sequence(
               process.uncleanSCRecovered*
               process.photonSequence*
               process.photonIDSequence
               )



## Separate collection for unclean PAT photons
process.uncleanPhotonUserData = process.photonUserData.clone(
    src = cms.InputTag('photons', '', 'UNCLEAN')
)
process.uncleanPatPhotons = process.patPhotons.clone(
    photonSource = cms.InputTag("photons", "", "UNCLEAN")
)
process.uncleanPatPhotons.userData.userFloats.src = egammaUserDataFloats(
    moduleName = "uncleanPhotonUserData"
)
process.uncleanPatPhotons.userData.userInts.src = egammaUserDataInts(
    moduleName = "uncleanPhotonUserData"
)

## Build the path
process.p = cms.Path(
    process.photonUserData *
    process.patPhotons *
    process.uncleanPhotons *
    process.uncleanPhotonUserData *
    process.uncleanPatPhotons
)

process.out.outputCommands.extend([
    'keep *_*SuperClusters_*_*',
    'keep *_*photon*_*_*',
    'keep *_*Photon*_*_*',
    'keep *_reducedEcalRecHits*_*_*',
    'keep *_uncleanSCRecovered_*_*',
    'drop *_*UserData_*_*',
    ])
