import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA1")

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
"file:/uscms_data/d1/stoyan/data/tmp/diMuonSkim_massAbove570_reReco_AOD.root",
"file:/uscms_data/d1/stoyan/data/tmp/diMuonSkim_massAbove570_prompt_AOD.root"
),
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(30) 
)


#------------------------------------------
# Load standard sequences.
#------------------------------------------
#process.load('Configuration/StandardSequences/MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load('Configuration/StandardSequences/GeometryIdeal_cff')


process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'GR_R_42_V20::All'



######### PF
# load the PAT config
process.load("PhysicsTools.PatAlgos.patSequences_cff")

## Output Module Configuration (expects a path 'p')
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent
process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('patTuple.root'),
                               # save only events passing the full path
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
                               # save PAT Layer 1 output; you need a '*' to
                               # unpack the list of commands 'patEventContent'
                               outputCommands = cms.untracked.vstring('drop *', *patEventContent )
                               )

# Configure PAT to use PF2PAT instead of AOD sources
# this function will modify the PAT sequences. 
from PhysicsTools.PatAlgos.tools.pfTools import *

postfix = "PFlow"
jetAlgo="AK5"
runOnMC = False
usePF2PAT(process,runPF2PAT=True, jetAlgo=jetAlgo, runOnMC=runOnMC, postfix=postfix)
# to use tau-cleaned jet collection uncomment the following:
#getattr(process,"pfNoTau"+postfix).enable = True

# to switch default tau to HPS tau uncomment the following:
#adaptPFTaus(process,"hpsPFTau",postfix=postfix)
if runOnMC == False:
    # removing MC matching for standard PAT sequence
    # for the PF2PAT+PAT sequence, it is done in the usePF2PAT function
    removeMCMatchingPF2PAT( process, '' ) 

# top projections in PF2PAT:
getattr(process,"pfNoPileUp"+postfix).enable = True

# verbose flags for the PF2PAT modules
getattr(process,"pfNoMuon"+postfix).verbose = False
process.pfIsolatedMuonsPFlow.isolationCuts   = cms.vdouble(9999.,9999.,9999.)
process.pfIsolatedMuonsPFlow.combinedIsolationCut = cms.double(9999.)
getattr(process,"pfNoMuon"+postfix).enable = False
getattr(process,"pfNoElectron"+postfix).enable = False
getattr(process,"pfNoTau"+postfix).enable = False
getattr(process,"pfNoJet"+postfix).enable = False



#########

#to include particle-based isolation to reco muon
from CommonTools.ParticleFlow.Isolation.tools_cfi import *  # for 4_2_x version 

process.isoDepMuonWithCharged   = isoDepositReplace( 'muons', 'pfAllChargedHadronsPFlow' )
process.isoDepMuonWithNeutral   = isoDepositReplace( 'muons', 'pfAllNeutralHadronsPFlow' )
process.isoDepMuonWithPhotons   = isoDepositReplace( 'muons', 'pfAllPhotonsPFlow' )

process.isoValMuonWithCharged = cms.EDProducer("CandIsolatorFromDeposits",
    deposits = cms.VPSet(cms.PSet(
        src = cms.InputTag("isoDepMuonWithCharged"),
        deltaR = cms.double(0.4),
        weight = cms.string('1'),
        vetos = cms.vstring(),
        skipDefaultVeto = cms.bool(True),
        mode = cms.string('sum')
    ))
)   

process.isoValMuonWithNeutral = cms.EDProducer("CandIsolatorFromDeposits",
    deposits = cms.VPSet(cms.PSet(
        src = cms.InputTag("isoDepMuonWithNeutral"),
        deltaR = cms.double(0.4),
        weight = cms.string('1'),
        vetos = cms.vstring('Threshold(0.5)'),
        skipDefaultVeto = cms.bool(True),
        mode = cms.string('sum')
    ))
)

process.isoValMuonWithPhotons = cms.EDProducer("CandIsolatorFromDeposits",
    deposits = cms.VPSet(cms.PSet(
        src = cms.InputTag("isoDepMuonWithPhotons"),
        deltaR = cms.double(0.4),
        weight = cms.string('1'),
        vetos = cms.vstring('Threshold(0.5)'),
        skipDefaultVeto = cms.bool(True),
        mode = cms.string('sum')
    ))
)

process.patMuons.isoDeposits = cms.PSet(
       pfNeutralHadrons = cms.InputTag("isoDepMuonWithNeutral"),
       pfChargedHadrons = cms.InputTag("isoDepMuonWithCharged"),
       pfPhotons = cms.InputTag("isoDepMuonWithPhotons")
)

process.patMuons.isolationValues = cms.PSet(
       pfNeutralHadrons = cms.InputTag("isoValMuonWithNeutral"),
       pfChargedHadrons = cms.InputTag("isoValMuonWithCharged"),
       pfPhotons = cms.InputTag("isoValMuonWithPhotons")
)


##



#process.muonAna = cms.EDFilter( "MuonAna",
    #isMC = cms.untracked.bool(False),
    #isAOD = cms.untracked.bool(True),
    #rootFileName = cms.untracked.string("muonHists_data.root"),
##    printout_NEvents = cms.untracked.uint32(50000), 
##    hltName = cms.untracked.string("REDIGI36X"),
    #l1GtRecordInputTag = cms.InputTag('gtDigis' ), 
    #lookAtL1Triggers = cms.untracked.bool(False),
    #lookAtHLTTriggers = cms.untracked.bool(True),
    #muonTag        = cms.InputTag("muons"),
    #applyFullSelection = cms.untracked.bool(False),
    #useAlignedSegmentsOnly = cms.untracked.bool(False),
    #onlyNegativeY_alignedS = cms.untracked.bool(False),
    #applyTrigger = cms.untracked.bool(False),
##    triggersToApply = cms.vstring("HLT_Mu15","HLT_Mu20","HLT_Mu24","HLT_Mu30"),
    #triggersToApply = cms.vstring("HLT_DoubleMu6","HLT_DoubleMu7","HLT_Mu13_Mu8"),
    #triggersToInvestigate_1 = cms.vstring("HLT_DoubleMu6","HLT_DoubleMu7","HLT_Mu13_Mu8"),
    #triggersToInvestigate_2 = cms.vstring("HLT_Mu15","HLT_Mu20","HLT_Mu24","HLT_Mu30"),
    #applyArbitration = cms.untracked.bool(False),
    #applyIsolation = cms.untracked.bool(False),
##    relIso_cut = cms.untracked.double(0.15),
    #relIso_cut = cms.untracked.double(0.2),
    #useISOcorrection = cms.untracked.bool(False),
    #usePF_relISO = cms.untracked.bool(True),
    #applyDepth = cms.untracked.bool(False),
    #qualityTR = cms.untracked.bool(False),
    #qualitySTA = cms.untracked.bool(False),     
    #apply_dxy_cut = cms.untracked.bool(True),
    #apply_p_cut = cms.untracked.bool(False),
    #apply_pt_cut = cms.untracked.bool(True),
    #pt_cut = cms.untracked.double(14.0),
    #pt_cut_2 = cms.untracked.double(9.0),
    #apply_eta_cut = cms.untracked.bool(True),
    #eta_cut = cms.untracked.double(2.4),
    #eta_cut_2 = cms.untracked.double(2.4),
    #doTrackCollections = cms.untracked.bool(False),
    #matchMuTrigger = cms.untracked.bool(True),
    #doSingleMuons = cms.untracked.bool(False)
##    doTandPefficiencies = cms.untracked.bool(False)
#)

#process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange(
#)

#### the path
process.p = cms.Path(getattr(process,"patPF2PATSequence"+postfix)*
   process.isoDepMuonWithCharged*
   process.isoDepMuonWithNeutral*
   process.isoDepMuonWithPhotons*
   process.isoValMuonWithNeutral*
   process.isoValMuonWithCharged*
   process.isoValMuonWithPhotons*
   process.patDefaultSequence
   #process.muonAna
   )

#### output 
process.outS = cms.OutputModule(
    "PoolOutputModule",
    outputCommands = cms.untracked.vstring('keep *','drop *_MEtoEDMConverter_*_*'),
    fileName = cms.untracked.string("/uscms_data/d1/stoyan/data/tmp/dataSkim.root"),
    dataset = cms.untracked.PSet(
      dataTier = cms.untracked.string('RECO'),
      filterName = cms.untracked.string('Skim')
    ),
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p'))
#    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('mySkim'))
)
#process.outpath = cms.EndPath(process.outS)
#process.outpath = cms.EndPath(process.outputSkim)