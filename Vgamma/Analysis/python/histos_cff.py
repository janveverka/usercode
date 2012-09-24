import copy
import FWCore.ParameterSet.Config as cms
import Vgamma.Analysis.cuts as cuts
import Vgamma.Analysis.cuts.selection

## Default histo manager setup
fullSelection = cms.PSet(
    ## What selection should be applied?
    selection = copy.deepcopy(cuts.selection.selection_zgtommg_sep2012),
    ## What histogram groups should be filled?
    do = cms.vstring('Muons', 'Photons', 'BarrelPhotons', 'EndcapPhotons',
                     'Dimuons', 'mmgCands', 'Pileup'),
    )

## Fill all histograms, apply no selection
noSelection = copy.deepcopy(fullSelection)
noSelection.selection.cutsToIgnore = ['selectMuons', 'selectPhoton',
                                      'selectDimuons', 'selectZg']