'''
Command-line interface to the extractor of the photon ID Q-Q Corrections.
Jan Veverka, MIT, jan.veverka@cern.ch
29 July 2013
'''

## Defaults
varnames = 'r9b sieieb setab'.split()
raw_name = 's12-zllm50-v7n'
target_name = 'r12a-pho-j22-v1'
#option = 'skim10k'
option = 'noskim'
max_entries = 1000
outdir = 'qqplots'
batch_mode = 'yes'

import ROOT

if batch_mode == 'yes':
    ROOT.gROOT.SetBatch(True)

import FWLite.Hgg.photonid.qqextractor as extractor

## Run!
extractor.main(varnames, raw_name, target_name, option, max_entries)
extractor.save_and_cleanup(outdir)

