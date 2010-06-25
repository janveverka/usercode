import FWCore.ParameterSet.Config as cms

from JPsi.EE.skimElectrons_cfi import *

## Define analyzer counting electrons
process.load("JPsi.EE.countHistos_cfi")
process.countHistosBefore = process.countHistos.clone()
process.countHistosAfter  = process.countHistos.clone()

## Define the filter path
process.load("JPsi.EE.filterSequence_cff")
process.p = cms.Path(
  process.countHistosBefore +
  process.filterSequence +
  process.countHistosAfter
)

process.maxEvents.output = 10

if __name__ == "__main__": import user