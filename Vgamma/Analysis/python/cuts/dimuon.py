import FWCore.ParameterSet.Config as cms

## Default dimuon selection
dimuon_cuts_sep2012 = cms.PSet(
    charge = cms.int32(0),
    minMass = cms.double(50),
    )

