from JPsi.MuMu.common.basicRoot import *
import os

path = '/raid2/veverka/esTrees/'

files = {
    'data' : '''
             esTree_ZMu-May10ReReco-42X-v3_V1.root
             esTree_PromptReco-v4_FNAL_42X-v3_V1.root
             '''.split(),
    'z' : ['esTree_DYToMuMu_pythia6_AOD-42X-v4_V1.root'],
}

def getChains(files=files, path=path):
    chains = {}
    for name, flist in files.items():
        chains[name] = TChain("tree/es")
        for f in flist:
            print "Loading ", name, ":", f
            chains[name].Add( os.path.join(path, f) )
    return chains

if __name__ == "__main__": import user

