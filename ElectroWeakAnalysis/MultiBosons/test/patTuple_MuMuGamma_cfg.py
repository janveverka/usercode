# This is an example PAT configuration showing the usage of PAT on full sim samples

# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# note that you can use a bunch of core tools of PAT
# to taylor your PAT configuration; for a few examples
# uncomment the following lines

from PhysicsTools.PatAlgos.tools.coreTools import *
removeCleaning(process)
#restrictInputToAOD(process)
#removeMCMatching(process, 'Muons')
#removeAllPATObjectsBut(process, ['Muons'])
#removeSpecificPATObjects(process, ['Electrons', 'Muons', 'Taus'])

#switch off new tau features introduced in 33X to restore 31X defaults
# new feaures: - shrinkingConeTaus instead of fixedCone ones
#              - TaNC discriminants attached for shrinkingConeTaus
#              - default preselection on cleaningLayer1
from PhysicsTools.PatAlgos.tools.tauTools import *
switchTo31Xdefaults(process)

# run the 3.3.x software on Summer 09 MC from 3.1.x:
#   - change the name from "ak" (3.3.x) to "antikt) (3.1.x)
#   - run jet ID (not run in 3.1.x)
# this apparently also works for 3.4.2 ...
from PhysicsTools.PatAlgos.tools.jetTools import *
addJetID(process,
         jetSrc = cms.InputTag("antikt5CaloJets"),
         jetIdTag = "antikt5"
        )
# in PAT (iterativeCone5) to ak5 (anti-kt cone = 0.5)
switchJetCollection(process,
                    cms.InputTag('antikt5CaloJets'),
                    doJTA            = True,
                    doBTagging       = True,
                    jetCorrLabel     = ('AK5','Calo'),
                    doType1MET       = True,
                    genJetCollection = cms.InputTag("antikt5GenJets"),
                    doJetID          = True,
                    jetIdLabel       = "antikt5"
                   )

# load the photonTools of PAT
from PhysicsTools.PatAlgos.tools.photonTools import *
addPhotonUserIsolation(process)


# let it run
process.p = cms.Path(
    process.patDefaultSequence
    )

# In addition you usually want to change the following parameters:

process.GlobalTag.globaltag =  'MC_3XY_V25::All'    ##  (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
pathPrefix = 'rfio:/castor/cern.ch/user/v/veverka/mc/Summer09/Zmumu_MC_31X_V3_7TeV-v1/GEN-SIM-RECO/test/'
process.source.fileNames = [
   pathPrefix + 'GEN-SIM-RECO_test.root'
   ]
# process.maxEvents.input = 3         ##  (e.g. -1 to run on all events)
#process.maxEvents.input = -1
##  (e.g. 10 to produce 10 events)
process.maxEvents = cms.untracked.PSet( output = cms.untracked.int32(10) )

## output file v3: adding genParticles
## output file v4: moving to CMSSW_3_5_4
## output file v5: adding reco photons, photonCore, conversions and trackerOnlyConverstions
## output file v6: added superclusters
#process.out.fileName = pathPrefix + 'PATLayer1_Output.fromAOD_full_v4.root'            ##  (e.g. 'myTuple.root')
process.out.fileName = 'PATLayer1_Output.fromAOD_full_v6.root'            ##  (e.g. 'myTuple.root')

process.out.outputCommands += [ 'keep recoGenParticles_genParticles_*_*', ## Keeps the MC objects for references
  'keep *_photons_*_*',
  'keep *_photonCore_*_*',
  'keep *_conversions_*_*',
  'keep *_trackerOnlyConversions_*_*',
  'keep *_ckfInOutTracksFromConversions_*_*',
  'keep *_ckfOutInTracksFromConversions_*_*',
  'keep *_*5x5SuperClusters*_*_*',
  'keep *_multi5x5BasicClusters_*Endcap*_*',
  'keep *_hybridSuperClusters_*_*',
  'keep *_correctedHybridSuperClusters_*_*',
]

process.options.wantSummary = False        ##  (to suppress the long output at the end of the job)
process.selectedPatMuons.cut = 'pt > 10 && abs(eta) < 2.5'
process.countPatMuons.minNumber = 2
process.countPatPhotons.minNumber = 1
# from EWK dimuon skim
process.muonMatch.maxDeltaR = 0.15
process.muonMatch.maxDPtRel = 1.0
process.muonMatch.resolveAmbiguities = True
process.muonMatch.resolveByMatchQuality = True
