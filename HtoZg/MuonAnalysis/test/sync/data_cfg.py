import copy
import FWCore.ParameterSet.Config as cms
import PhysicsTools.PatAlgos.tools.coreTools as patcore
import HtoZg.CommonAnalysis.json as json
import HtoZg.CommonAnalysis.process_cfi as process_cfi

process = copy.deepcopy(process_cfi.process)

## Input files
process.source.fileNames.append(
    '/store/data/Run2012B/DoubleMu/AOD/29Jun2012-v1/0001/C46FD2A9-3FC3-E111-A1A8-485B39800C00.root'
    )

## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

## Apply the json file
jsonfile = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Reprocessing/Cert_190456-196531_8TeV_29Jun2012ReReco_Collisions12_JSON.txt'
json.apply(jsonfile, process.source)

## Standard PAT Configuration File
# process.load("PhysicsTools.PatAlgos.patSequences_cff")

## The HtoZg sequence
process.load('HtoZg.MuonAnalysis.skimSequence_cff')
patcore.removeAllPATObjectsBut(process, ['Muons'])
patcore.removeMCMatching(process)

## TFileService for the ntuple output
process.load('HtoZg.CommonAnalysis.TFileService_cfi')
# process.TFileService.fileName = 'zg_data.root'

process.p = cms.Path(process.skimSequence)

if __name__ == '__main__':
    ## Adds tab-completion and history for interactive testing.
    import user

