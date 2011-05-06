import FWCore.ParameterSet.Config as cms

###############################################################################
tree = cms.EDAnalyzer("CandViewTreeMaker",
    name = cms.untracked.string("tree"),
    title = cms.untracked.string("Easter Bump tree"),
    src = cms.InputTag("egammas"),
    prefix = cms.untracked.string("eg."),
    sizeName = cms.untracked.string("eg.size"),
    variables = cms.VPSet()
) # end of tree

###############################################################################
varPSet = lambda t,q: cms.PSet( tag      = cms.untracked.string(t),
                                quantity = cms.untracked.string(q)  )


###############################################################################
def condVarPSet(iTag, iIf, iThen, iElse):
    return cms.PSet( tag      = cms.untracked.string(iTag),
                     conditionalQuantity = cms.untracked.PSet(
                         ifCondition  = cms.untracked.string(iIf),
                         thenQuantity = cms.untracked.string(iThen),
                         elseQuantity = cms.untracked.string(iElse)
                     ) # end of conditionalQuantity
           ) # end of cms.PSet

###############################################################################
def eleVarPSet(iTag, iQuantity):
    iQuantity = 'daughter("electron").' + iQuantity
    return varPSet(iTag, iQuantity)

###############################################################################
def phoVarPSet(iTag, iQuantity):
    iQuantity = 'daughter("photon").' + iQuantity
    return varPSet(iTag, iQuantity)


###############################################################################
tree.variables.extend([ varPSet( "mass", "mass" ),
                        eleVarPSet( "ele.pt", "pt" ),
                        eleVarPSet( "ele.eta", "eta" ),
                        eleVarPSet( "ele.phi", "phi" ),
                        phoVarPSet( "pho.pt", "pt" ),
                        phoVarPSet( "pho.eta", "eta" ),
                        phoVarPSet( "pho.phi", "phi" ),
])

