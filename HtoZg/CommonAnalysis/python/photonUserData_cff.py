import FWCore.ParameterSet.Config as cms

photonUserFloats = []
photonUserInts = []

## Photon isolation variables
for x in '''rho
            chargedHadronEA
            neutralHadronEA
            photonEA
            pfChargedHadron
            pfNeutralHadron
            pfPhoton
            pfChargedHadronRhoCorrected
            pfNeutralHadronRhoCorrected
            pfPhotonRhoCorrected'''.split():
    photonUserFloats.append(cms.InputTag('photonIsolation', x))

## Photon conversion tools variables
photonUserFloats.append(cms.InputTag('conversionTools', 'deltaRToTrack'))

for x in 'passElectronVeto hasMatchedConversion'.split():
    photonUserInts.append(cms.InputTag('conversionTools', x))
