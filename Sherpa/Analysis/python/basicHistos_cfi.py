import FWCore.ParameterSet.Config as cms

ptHisto = cms.PSet(
  itemsToPlot = cms.untracked.int32(-1),
  min = cms.untracked.double(0),
  max = cms.untracked.double(300),
  nbins = cms.untracked.int32(300),
  name = cms.untracked.string("Pt"),
  description = cms.untracked.string("P_{#perp}   [GeV/c]"),
  plotquantity = cms.untracked.string("pt")
)

etaHisto = cms.PSet(
  itemsToPlot = cms.untracked.int32(-1),
  min = cms.untracked.double(-10.0),
  max = cms.untracked.double(10.0),
  nbins = cms.untracked.int32(200),
  name = cms.untracked.string("Eta"),
  description = cms.untracked.string("#eta"),
  plotquantity = cms.untracked.string("eta")
)

phiHisto = cms.PSet(
  itemsToPlot = cms.untracked.int32(-1),
  min = cms.untracked.double(-4),
  max = cms.untracked.double(4),
  nbins = cms.untracked.int32(80),
  name = cms.untracked.string("Phi"),
  description = cms.untracked.string("#phi"),
  plotquantity = cms.untracked.string("phi")
)

rapidityHisto = cms.PSet(
  itemsToPlot = cms.untracked.int32(-1),
  min = cms.untracked.double(-6.0),
  max = cms.untracked.double(6.0),
  nbins = cms.untracked.int32(120),
  name = cms.untracked.string("Rapidity"),
  description = cms.untracked.string("y"),
  plotquantity = cms.untracked.string("rapidity")
)

massHisto = cms.PSet(
  itemsToPlot = cms.untracked.int32(-1),
  min = cms.untracked.double(0),
  max = cms.untracked.double(200),
  nbins = cms.untracked.int32(200),
  name = cms.untracked.string("Mass"),
  description = cms.untracked.string("Mass [GeV/c^{2}]"),
  plotquantity = cms.untracked.string("mass")
)

pdgIdHisto = cms.PSet(
  itemsToPlot = cms.untracked.int32(-1),
  min = cms.untracked.double(-25.5),
  max = cms.untracked.double(25.5),
  nbins = cms.untracked.int32(51),
  name = cms.untracked.string("PdgId"),
  description = cms.untracked.string("PDG id"),
  plotquantity = cms.untracked.string("pdgId")
)

statusHisto = cms.PSet(
  itemsToPlot = cms.untracked.int32(-1),
  min = cms.untracked.double(0.5),
  max = cms.untracked.double(10.5),
  nbins = cms.untracked.int32(10),
  name = cms.untracked.string("Status"),
  description = cms.untracked.string("Status"),
  plotquantity = cms.untracked.string("status")
)

motherCountHisto = cms.PSet(
  itemsToPlot = cms.untracked.int32(-1),
  min = cms.untracked.double(-0.5),
  max = cms.untracked.double(50.5),
  nbins = cms.untracked.int32(51),
  name = cms.untracked.string("MotherCount"),
  description = cms.untracked.string("number of mothers"),
  plotquantity = cms.untracked.string("numberOfMothers")
)

motherPdgIdHisto = cms.PSet(
  itemsToPlot = cms.untracked.int32(-1),
  min = cms.untracked.double(-100.5),
  max = cms.untracked.double(100.5),
  nbins = cms.untracked.int32(201),
  name = cms.untracked.string("MotherPdgId"),
  description = cms.untracked.string("mother PDG id"),
  plotquantity = cms.untracked.string("mother(0).pdgId")
)

motherStatusHisto = cms.PSet(
  itemsToPlot = cms.untracked.int32(-1),
  min = cms.untracked.double(0.5),
  max = cms.untracked.double(10.5),
  nbins = cms.untracked.int32(10),
  name = cms.untracked.string("MotherStatus"),
  description = cms.untracked.string("Mother Status"),
  plotquantity = cms.untracked.string("mother(0).status")
)

grandmotherCountHisto = cms.PSet(
  itemsToPlot = cms.untracked.int32(-1),
  min = cms.untracked.double(-0.5),
  max = cms.untracked.double(50.5),
  nbins = cms.untracked.int32(51),
  name = cms.untracked.string("GrandmotherCount"),
  description = cms.untracked.string("number of grandmothers"),
  plotquantity = cms.untracked.string("mother(0).numberOfMothers")
)

grandmotherStatusHisto = cms.PSet(
  itemsToPlot = cms.untracked.int32(-1),
  min = cms.untracked.double(0.5),
  max = cms.untracked.double(10.5),
  nbins = cms.untracked.int32(10),
  name = cms.untracked.string("GrandmotherStatus"),
  description = cms.untracked.string("Gandmother Status"),
  plotquantity = cms.untracked.string("mother(0).mother(0).status")
)

grandmotherPdgIdHisto = cms.PSet(
  itemsToPlot = cms.untracked.int32(-1),
  min = cms.untracked.double(-100.5),
  max = cms.untracked.double(100.5),
  nbins = cms.untracked.int32(201),
  name = cms.untracked.string("GrandmotherPdgId"),
  description = cms.untracked.string("grandmother PDG id"),
  plotquantity = cms.untracked.string("mother(0).mother(0).pdgId")
)

sisterCountHisto = cms.PSet(
  itemsToPlot = cms.untracked.int32(-1),
  min = cms.untracked.double(-0.5),
  max = cms.untracked.double(50.5),
  nbins = cms.untracked.int32(51),
  name = cms.untracked.string("SistersCount"),
  description = cms.untracked.string("number of sisters"),
  plotquantity = cms.untracked.string("mother(0).numberOfDaughters")
)

sisterPdgIdHisto = cms.PSet(
  itemsToPlot = cms.untracked.int32(-1),
  min = cms.untracked.double(-100.5),
  max = cms.untracked.double(100.5),
  nbins = cms.untracked.int32(201),
  name = cms.untracked.string("SisterPdgId"),
  description = cms.untracked.string("sister PDG id"),
  plotquantity = cms.untracked.string("mother(0).daughter(0).pdgId")
)

daughterCountHisto = cms.PSet(
  itemsToPlot = cms.untracked.int32(-1),
  min = cms.untracked.double(-0.5),
  max = cms.untracked.double(50.5),
  nbins = cms.untracked.int32(51),
  name = cms.untracked.string("DaughterCount"),
  description = cms.untracked.string("number of daughters"),
  plotquantity = cms.untracked.string("numberOfDaughters")
)

daughter0PdgIdHisto = cms.PSet(
  itemsToPlot = cms.untracked.int32(-1),
  min = cms.untracked.double(-100.5),
  max = cms.untracked.double(100.5),
  nbins = cms.untracked.int32(201),
  name = cms.untracked.string("Daughter0PdgId"),
  description = cms.untracked.string("daughter 0 PDG id"),
  plotquantity = cms.untracked.string("daughter(0).pdgId")
)

daughter0StatusHisto = cms.PSet(
  itemsToPlot = cms.untracked.int32(-1),
  min = cms.untracked.double(0.5),
  max = cms.untracked.double(10.5),
  nbins = cms.untracked.int32(10),
  name = cms.untracked.string("Daughter0Status"),
  description = cms.untracked.string("Daughter 0 Status"),
  plotquantity = cms.untracked.string("daughter(0).status")
)

simpleKineGenHistos = cms.PSet(
  histograms = cms.VPSet(
    ptHisto, etaHisto, phiHisto, pdgIdHisto, statusHisto
  )
)

simpleKineGenDebugHistos = cms.PSet(
  histograms = cms.VPSet(
    ptHisto, etaHisto, phiHisto,
    pdgIdHisto, statusHisto,
    motherCountHisto, motherPdgIdHisto, motherStatusHisto,
    grandmotherCountHisto, grandmotherPdgIdHisto, grandmotherStatusHisto,
    sisterCountHisto, sisterPdgIdHisto,
    daughterCountHisto, daughter0PdgIdHisto, daughter0StatusHisto
  )
)

composite2KineHistos = cms.PSet(
  histograms = cms.VPSet(
    ptHisto, etaHisto, phiHisto, rapidityHisto, massHisto
  )
)


