import FWCore.ParameterSet.Config as cms

basicTest = cms.EDAnalyzer("CandViewTreeMaker",
    name = cms.untracked.string("tree"),
    title = cms.untracked.string("photon tree test"),
    src = cms.InputTag("photons"),
    prefix = cms.untracked.string("photon."),
    sizeName = cms.untracked.string("photon.size"),
    variables = cms.VPSet(
        cms.PSet( tag      = cms.untracked.string("pt"),
                  quantity = cms.untracked.string("pt")  ),

        cms.PSet( tag      = cms.untracked.string("eta"),
                  quantity = cms.untracked.string("eta")  ),

        cms.PSet( tag      = cms.untracked.string("phi"),
                  quantity = cms.untracked.string("phi")  ),

        ## An example of a quantity using the lazy parsing
        cms.PSet( tag      = cms.untracked.string("r9"),
                  quantity = cms.untracked.string("r9")  ),

        ## An example of a conditional quantity
        cms.PSet( tag      = cms.untracked.string("zSide"),
                  conditionalQuantity = cms.untracked.PSet(
                      ifCondition  = cms.untracked.string("eta > 0"),
                      thenQuantity = cms.untracked.string("1"),
                      elseQuantity = cms.untracked.string("-1")
                  ) # end of conditionalQuantity
        ) # end of the last cms.PSet
    ) # end of variables
) # end of tree
