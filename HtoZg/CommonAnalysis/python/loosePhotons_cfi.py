import FWCore.ParameterSet.Config as cms

## These are photons that pass all the cuts for the Loose 
## Cut-Based ID for non-triggering photons [1] that
## can be implemented by the string parser. 
## [1] https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedPhotonID2012
##     Revision: r8
##     Accessed: 11 Aug 2012, 04:45 CEST.

loosePhotons = cms.EDFilter('PATPhotonSelector',
    src = cms.InputTag('selectedPatPhotons'),
    cut = cms.string('''
        (isEB &&
         hadTowOverEm < 0.05 &&
         sigmaIetaIeta < 0.012 &&
         userFloat("photonIsolation:pfChargedHadronRhoCorrected") < 2.6 &&
         userFloat("photonIsolation:pfNeutralHadronRhoCorrected") 
             < 3.5 + 0.04 * pt &&
         userFloat("photonIsolation:pfPhotonRhoCorrected") 
             < 1.3 + 0.005 * pt
         ) ||
        (!isEB &&
         hadTowOverEm < 0.05 &&
         sigmaIetaIeta < 0.034 &&
         userFloat("photonIsolation:pfChargedHadronRhoCorrected") < 2.3 &&
         userFloat("photonIsolation:pfNeutralHadronRhoCorrected") 
             < 2.9 + 0.04 * pt
         )
        '''),
    filter = cms.bool(True)                                
    )

