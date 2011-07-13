from JPsi.MuMu.common.basicRoot import *
import os
import socket

_hostname = socket.gethostname()
if _hostname == 't3-susy.ultralight.org':
    ## Path for the t3-susy
    _path = '/raid2/veverka/esTrees/'
elif _hostname == 'nbcitjv':
    ## Path for Jan's Dell Inspiron 6000 laptop
    _path = '/home/veverka/Work/data/esTrees'
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



_treeNames = {
    'v1' : 'tree/es',
    'v2' : 'pmvTree/pmv',
    'v3' : 'tree/es',
    'v4' : 'tree/pmv',
    'v5' : 'tree/pmv',
    'v6' : 'tree/pmv',
    'v7' : 'tree/pmv',
}


def getChains(version='v4'):
    chains = {}
    for name, flist in _files[version].items():
        chains[name] = TChain( _treeNames[version] )
        for f in flist:
            print "Loading ", name, ":", f
            chains[name].Add( os.path.join(_path, f) )
    return chains

if __name__ == "__main__": import user

