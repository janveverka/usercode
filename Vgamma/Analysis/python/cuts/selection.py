import copy
import FWCore.ParameterSet.Config as cms
import Vgamma.Analysis.cuts as cuts
import Vgamma.Analysis.cuts.dimuon
import Vgamma.Analysis.cuts.muon
import Vgamma.Analysis.cuts.photon
import Vgamma.Analysis.cuts.zg


muon_cuts = cuts.muon.muon_cuts_sep2012
dimuon_cuts = cuts.dimuon.dimuon_cuts_sep2012
photon_barrel_cuts = cuts.photon.photon_barrel_cuts_sep2012
photon_endcap_cuts = cuts.photon.photon_endcap_cuts_sep2012
zg_cuts = cuts.zg.zg_cuts_sep2012

selection_zgtommg_sep2012 = cms.PSet(
    selectMuons   = cms.bool(True),
    selectDimuons = cms.bool(True),
    selectPhoton  = cms.bool(True),
    selectZg      = cms.bool(True),
    cutsToIgnore  = cms.vstring(),
    muonCuts         = copy.deepcopy(muon_cuts         ),
    dimuonCuts       = copy.deepcopy(dimuon_cuts       ),
    photonBarrelCuts = copy.deepcopy(photon_barrel_cuts),
    photonEndcapCuts = copy.deepcopy(photon_endcap_cuts),
    ZgCuts           = copy.deepcopy(zg_cuts           )
    )
