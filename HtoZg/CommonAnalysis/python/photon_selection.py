'''
Gives expression string that defines photon selection.
'''

## These are photons that pass all the cuts for the Loose 
## Cut-Based ID for non-triggering photons [1] that
## can be implemented by the string parser. 
## [1] https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedPhotonID2012
##     Revision: r8
##     Accessed: 11 Aug 2012, 04:45 CEST.

## FIXME: Add H/E cut.
cutbased_id_loose_2011 = '''
    (
        (
            isEB &&
            userInt("conversionTools:passElectronVeto") > 0 &&
            sigmaIetaIeta < 0.012 &&
            userFloat("photonIsolation:pfChargedHadronRhoCorrected") < 2.6 &&
            userFloat("photonIsolation:pfNeutralHadronRhoCorrected") 
                < 3.5 + 0.04 * pt &&
            userFloat("photonIsolation:pfPhotonRhoCorrected") 
                < 1.3 + 0.005 * pt
        ) ||
        (  
            !isEB &&
            abs(eta) < 2.4 &&
            userInt("conversionTools:passElectronVeto") > 0 &&
            sigmaIetaIeta < 0.034 &&
            userFloat("photonIsolation:pfChargedHadronRhoCorrected") < 2.3 &&
            userFloat("photonIsolation:pfNeutralHadronRhoCorrected") 
                < 2.9 + 0.04 * pt
        )
    )
    '''

cutbased_id_loose_2012 = '''
    (
        (
            isEB &&
            userInt("conversionTools:passElectronVeto") > 0 &&
            hadTowOverEm < 0.05 &&
            sigmaIetaIeta < 0.012 &&
            userFloat("photonIsolation:pfChargedHadronRhoCorrected") < 2.6 &&
            userFloat("photonIsolation:pfNeutralHadronRhoCorrected") 
                < 3.5 + 0.04 * pt &&
            userFloat("photonIsolation:pfPhotonRhoCorrected") 
                < 1.3 + 0.005 * pt
        ) ||
        (  
            !isEB &&
            abs(eta) < 2.4 &&
            userInt("conversionTools:passElectronVeto") > 0 &&
            hadTowOverEm < 0.05 &&
            sigmaIetaIeta < 0.034 &&
            userFloat("photonIsolation:pfChargedHadronRhoCorrected") < 2.3 &&
            userFloat("photonIsolation:pfNeutralHadronRhoCorrected") 
                < 2.9 + 0.04 * pt
        )
    )
    '''

htozg_id = cutbased_id_loose_2011