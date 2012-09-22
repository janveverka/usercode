import FWCore.ParameterSet.Config as cms

## Default photon selection in the barrel
photon_barrel_cuts_sep2012 = cms.PSet(
    minPt = cms.double(15),
    minAbsEtaSC = cms.double(0),
    maxAbsEtaSC = cms.double(1.4442),
    maxSihih = cms.double(0.11),
    hasPixelMatch = cms.bool(False),
    maxTrackIso = cms.double(2.0),
    maxEcalIso = cms.double(4.2),
    maxHcalIso = cms.double(2.2),
    cutsToIgnore = cms.vstring("minAbsEtaSC"),
    )

## Default photon selection in the endcaps
photon_endcap_cuts_sep2012 = cms.PSet(
    minPt = cms.double(15),
    minAbsEtaSC = cms.double(1.556),
    maxAbsEtaSC = cms.double(2.5),
    maxSihih = cms.double(0.30),
    hasPixelMatch = cms.bool(False),
    maxTrackIso = cms.double(2.0),
    maxEcalIso = cms.double(4.2),
    maxHcalIso = cms.double(2.2),
    )
