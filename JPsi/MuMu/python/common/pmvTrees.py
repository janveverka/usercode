import os
import socket
from JPsi.MuMu.common.basicRoot import *

_hostname = socket.gethostname()
if _hostname == 't3-susy.ultralight.org':
    ## Path for the t3-susy
    _path = {
        'v5' : '/raid2/veverka/PMVTrees_v5',
        'v9' : '/raid2/veverka/pmvTrees/',
        'v10': '/raid2/veverka/pmvTrees/',
        'v11': '/raid2/veverka/pmvTrees/',
        'v12': '/raid2/veverka/pmvTrees/',
    }
elif _hostname == 'nbcitjv':
    ## Path for Jan's Dell Inspiron 6000 laptop
    _path = {
        'v5': '/home/veverka/Work/data/PMVTrees_v5',
        'v9' : '/home/veverka/Work/data/pmvTrees',
        'v10': '/home/veverka/Work/data/pmvTrees',
        'v11': '/home/veverka/Work/data/pmvTrees',
        'v12': '/home/veverka/Work/data/pmvTrees',
    }
elif _hostname == 'eee.home' or _hostname == 'Jan-Veverkas-MacBook-Pro.local':
    ## Path for Jan's MacBook Pro
    _path = {
        'v9' : '/Users/veverka/Work/Data/pmvTrees',
        'v10': '/Users/veverka/Work/Data/pmvTrees',
        'v11': '/Users/veverka/Work/Data/pmvTrees',
        'v12': '/Users/veverka/Work/Data/pmvTrees',
    }
else:
    raise RuntimeError, "Unknown hostname `%s'" % _hostname


_files = {}

_files['v5'] = {
    'data': ['pmvTree_ZMu-May10ReReco-42X-v3_V5.root'],
    'z'   : ['pmvTree_Z-RECO-41X-v2_V5.root'],
    'qcd' : ['pmvTree_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Spring11_41X-v2_V5.root'],
    'w'   : ['pmvTree_WToMuNu_TuneZ2_7TeV-pythia6_Summer11_RECO_42X-v4_V5.root'],
    'tt'  : ['pmvTree_TTJets_TuneZ2_7TeV-madgraph-tauola_Spring11_41X-v2_V5.root'],
}

_files['v9'] = {
    'data' : [ 'pmvTree_V9_Run2010B-ZMu-Apr21ReReco-v1.root',
              'pmvTree_V9_ZMu-May10ReReco-42X-v3.root',
              'pmvTree_V9_PromptReco-v4_FNAL_42X-v3.root', ],
    'data2011' : [ 'pmvTree_V9_ZMu-May10ReReco-42X-v3.root',
                   'pmvTree_V9_PromptReco-v4_FNAL_42X-v3.root', ],
    'z'    : [ 'pmvTree_V9_DYToMuMu_pythia6_v2_RECO-42X-v4.root' ],
    'qcd'  : [ 'pmvTree_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Spring11_41X-v2_V6.root' ],
    'w'    : [ 'pmvTree_WToMuNu_TuneZ2_7TeV-pythia6_Summer11_RECO_42X-v4_V6.root' ],
    'tt'   : [ 'pmvTree_TTJets_TuneZ2_7TeV-madgraph-tauola_Spring11_41X-v2_V6.root' ],
}

_files['v10'] = {
    'gj' : [ 'pmvTree_V10_G_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6_' + \
                'S4-v1_condor_Inclusive_AOD-42X-v9.root' ],
}

_files['v11'] = {
    'z' : [ 'pmvTree_V11_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_' + \
                'S4-v1_condor_Dimuon_AOD-42X-v9.root' ],
}

_files['v12'] = {
    'z' : ['pmvTree_V12_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_' +\
           'S4-v1_condor_Dimuon_AOD-42X-v9.root' ],
    'z1' : ['pmvTree_V12_DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia_' +\
           'S4-v1_condor_Dimuon_AOD-42X-v9_1.root' ],
    'gj': [ 'pmvTree_V12_G_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6_' +\
                'S4-v1_condor_Inclusive_AOD-42X-v9.root' ],
}

_treeNames = {
    'v5' : 'pmvTree/pmv',
    'v9' : 'pmvTree/pmv',
    'v10': 'pmvTree/pmv',
    'v11': 'pmvTree/pmv',
    'v12': 'pmvTree/pmv',
}

#------------------------------------------------------------------------------
def getChains(version='v9'):
    'Given a version string returns a dictionary of name:TChain.'
    chains = {}
    for name, flist in _files[version].items():
        chains[name] = TChain( _treeNames[version] )
        for f in flist:
            print "Loading ", name, ":", f
            chains[name].Add( os.path.join(_path[version], f) )
    return chains
# getChains <--

## Enable tab completion and history during interactive inspection
if __name__ == "__main__": import user
