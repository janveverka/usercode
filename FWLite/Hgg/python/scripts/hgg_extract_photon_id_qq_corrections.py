'''
Command-line interface to the extractor of the photon ID Q-Q Corrections.
Jan Veverka, MIT, jan.veverka@cern.ch
29 July 2013
'''

import ROOT

batch_mode = 'yes'
if batch_mode == 'yes':
    ROOT.gROOT.SetBatch(True)

import FWLite.Tools.roofit as roo
import FWLite.Hgg.photonid.qqextractor as extractor

## Defaults
varnames =  [
    'r9b', #'r9e',
    'setab', #'setae',
    'sphib', 'sphie',
    'sieieb', #'sieiee',
    #'cieipb', #'cieipe',
    #'s4ratiob', #'s4ratioe',
    ][:]

raw_name = 's12-zllm50-v7n'
#target_name = 'r12a-pho-j22-v1'
target_name = 'r12a-pho-j22-v1'
#option = 'skim10k'
option = 'noskim'
max_entries = 100000
rho = 0.9
outdir = '13-07-31/100k'

## Run!
roo.silence()
extractor.main(varnames, raw_name, target_name, option, max_entries, rho)
extractor.save_and_cleanup(outdir)

