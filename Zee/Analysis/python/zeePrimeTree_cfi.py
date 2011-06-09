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
  ebRechits = cms.PSet(
      src = cms.InputTag("reducedEcalRecHitsEB"),
      prefix = cms.untracked.string("ebRechit."),
      sizeName = cms.untracked.string("ebRechit.size"),
      variables = cms.VPSet(),
  ),
  eeRechits = cms.PSet(
      src = cms.InputTag("reducedEcalRecHitsEE"),
      prefix = cms.untracked.string("eeRechit."),
      sizeName = cms.untracked.string("eeRechit.size"),
      variables = cms.VPSet(),
  ),
  esRechits = cms.PSet(
      src = cms.InputTag("reducedEcalRecHitsES"),
      prefix = cms.untracked.string("esRechit."),
      sizeName = cms.untracked.string("esRechit.size"),
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
    ('isEB' , 'isEB'),
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

zeePrimeTree.ebRechits.variables.extend([
    var( 'energy', 'energy'),
    var( 'time'  , 'time'),
    var( 'recoFlag', 'recoFlag' ),
    var( 'id', 'id.rawId' ),
])

zeePrimeTree.eeRechits.variables.extend([
    var( 'energy', 'energy'),
    var( 'time'  , 'time'),
    var( 'recoFlag', 'recoFlag' ),
    var( 'id', 'id.rawId' ),
])

zeePrimeTree.esRechits.variables.extend([
    var( 'energy', 'energy'),
    var( 'time'  , 'time'),
    var( 'recoFlag', 'recoFlag' ),
    var( 'id', 'id.rawId' ),
])
