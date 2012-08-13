'''
Defines a default process and loads default sequences.

It should be customized for specific purpose like this:

import HtoZg.CommonAnalysis.process_cfi
process = HtoZg.CommonAnalysis.process_cfi.process.clone()
process.source.fileNames.extend(['file1.root', 'file2.root', ..., fileN.root'])
...

Jan Veverka, Caltech, 31 July 2012
'''
import FWCore.ParameterSet.Config as cms

process = cms.Process("ZG")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring()
)

## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
## This is new in 52x
# from Configuration.AlCa.autoCond import autoCond
# process.GlobalTag.globaltag = cms.string( autoCond[ 'startup' ] )
## GT for 2011 MC as a default
process.GlobalTag.globaltag = 'START42_V14B::All'
process.load("Configuration.StandardSequences.MagneticField_cff")

## Test JEC from test instances of the global DB
#process.load("PhysicsTools.PatAlgos.patTestJEC_cfi")

## Test JEC from local sqlite file
#process.load("PhysicsTools.PatAlgos.patTestJEC_local_cfi")

## Standard PAT Configuration File
#process.load("PhysicsTools.PatAlgos.patSequences_cff")

## Output Module Configuration (expects a path 'p')
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('zgTuple.root'),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    # save PAT Layer 1 output; you need a '*' to
    # unpack the list of commands 'patEventContent'
    outputCommands = cms.untracked.vstring('drop *', *patEventContent )
    )

# process.outpath = cms.EndPath(process.out)
