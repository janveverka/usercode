'''
Defines a configuration fragment that can be used as a part of the
variables parameter of the TreeMaker describing muon ID variables 
of a pat::Muon (vertexing variables are embedded as user floats).

Jan Veverka, Caltech, 6 Aug 2012
'''

import FWCore.ParameterSet.Config as cms
import Misc.TreeMaker.tools as tools

## Set Thigt Muon ID at
## https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId#Tight_Muon
## Revision: r35
## Accessed: 6 Aug 2012, 22:41 CEST.
muonIdVariables = tools.get_variables_from_map([
    ('isGlobal', 'isGlobalMuon'                                     ),
    ('isPF'    , 'isPFMuon'                                         ),
    ('normChi2', 'globalTrack().normalizedChi2'                     ),
    ('nHit'    , 'globalTrack().hitPattern().numberOfValidMuonHits' ),
    ('nMatch'  , 'numberOfMatchedStations'                          ),
    ('dxy'     , 'userFloat("muonVertexing:dxy")'                   ),
    ('dz'      , 'userFloat("muonVertexing:dz")'                    ),
    ('nPixel'  , 'innerTrack().hitPattern().numberOfValidPixelHits' ),
    ('nLayer'  , 'track().hitPattern().trackerLayersWithMeasurement'),
    ])
