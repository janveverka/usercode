import FWCore.ParameterSet.Config as cms

photonUserFloats = []

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
