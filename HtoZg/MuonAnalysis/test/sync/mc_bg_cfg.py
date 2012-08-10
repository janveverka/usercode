import copy
import FWCore.ParameterSet.Config as cms
import PhysicsTools.PatAlgos.tools.coreTools as patcore
import HtoZg.CommonAnalysis.process_cfi

process = copy.deepcopy(HtoZg.CommonAnalysis.process_cfi.process)

## Input files
process.source.fileNames.append(
    '/store/mc/Summer12/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/AODSIM/PU_S7_START52_V9-v2/0003/EAF43999-8D9B-E111-A418-003048D4610E.root'
    )

## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

## Standard PAT Configuration File
# process.load("PhysicsTools.PatAlgos.patSequences_cff")

## The HtoZg sequence
process.load('HtoZg.MuonAnalysis.skimSequence_cff')
patcore.removeAllPATObjectsBut(process, ['Muons'])

## The muon tree maker
#process.load('HtoZg.MuonAnalysis.muonTree_cfi')
#process.muonsAfterVertexFilter = process.muonTree.clone()
#process.muonsAfterId = process.muonTree.clone(
    #src = cms.InputTag('tightMuons')
    #)

## TFileService for the ntuple output
process.load('HtoZg.CommonAnalysis.TFileService_cfi')

process.p = cms.Path(process.skimSequence)
#process.p = cms.Path(process.allInputEvents +
                     #process.hltFilterSequence + 
                     #process.vertexFilterSequence +
                     #process.patSequence +
                     #process.muonsAfterVertexFilter +
                     #process.tightDimuonSequence +
                     #process.muonsAfterId) 

if __name__ == '__main__':
    ## Adds tab-completion and history for interactive testing.
    import user

