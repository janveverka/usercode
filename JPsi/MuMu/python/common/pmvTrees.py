import os
from JPsi.MuMu.common.basicRoot import *

def getChains(files=files, path=path):
    chains = {}
    for name, flist in files.items():
        chains[name] = TChain('MuMuGammaTree/mmg')
        for f in flist:
            print 'Loading ', name, ':', f
            chains[name].Add( os.path.join(path, f) )
    return chains

path = '/raid2/veverka/PMVTrees_v5/'

files = {
  'data': 'pmvTree_ZMu-May10ReReco-42X-v3_V5.root',
  'z'   : 'pmvTree_Z-RECO-41X-v2_V5.root',
  'qcd' : 'pmvTree_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Spring11_41X-v2_V5.root',
  'w'   : 'pmvTree_WToMuNu_TuneZ2_7TeV-pythia6_Summer11_RECO_42X-v4_V5.root',
  'tt'  : 'pmvTree_TTJets_TuneZ2_7TeV-madgraph-tauola_Spring11_41X-v2_V5.root',
}


