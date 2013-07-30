'''
Provides photon trees given their name.  Adjusts path on different hosts
automatically.
Jan Veverka, MIT, jan.veverka@cern.ch
29 July 2013
'''
import os
import socket
import ROOT

analysis = 'hgg-2013Final8TeV_ID'

host_to_base_dir = {
    'Jan-Veverkas-MacBook-Pro.local': '/Users/veverka/Work/Data',
    't3btch000.mit.edu': '/home/mingyang/cms/hist'
    }
    
host_base = socket.gethostname()
if 't3btch' in host_base:
    host_base = 't3btch000.mit.edu'
base_dir = host_to_base_dir[host_base]

open_files = []

#______________________________________________________________________________
def get(name, option='noskim'):
    '''
    Returns the tree corresponding to the given name.
    '''
    supported_names = '''
        r12a-pho-j22-v1
        r12b-dph-j22-v1
        r12c-dph-j22-v1
        r12d-dph-j22-v1
        s12-h110gg-gf-v7n
        s12-h124gg-gf-v7n
        s12-h140gg-gf-v7n
        s12-pj20_40-2em-v7n
        s12-pj40-2em-v7n
        s12-zllm50-v7n
        '''.split()
    #print supported_names
    #name_is_supported = False
    #for sname in supported_names:
        #if name == sname:
            #name_is_supported = True
            #print name, '==', sname
        #else:
            #print name, '<>', sname
    #if not name_is_supported:
    if not name in supported_names:
        raise RuntimeError, name + " not supported!"
    file_name = analysis + '_' + name + '_' + option + '.root'
    last_dir = 'merged'
    if 'skim10k' in option:
        last_dir = 'skimmed'        
    source = os.path.join(base_dir, analysis, last_dir, file_name)
    infile = ROOT.TFile.Open(source)
    open_files.append(infile)
    tree_name = get_tree_name(option)
    tree = infile.Get(tree_name)
    if not tree:
        raise RuntimeError, 'No %s in %s!' % (tree_name, source)
    return tree
## End of get(name)


#______________________________________________________________________________
def get_tree_name(option):
    if 'skim' == option[0:4]:
        return 'hPhotonTree'
    else:
        return '/'.join([
            'RunLumiSelectionMod',
            'MCProcessSelectionMod',
            'HLTModP',
            'GoodPVFilterMod',
            'JetPub',
            'JetCorrectionMod',
            'SeparatePileUpMod',
            'ElectronIDMod',
            'MuonIDMod',
            'PhotonPairSelectorPreselInvertEleVetoNoSmear',
            'PhotonTreeWriterPreselInvertEleVetoNoSmear',
            'hPhotonTree',
            ])
## End of get_tree_name(option)


#______________________________________________________________________________
def close_files():
    '''
    Calls the `Close()' method for all files in the `open_files' list.
    '''
    for infile in open_files:
        infile.Close()
## End of close_files()
