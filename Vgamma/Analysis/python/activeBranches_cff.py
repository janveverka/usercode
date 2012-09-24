'''
Defines cms.vstring activeBranches that holds a list of regular expressions
matching names of VgAnalyzerTree branches that will be active in the
VgAnalyzer, i.e. their status will be set to 1 and they will be added 
to the cache.
'''

import FWCore.ParameterSet.Config as cms

activeMuonBranches = cms.vstring('''
    nMu
    muEta
    muPhi
    muCharge
    muPt
    muType
    muIsoTrk
    muIsoEcal
    muIsoHcal
    muChi2NDF
    muNumberOfValidMuonHits
    muStations
    muPVD0
    muPVDz
    muNumberOfValidPixelHits
    muNumberOfValidTrkHits
    '''.split()
    )

activePhotonBranches = cms.vstring('''
    nPho
    phoEta
    phoPhi
    phoEt
    phoSCEta
    phoTrkIsoHollowDR04
    phoEcalIsoDR04
    phoHcalIsoDR04
    phoHoverE
    phohasPixelSeed
    phoSigmaIEtaIEta
    phoSigmaIPhiIPhi
    phoR9
    '''.split()
    )

activePileupBranches = cms.vstring('rho', 'rhoNeutral')

activeBranchesData = cms.vstring()
activeBranchesData.extend(activeMuonBranches)
activeBranchesData.extend(activePhotonBranches)
activeBranchesData.extend(activePileupBranches)

activeBranchesMC = activeBranchesData + ['nPU']
