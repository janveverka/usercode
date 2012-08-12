'''
Defines a configuration fragment that can be used as a part of the
variables parameter of the TreeMaker describing muon isolation variables 
of a pat::Muon, some are embedded as user floats.

Jan Veverka, Caltech, 8 Aug 2012
'''

import FWCore.ParameterSet.Config as cms
import Misc.TreeMaker.tools as tools

from HtoZg.MuonAnalysis.muon_selection import htozg_isolation

## Set Thigt Muon ID at
## https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId#Tight_Muon
## Revision: r35
## Accessed: 6 Aug 2012, 22:41 CEST.
muonIsolationVariables = tools.get_variables_from_map([
    ('chIso'  , 'pfIsolationR04().sumChargedHadronPt'),
    ('nhIso'  , 'pfIsolationR04().sumNeutralHadronEt'),
    ('phIso'  , 'pfIsolationR04().sumPhotonEt'       ),
    ('combIso', 'userFloat("muonIsolation:combIso")' ),
    ('rho'    , 'userFloat("muonIsolation:rho")'     ),
    ('EA'     , 'userFloat("muonIsolation:EA")'      ),
    ('passIso', '? %s ? 1 : 0' % htozg_isolation     ),
    ])
