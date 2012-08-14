'''
Tools to facilitate configuration sequence building.

Jan Veverka, Caltech
14 August 1977
'''
import FWCore.ParameterSet.Config as cms
from PhysicsTools.PatAlgos.tools.pfTools import usePF2PAT

##_____________________________________________________________________________
def ensure_labels(label_map):
    '''
    Takes a map of {label -> config} and ensures that all
    configuration fragments "config" that are labelable have
    their labels properly set.
    
    USAGE: ensure_labels(locals())
    '''
    for label, config in label_map.items():
        if cms._Labelable in type.mro(type(config)):
            print 'ensure_labels: Setting label for', label
            config.setLabel(label)
## End of ensure_labels
