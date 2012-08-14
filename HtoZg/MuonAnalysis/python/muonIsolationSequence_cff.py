'''
Includes particle-based isolation to reco muon in 42x.
Inspired by
http://lotus.phys.northwestern.edu/~stoyan/work/DY_stuff/2012/PF_isoCode_42X/
Jan Veverka, Caltech
14 August, 2012
'''
import FWCore.ParameterSet.Config as cms

from CommonTools.ParticleFlow.Isolation.tools_cfi import isoDepositReplace
from HtoZg.CommonAnalysis.tools import ensure_labels

isoDepMuonWithCharged = isoDepositReplace('muons', 'pfAllChargedHadronsPFlow')
isoDepMuonWithNeutral = isoDepositReplace('muons', 'pfAllNeutralHadronsPFlow')
isoDepMuonWithPhotons = isoDepositReplace('muons', 'pfAllPhotonsPFlow')

isoValMuonWithCharged = cms.EDProducer("CandIsolatorFromDeposits",
    deposits = cms.VPSet(cms.PSet(
        src = cms.InputTag("isoDepMuonWithCharged"),
        deltaR = cms.double(0.4),
        weight = cms.string('1'),
        vetos = cms.vstring(),
        skipDefaultVeto = cms.bool(True),
        mode = cms.string('sum')
    ))
)   

isoValMuonWithNeutral = cms.EDProducer("CandIsolatorFromDeposits",
    deposits = cms.VPSet(cms.PSet(
        src = cms.InputTag("isoDepMuonWithNeutral"),
        deltaR = cms.double(0.4),
        weight = cms.string('1'),
        vetos = cms.vstring('Threshold(0.5)'),
        skipDefaultVeto = cms.bool(True),
        mode = cms.string('sum')
    ))
)

isoValMuonWithPhotons = cms.EDProducer("CandIsolatorFromDeposits",
    deposits = cms.VPSet(cms.PSet(
        src = cms.InputTag("isoDepMuonWithPhotons"),
        deltaR = cms.double(0.4),
        weight = cms.string('1'),
        vetos = cms.vstring('Threshold(0.5)'),
        skipDefaultVeto = cms.bool(True),
        mode = cms.string('sum')
    ))
)

ensure_labels(locals())

muonIsolationSequence = cms.Sequence(
    isoDepMuonWithCharged + 
    isoDepMuonWithNeutral + 
    isoDepMuonWithPhotons +
    isoValMuonWithCharged + 
    isoValMuonWithNeutral + 
    isoValMuonWithPhotons
    )


if __name__ == '__main__':
    import user