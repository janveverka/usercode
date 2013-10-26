'''
Command-line interface to the extractor of the photon ID Q-Q Corrections.
Jan Veverka, MIT, jan.veverka@cern.ch
29 July 2013
'''
#batch_mode = 'yes'
batch_mode = 'no'

import sys

if batch_mode == 'yes':
	sys.argv.append('-b-')

import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Hgg.photonid.qqextractor as extractor

## Defaults
varnames = [
    'r9b', #'r9e',
    #'setab', #'setae',
    #'sphib', 'sphie',
    #'sieieb', #'sieiee',
    #'cieipb', #'cieipe',
    #'s4ratiob', #'s4ratioe',
    ][:]

raw_name = 's12-zllm50-v7n'
#target_name = 'r12a-pho-j22-v1'
target_name = 'r12a-pho-j22-v1'
## Use on MacBook
option = 'skim10k'
#option = 'noskim'
max_entries = -1
prescale = 1
prescale_phase = 0
rho = 0.9
outdir = 'prescale_%dof%d' % (prescale_phase, prescale)

## Run!
roo.silence()
extractor.main(
	varnames=varnames, 
	raw_name=raw_name, 
	target_name=target_name, 
	option=option, 
	max_entries=max_entries, 
	prescale=prescale,
	prescale_phase=prescale_phase,
	rho=rho)
extractor.save_and_cleanup(outdir)

