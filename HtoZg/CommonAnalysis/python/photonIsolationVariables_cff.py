'''
Defines a configuration fragment that can be used as a part of the
variables parameter of the TreeMaker describing photon isolation variables 
of a pat::Photon that are embedded as user floats.

Jan Veverka, Caltech, 11 Aug 2012
'''

import FWCore.ParameterSet.Config as cms
import Misc.TreeMaker.tools as tools

## Set Loose Cut-Based Photon ID optimized for non-triggering phostons at
## https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedPhotonID2012
## Revision: r8
## Accessed: 11 Aug 2012, 04:45 CEST.
photonIsolationVariables = tools.get_variables_from_map([
    ('chIso' , 'userFloat("photonIsolation:pfChargedHadron")' ),
    ('nhIso' , 'userFloat("photonIsolation:pfNeutralHadron")' ),
    ('phIso' , 'userFloat("photonIsolation:pfPhoton")'        ),
    ('rho'   , 'userFloat("photonIsolation:rho")'             ),
    ('chEA'  , 'userFloat("photonIsolation:chargedHadronEA")' ),
    ('nhEA'  , 'userFloat("photonIsolation:neutralHadronEA")' ),
    ('phEA'  , 'userFloat("photonIsolation:photonEA")'        ),
    ])
