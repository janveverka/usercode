import FWCore.ParameterSet.Config as cms
import HLTrigger.HLTfilters.hltHighLevel_cfi

hltFilter = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
hltFilter.throw = cms.bool(False)
hltFilter.HLTPaths = '''
    HLT_Mu17_Mu8_v*
    HLT_Mu17_TkMu8_v*
    HLT_Mu22_Mu8_v*
    HLT_Mu22_TkMu8_v*
    HLT_IsoMu24_eta2p1_v*
    HLT_IsoMu24_v*
    '''.split()
