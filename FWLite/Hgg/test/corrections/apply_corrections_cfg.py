# -*- coding: utf-8 -*-
import os
from copy import copy
import FWCore.ParameterSet.Config as cms


process = cms.Process('HggCorrectionsApplication')

photon_pair = lambda variable: ['ph1.' + variable, 'ph2.' + variable]

#_______________________________________________________________________________
def correction_pset(raw_variable, corrected_variable,
                    correction_graph_barrel, correction_graph_endcaps):
    '''
    Helps to more briefly define the correction configuration.
    Returns the cms.PSet describing it given the four strings.
    '''
    return cms.PSet(
        rawVariable            = cms.string(raw_variable),
        correctedVariable      = cms.string(corrected_variable),
        correctionGraphBarrel  = cms.string(correction_graph_barrel),
        correctionGraphEndcaps = cms.string(correction_graph_endcaps),
        )
## End of correction_pset


#_______________________________________________________________________________
def correction_pset_pair(raw_variable):
    return [correction_pset('ph1.' + raw_variable,
                            'ph1.' + raw_variable + '_corr',
                            raw_variable + 'b_qq_2',
                            raw_variable + 'e_qq_2'),
            correction_pset('ph2.' + raw_variable,
                            'ph2.' + raw_variable + '_corr',
                            raw_variable + 'b_qq_2',
                            raw_variable + 'e_qq_2'),]
## End of correction_pset_pair


#_______________________________________________________________________________
process.inputs = cms.PSet(
    ## Set below
    fileNames = cms.vstring(),
    treeName = cms.string('hPhotonTree'),
    version = cms.string('031'),
    variables = cms.vstring('mass/F',
                            *(photon_pair('pt/F') +
                            photon_pair('eta/F') +
                            photon_pair('r9/F') +
                            photon_pair('sigietaieta/F')))
    # activeBranches = copy.deepcopy(activeBranchesMC),
    )

### Jan's laptop
#base_path = '/Users/veverka/Work/Data/hgg-2013Final8TeV_ID/'
## T3 MIT
base_path = '/home/veverka/cms/hist/hgg-2013Final8TeV_ID/'

for filename in [
    #'ZGammaToMuMuGamma_2Jet_MG5_TuneZ2_mmgSkim_test10.root',
    'skimmed/hgg-2013Final8TeV_ID_s12-zllm50-v7n_skim10k.root',
    #'DoubleMu_Run2011A-05Aug2011-v1_mmgSkim_5kevt.root',
    ]:
    process.inputs.fileNames.append(
        os.path.join(base_path, filename)
        )

#_______________________________________________________________________________
output_filename = os.path.join(
    base_path, 'corrected',
    'hgg-2013Final8TeV_ID_s12-zllm50-v7n_skim10k.root'
    )
process.outputs = cms.PSet(
    fileName = cms.string(output_filename),
    treeName = cms.string('hPhotonTree'),
    variables = copy(process.inputs.variables),
    corrections = cms.VPSet(
        correction_pset('ph1.sigietaieta', 'ph1.sigietaieta_corr', 
                        'sieieb_qq_2', 'sieiee_qq_2'),
        correction_pset('ph2.sigietaieta', 'ph2.sigietaieta_corr', 
                        'sieieb_qq_2', 'sieiee_qq_2'),
        *correction_pset_pair('r9')
        )
    )
    
#_______________________________________________________________________________
process.maxEntries = cms.PSet(
    toProcess = cms.untracked.int64(-1),
    reportEvery = cms.untracked.int64(1000)
    )
    
#_______________________________________________________________________________
process.options = cms.PSet(
    verbosity = cms.int64(1)
    )
    
#_______________________________________________________________________________
if __name__ == '__main__':
    import user
    
