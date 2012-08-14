import FWCore.ParameterSet.Config as cms

from RecoJets.Configuration.RecoPFJets_cff import kt4PFJets

kt6PFJetsPho = kt4PFJets.clone(
    rParam        = 0.6,
    doRhoFastjet  = True,
    doAreaFastjet = True,
    voronoiRfact  = 0.9,
    )
