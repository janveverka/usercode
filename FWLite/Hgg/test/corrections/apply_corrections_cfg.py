import os
import FWCore.ParameterSet.Config as cms


process = cms.Process('HggCorrectionsApplication')

#______________________________________________________________________________
process.inputs = cms.PSet(
    fileNames = cms.vstring(),
    treeName = cms.string('hPhotonTree'),
    version = cms.string('031'),
    # activeBranches = copy.deepcopy(activeBranchesMC),
    )

## Jan's laptop
base_path = '/Users/veverka/Work/Data/hgg-2013Final8TeV_ID/'

for filename in [
    #'ZGammaToMuMuGamma_2Jet_MG5_TuneZ2_mmgSkim_test10.root',
    'skimmed/hgg-2013Final8TeV_ID_s12-zllm50-v7n_skim10k.root',
    #'DoubleMu_Run2011A-05Aug2011-v1_mmgSkim_5kevt.root',
    ]:
    process.inputs.fileNames.append(
        os.path.join(base_path, filename)
        )

#______________________________________________________________________________
output_filename = os.path.join(
    base_path, 'corrected',
    'hgg-2013Final8TeV_ID_s12-zllm50-v7n_skim10k.root'
    )
process.outputs = cms.PSet(
    outputName = cms.string(output_filename)
    )
    
#______________________________________________________________________________
process.maxEvents = cms.PSet(
    toProcess = cms.untracked.int64(-1),
    reportEvery = cms.untracked.int64(100)
    )
    
#______________________________________________________________________________
process.options = cms.PSet(
    verbosity = cms.int64(1)
    )
    
#______________________________________________________________________________
if __name__ == '__main__':
    import user
    
