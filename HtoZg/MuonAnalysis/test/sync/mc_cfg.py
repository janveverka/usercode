import copy
import FWCore.ParameterSet.Config as cms
import PhysicsTools.PatAlgos.tools.coreTools as patcore
import HtoZg.CommonAnalysis.process_cfi

process = copy.deepcopy(HtoZg.CommonAnalysis.process_cfi.process)

## Global tag
process.GlobalTag.globaltag = 'START42_V14B::All'

## Input files
process.source.fileNames.append(
    '/store/mc/Fall11/GluGluToHToZG_M-125_7TeV-powheg-pythia6/AODSIM/PU_S6_START42_V14B-v1/0000/4E7D0288-43BA-E111-B933-0026189438F7.root'
    )

## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

## Standard PAT Configuration File
# process.load("PhysicsTools.PatAlgos.patSequences_cff")

## The HtoZg sequence
process.load('HtoZg.MuonAnalysis.skimSequence_cff')
patcore.removeAllPATObjectsBut(process, ['Muons', 'Photons'])

## TFileService for the ntuple output
process.load('HtoZg.CommonAnalysis.TFileService_cfi')
process.TFileService.fileName = 'mc.root'

process.p = cms.Path(process.skimSequence)

if __name__ == '__main__':
    ## Adds tab-completion and history for interactive testing.
    import user

