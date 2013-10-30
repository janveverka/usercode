# -*- coding: utf-8 -*-
'''
Command-line interface to the extractor of the photon ID Q-Q Corrections.
Jan Veverka, MIT, jan.veverka@cern.ch
29 July 2013
'''
batch_mode = 'yes'
#batch_mode = 'no'

import socket
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
target_name = 'r12b-dph-j22-v1'
#raw_names = ['s12-zllm50-v7n']
#target_names = [
    #'r12a-pho-j22-v1',
    #'r12b-dph-j22-v1',
    #]
max_entries = 1000
prescale = 1
prescale_phase = 0
rho = 0.9
outdir = 'prescale_%dof%d' % (prescale_phase, prescale)

## Choose the option automatically based on the hostname
option_for_host = {
    'Jan-Veverkas-MacBook-Pro.local': 'skim10k',
    't3btch000.mit.edu'             : 'noskim',
    }
host = socket.gethostname()
if 't3btch' in host:
    host = 't3btch000.mit.edu'
option = option_for_host[host]


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

