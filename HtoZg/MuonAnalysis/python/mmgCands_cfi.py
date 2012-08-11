import FWCore.ParameterSet.Config as cms

mmgCands = cms.EDProducer('CandViewShallowClonePtrCombiner',
    checkCharge = cms.bool(False),
    cut = cms.string('''
        min(deltaR(daughter("dimuon").daughter(0).eta,
                   daughter("dimuon").daughter(0).phi,
                   daughter("photon").eta,
                   daughter("photon").phi),
            deltaR(daughter("dimuon").daughter(1).eta,
                   daughter("dimuon").daughter(1).phi,
                   daughter("photon").eta,
                   daughter("photon").phi)) > 0.4
        '''),
    decay = cms.string("isolatedDimuons loosePhotons"),
    roles = cms.vstring("dimuon", "photon")
    )
