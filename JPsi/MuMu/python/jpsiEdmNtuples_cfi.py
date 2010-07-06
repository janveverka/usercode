import FWCore.ParameterSet.Config as cms

# {tag: quantity}
# Tag is set to a TTree alias.
# Quantity is interpreted by the PhysicsCutParser and resulting value is stored.
jpsiQuantities = {
  "Mass": "mass",
  "Pt"  : "pt",
  "Eta" : "eta",
  "Phi" : "phi",
  "Y"   : "y",
  "P"   : "p",
  "Charge" : "charge",
}

muonQuantities = {
  "Pt"  : "pt",
  "Eta" : "eta",
  "Phi" : "phi",
  "P"   : "p",
  "Charge" : "charge",
}

for x in muonQuantities.keys():
  jpsiQuantities["Dau1" + x] = "daughter(0).masterClone." + muonQuantities[x]
  jpsiQuantities["Dau2" + x] = "daughter(1).masterClone." + muonQuantities[x]

jpsiVars = cms.VPSet()

jpsiVars += [
  cms.PSet(
    tag = cms.untracked.string(aTag),
    quantity = cms.untracked.string(jpsiQuantities[aTag])
  ) for aTag in jpsiQuantities.keys()
]

ggosJPsiEdmNtuple = cms.EDProducer("CandViewNtpProducer",
  src = cms.InputTag("dimuonsGGOS"),
  lazyParser = cms.untracked.bool(True),
  prefix = cms.untracked.string("ggosJPsi"),
  variables = jpsiVars
)

ggssJPsiEdmNtuple = ggosJPsiEdmNtuple.clone(src = "dimuonsGGSS", prefix = "ggssJPsi")

gtosJPsiEdmNtuple = ggosJPsiEdmNtuple.clone(src = "dimuonsGTOS", prefix = "gtosJPsi")
gtssJPsiEdmNtuple = ggosJPsiEdmNtuple.clone(src = "dimuonsGTSS", prefix = "gtssJPsi")

ttosJPsiEdmNtuple = ggosJPsiEdmNtuple.clone(src = "dimuonsTTOS", prefix = "ttosJPsi")
ttssJPsiEdmNtuple = ggosJPsiEdmNtuple.clone(src = "dimuonsTTSS", prefix = "ttssJPsi")
