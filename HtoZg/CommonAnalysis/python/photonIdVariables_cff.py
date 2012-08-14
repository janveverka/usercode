'''
Defines a configuration fragment that can be used as a part of the
variables parameter of the TreeMaker describing photon ID variables 
of a pat::Photon, some may be embedded as user floats.

Jan Veverka, Caltech, 11 Aug 2012
'''

import FWCore.ParameterSet.Config as cms
import Misc.TreeMaker.tools as tools

from HtoZg.CommonAnalysis.photon_selection import htozg_id

## Set Loose Cut-Based Photon ID optimized for non-triggering phostons at
## https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedPhotonID2012
## Revision: r8
## Accessed: 11 Aug 2012, 04:45 CEST.
photonIdVariables = tools.get_variables_from_map([
    ('isEB'   , 'isEB'),
    ('eleVeto', 'userInt("conversionTools:passElectronVeto")'),
    ('hoe'    , 'userFloat("photonId:hadTowOverEm")' ),
    ('sihih'  , 'sigmaIetaIeta'),
    ('passID', '? %s ? 1 : 0' % htozg_id                      ),
    ])
