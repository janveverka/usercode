'''
module Zmmg.FWLite.phosphor.fitter
---------------------------------

Facilitates the PHOton energy Scale and PHOton energy Resolution (PHOSPHOR)
extraction using radiative Z decays to muons Z -> mu+ mu- gamma.

Provides a python class Fitter that
    - Builds a model PDF.
    - Provides I/O of the model PDF in a workspace.
    - Validates a model.
    - Retreives a dataset (?)
    - Fits a dataset to the model.
    - Provides I/O of the fit results in a workspace.
    - Validates a fit.
'''

import ROOT
import FWLite.Tools.roofit as roo

#==============================================================================
class Fitter:
    #__________________________________________________________________________
    def __init__(self, name='phosphor', title=None):
        '''
        Fitter()
        
        Zmmg.FWLite.phosphor.fitter.Fitter class constructor. This class
        facilitates building, validating, fitting and fit validation for
        the PHOSPHOR model as well the I/O with a workspace.
        '''
        ## If no title provided, use the name for it.
        if not title:
            title = name
            
        self.w = ROOT.RooWorkspace(name, title)
    ## End of Fitter.__init__(...)
    
    
    #__________________________________________________________________________
    def build_model(self, cfg):
        '''
        void Fitter.build_model()
        
        Builds the model given the configuration `cfg'.
        Preconditions: None.
        Postconditions: The workspace self.w constains the model and all its
            its dependents including component PDFs, variables and training
            data.  They are store in a top-level directory `model.'
        '''
        
        pass
    ## End of Fitter.build_model(...)
    
    
    #__________________________________________________________________________
    def validate_model(self):
        '''
        void Fitter.validate_model()
        
        
        Makes validation plots for the model:
            - Signal PDF vs mass and phos.
            - Signal moment morph reference shapes vs mass.
            - Signal PDF projection vs mass for a number of phos and phor 
              values.
        Preconditions: The model is in the workspace self.w/model.
        Postconditions: The validation plot canvases are created and appended
            together with their components in the workspace directory 
            `model_validation.'
        '''
        pass
    ## End of Fitter.validate_model()
       
    #__________________________________________________________________________
    def fit_data(self, cfg):
        '''
        void Fitter.fit_data(cfg)
        
        Gets the data described in the configuration and fits it with the
        model
        Preconditions: The model is in the workspace.
        Postcondistions: The data and the fit results are added to the 
            workspace in a directory whose name is specified in the 
            configuration.
        '''
        pass
    ## End of Fitter.fit_data()
    
    #__________________________________________________________________________
    def validate_fit(self, cfg):
        '''
        void Fitter.validate_fit(cfg)
        
        Creates validation plots for a fit to data specified in the 
            configuration.
        Preconditions: The model, the data and the fit results are in the 
            workspace.
        Postcondistions: The validation plots are added to a subdirectory
            fit_validation of the directory containing the data and fit.
        '''
        pass
    ## End of Fitter.validate_fit()
    
## End of class Fitter.
