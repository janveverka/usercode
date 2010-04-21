## V-gamma Z(->mumu)gamma subskim
## Based on ElectroWeakAnalysis/Skimming/test/EWK_ZMuMuSubskim.py
## and PhysicsTools/PatAlgos/python/patTemplate_cfg.py

import FWCore.ParameterSet.Config as cms

process = cms.Process("VGAMMA")

## Message logger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
     fileNames = cms.untracked.vstring(
      'rfio:/castor/cern.ch/cms/store/relval/CMSSW_3_5_7/RelValZMM/GEN-SIM-RECO/START3X_V26-v1/0012/10B71379-4549-DF11-9D80-003048D15D22.root'
    )
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'START3X_V26::All'
process.load("Configuration.StandardSequences.MagneticField_cff")

process.load("ElectroWeakAnalysis.MultiBosons.Skimming.zMuMu_SubskimSequences_cff")

## Add the PAT stuff here
## This is kind of ugly since we first load all the PAT
## + sequences and then remove most of them again. It takes
## + long but it is easily reconfigurable and will keep in
## + synch with changes in the PAT by default.
process.load("PhysicsTools.PatAlgos.patSequences_cff")

## Add V-gamma specific path (store only events with
## + at least 1 mumuGamma candidate
process.load("ElectroWeakAnalysis.MultiBosons.Skimming.ZMuMuGamma_SubskimSequences_cff")

## Import the output module configuration from the ZMuMu
from ElectroWeakAnalysis.Skimming.zMuMuSubskimOutputModule_cfi import zMuMuSubskimOutputModule
process.out = zMuMuSubskimOutputModule.clone(
  fileName = 'zMuMuGammaSubskim.root',
  SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring("p")
  )
)

## Add the PAT parameters to the output module
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent
process.out.outputCommands += cms.untracked.vstring(*patEventContent )

process.outpath = cms.EndPath(process.out)

## Ease the inspection of the file with `python -i <filename>'
if __name__ == "__main__":
  import user
