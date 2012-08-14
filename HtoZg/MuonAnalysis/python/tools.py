'''
Tools to facilitate configuration sequence building.

Jan Veverka, Caltech
14 August 1977
'''
import FWCore.ParameterSet.Config as cms
from PhysicsTools.PatAlgos.tools.pfTools import usePF2PAT

##_____________________________________________________________________________
def add_muon_isolation(process):
    '''
    Adds the PF isolation for muons in 42x
    '''
    ## Configure PAT to use PF2PAT instead of AOD sources
    ## this function will modify the PAT sequences.     
    usePF2PAT(process, runPF2PAT=True, jetAlgo='AK5', 
              runOnMC=False, postfix='PFlow')
    ## Top projections in PF2PAT
    process.pfNoPileUp.enable = True
    ## verbose flags for the PF2PAT modules
    process.pfNoMuonPFlow.verbose = False

    process.pfIsolatedMuonsPFlow.isolationCuts   = cms.vdouble(9999., 9999.,
                9999.)
    process.pfIsolatedMuonsPFlow.combinedIsolationCut = cms.double(9999.)
    process.pfNoMuonPFlow.enable = False
    process.pfNoElectronPFlow.enable = False
    process.pfNoTauPFlow.enable = False
    process.pfNoJetPFlow.enable = False
    
    ## Load the sequence that calculates the isolations using the PAT PFlow 
    process.load('HtoZg.MuonAnalysis.muonIsolationSequence_cff')

    ## Include the pf isolations in the default PAT muons
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

    
    ## Prepend the calculation of the muon isolation before PAT
    process.patSequence = cms.Sequence(process.patPF2PATSequencePFlow + 
                                       process.muonIsolationSequence + 
                                       process.patSequence)
## End of add_muon_isolation
