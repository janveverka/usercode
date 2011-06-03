import FWCore.ParameterSet.Config as cms

zeePrimeTree = cms.EDAnalyzer("ZeePrimeTreeMaker",
  name  = cms.untracked.string("zee"),
  title = cms.untracked.string("Z'-> ee analysis"),
  src   = cms.InputTag("patPhotons"),
  prefix = cms.untracked.string("ee."),
  sizeName = cms.untracked.string("ee.size"),
  variables = cms.VPSet(),
  photons = cms.PSet(
      src = cms.InputTag("patPhotons"),
      prefix = cms.untracked.string("photon."),
      sizeName = cms.untracked.string("photon.size"),
      variables = cms.VPSet(),
  ),
  uncleanPhotons = cms.PSet(
      src = cms.InputTag("uncleanPatPhotons"),
      prefix = cms.untracked.string("uncleanPhoton."),
      sizeName = cms.untracked.string("uncleanPhoton.size"),
      variables = cms.VPSet(),
  ),
)

def var(iTag, iQuantity):
    return cms.PSet( tag = cms.untracked.string(iTag),
                     quantity = cms.untracked.string(iQuantity) )

def varList(iList):
    return [ var(t, q) for t, q in iList ]

## Kinematic variables common to all candidates
kinematicVars = [ ('pt', 'pt'),
                  ('eta', 'eta'),
                  ('phi', 'phi')  ]

## Photon specific variables
photonVars = [
    ('r9' , 'r9'),
    ('hoe', 'hadronicOverEm'),
]

for variables in [ zeePrimeTree.photons.variables,
                   zeePrimeTree.uncleanPhotons.variables, ] :
    variables.extend( varList(kinematicVars) +
                      varList(photonVars) )

zeePrimeTree.photons.variables.append(
    var( 'seedTime', 'userFloat("photonUserData:seedTime")' )
)

zeePrimeTree.uncleanPhotons.variables.append(
    var( 'seedTime', 'userFloat("uncleanPhotonUserData:seedTime")' )
)
