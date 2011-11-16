import os
import socket
import JPsi.MuMu.common.clusterCorrections as clusterCorrs

from JPsi.MuMu.common.basicRoot import *

_hostname = socket.gethostname()
if _hostname == 't3-susy.ultralight.org':
    ## Path for the t3-susy
    _path = '/raid2/veverka/esTrees/'
elif _hostname == 'nbcitjv':
    ## Path for Jan's Dell Inspiron 6000 laptop
    _path = '/home/veverka/Work/data/esTrees'
elif (_hostname == 'eee.home' or
      _hostname == 'Jan-Veverkas-MacBook-Pro.local' or
      (_hostname[:8] == 'pb-d-128' and _hostname[-8:] == '.cern.ch')):
    ## Path for Jan's MacBook Pro
    _path = '/Users/veverka/Work/Data/esTrees'
else:
    raise RuntimeError, "Unknown hostname `%s'" % _hostname

_files = {}
_files['v1'] = {
    'data' : '''
            esTree_ZMu-May10ReReco-42X-v3_V1.root
            esTree_PromptReco-v4_FNAL_42X-v3_V1.root
            '''.split(),
    'z' : ['esTree_DYToMuMu_pythia6_AOD-42X-v4_V1.root'],
}

_files['v2'] = {
    ## pmvTree format
    'data' : '''
            esTree_ZMu-May10ReReco-42X-v3_V2.root
            esTree_PromptReco-v4_FNAL_42X-v3_V2.root
            '''.split(),
    'z' : ['esTree_DYToMuMu_pythia6_AOD-42X-v4_V2.root'],
    'w'    : ['esTree_WToMuNu_TuneZ2_7TeV-pythia6_Summer11_RECO_42X-v4_V2.root'],
    'tt'   : ['esTree_TTJets_TuneZ2_7TeV-madgraph-tauola_Spring11_41X-v2_V2.root'],
    'qcd'  : ['esTree_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Spring11_41X-v2_V2.root'],
}

_files['v3'] = {
    # Results with 715 / pb of June 17 up to run 166861
    'data' : [ 'esTree_V3_ZMu-May10ReReco-42X-v3.root',
               'esTree-V3_PromptReco-v4_FNAL_42X-v3.root', ],
    'z'    : [ 'esTree_V3_DYToMuMu_pythia6_v2_RECO-42X-v4.root' ],
}

_files['v4'] = {
    'data' : '''
             esTree_V4_Run2010B-ZMu-Apr21ReReco-v1.root
             esTree_V4_PromptReco-v4_FNAL_42X-v3.root
             esTree_V4_ZMu-May10ReReco-42X-v3.root
             '''.split(),
    'z'    : [ 'esTree_V4_DYToMuMu_pythia6_v2_RECO-42X-v4.root' ],
}

_files['v5'] = {
    'z'    : [ 'esTree_V5_DYToMuMu_pythia6_v2_RECO-42X-v4.root' ],
}

_files['v6'] = {
    'z'    : [ 'esTree_V6_DYToMuMu_pythia6_v2_RECO-42X-v4.root' ],
}

_files['v7'] = {
    'data' : '''
             esTree_V7_Run2010B-ZMu-Apr21ReReco-v1.root
             esTree_V7_ZMu-May10ReReco-42X-v3.root
             esTree_V7_PromptReco-v4_FNAL_42X-v3.root
             '''.split(),
    'z'    : [ 'esTree_V7_DYToMuMu_pythia6_v2_RECO-42X-v4.root' ],
}

_files['v8'] = {
    'data' : '''
             esTree_V8_05Jul2011ReReco-ECAL-v1_condor_Dimuon_RECO-42X-v9_test.root
             esTree_V8_DoubleMu_Dimuon_AOD_Aug5rereco.root
             esTree_V8_DoubleMu_Dimuon_AOD_Prompt_v6.root
             '''.split(),
    'z_test'    : '''
             esTree_V8_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9_job5_of40.root
             esTree_V8_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9_job16_of40.root
             esTree_V8_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9_job20_of40.root
             esTree_V8_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9_job31_of40.root
             esTree_V8_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9_job39_of40.root
             '''.split(),
    'z'    : '''
             esTree_V8_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9.root
             '''.split(),
}

_files['v10'] = {
    'data' : '''
             esTree_V10_DoubleMu_Run2011A-May10ReReco-v1_glite_Dimuon_RECO-42X-v9.root
             esTree_V10_DoubleMu_Run2011A-PromptReco-v4_glite_Dimuon_RECO-42X-v9.root
             '''.split(),
    'z'    : [ 'esTree_V10_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9.root' ]
}

_files['v11'] = {
    'data' : '''
             esTree_V11_DoubleMu_Run2011A-May10ReReco-v1_glite_Dimuon_RECO-42X-v9.root
             esTree_V11_DoubleMu_Run2011A-PromptReco-v4_glite_Dimuon_RECO-42X-v9.root
             '''.split(),
    'z'    : [ 'esTree_V11_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_S4-v1_condor_Dimuon_AOD-42X-v9.root' ]
}

_treeNames = {
    'v1' : 'tree/es',
    'v2' : 'pmvTree/pmv',
    'v3' : 'tree/es',
    'v4' : 'tree/pmv',
    'v5' : 'tree/pmv',
    'v6' : 'tree/pmv',
    'v7' : 'tree/pmv',
    'v8' : 'tree/pmv',
    'v10' : 'tree/pmv',
    'v11' : 'tree/pmv',
}


def getChains(version='v4'):
    chains = {}
    for name, flist in _files[version].items():
        chains[name] = TChain( _treeNames[version] )
        for f in flist:
            print "Loading ", name, ":", f
            chains[name].Add( os.path.join(_path, f) )

    ## Set aliases
    for ch in chains.values():
        ch.SetAlias( 'phoE', 'phoPt * cosh(phoEta)' )
        ch.SetAlias( 'brem', 'scPhiWidth / scEtaWidth' )
        ch.SetAlias( 'rawE', 'scRawE + preshowerE' )
        ch.SetAlias( 'corrE', 'phoCrackCorr * corrE(rawE, scEta, brem)' )
        ch.SetAlias( 'newCorrE', 'phoCrackCorr * newCorrE(rawE, scEta, brem)' )
        ch.SetAlias( 'corrKRatio', 'phoE * kRatio / corrE' )
        ch.SetAlias( 'newCorrKRatio', 'phoE * kRatio / newCorrE' )
        ch.SetAlias('m1gMass',
                    'sqrt(2*mu1Pt*phoPt*(cosh(mu1Eta - phoEta) - cos(mu1Phi - phoPhi)))')
        ch.SetAlias('m2gMass',
                    'sqrt(2*mu2Pt*phoPt*(cosh(mu2Eta - phoEta) - cos(mu2Phi - phoPhi)))')

    return chains

if __name__ == "__main__":
    import user

