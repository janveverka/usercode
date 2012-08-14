import copy
import FWCore.ParameterSet.Config as cms
import PhysicsTools.PatAlgos.tools.coreTools as patcore
import HtoZg.CommonAnalysis.json as json
import HtoZg.CommonAnalysis.process_cfi as process_cfi

process = copy.deepcopy(process_cfi.process)

## Global tag
process.GlobalTag.globaltag = 'FT_R_42_V24::All'

## Input files
process.source.fileNames.append(
    '/store/data/Run2011A/DoubleMu/AOD/16Jan2012-v1/0001/E8EFCAFA-3F44-E111-A9DF-0026189438BC.root'
    )

## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

## Apply the json file
jsonfile = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Reprocessing/Cert_190456-196531_8TeV_29Jun2012ReReco_Collisions12_JSON.txt'
json.apply(jsonfile, process.source)

## Standard PAT Configuration File
# process.load("PhysicsTools.PatAlgos.patSequences_cff")

## The HtoZg sequence
process.load('HtoZg.MuonAnalysis.skimSequence_cff')
patcore.removeAllPATObjectsBut(process, ['Muons', 'Photons'])
patcore.removeMCMatching(process)

## TFileService for the ntuple output
process.load('HtoZg.CommonAnalysis.TFileService_cfi')
process.TFileService.fileName = 'data.root'

process.p = cms.Path(process.skimSequence)

if __name__ == '__main__':
    ## Adds tab-completion and history for interactive testing.
    import user

