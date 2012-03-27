'''
Fits linear transforamtions of MC showershape variables to match data.
Jan Veverka, Caltech, 27 March 2012
'''

import ROOT

import FWLite.Tools.roofit as roo
import FWLite.Tools.dataset as dataset
import FWLite.Tools.canvases as canvases
import FWLite.Tools.cmsstyle as cmsstyle

import JPsi.MuMu.common.energyScaleChains as esChains

from FWLite.Tools.modalinterval import ModalInterval
from FWLite.Tools.parameterizedkeyspdf import ParameterizedKeysPdf

#===============================================================================
class Fitter:
    '''
    Builds model, obtains data and fits linear transformation of
    the MC shower shape variables to data.
    '''


    #___________________________________________________________________________
    def __init__(self):
        '''Initializes attributes.'''
        self.w = ROOT.RooWorkspace('w', 'rescaling fitter')
    ## End of Fitter.__init__().
        

    #___________________________________________________________________________
    def run(self):
        '''Main entry point to the execution.'''
        self.define_observables()
        self.get_samples()
        self.build_models()
        self.fit_models_to_samples()
        self.make_plots()
        self.write_outputs()
    ## End of Fitter.run().


    #___________________________________________________________________________
    def define_observables(self):
        '''Defines data observables in the workspace.'''
        self.w.factory('mmg[90,30,150]').SetTitle('mass_{#mu#mu#gamma}')
        self.w.factory('mm[90,30,150]').SetTitle('mass_{#mu#mu}')
        self.w.factory('r9[1,0,1.1]').SetTitle('E_{3x3}^{#gamma}/E_{raw}^{SC}')
    ## End of Fitter.define_observables().


    #___________________________________________________________________________
    def get_samples(self):
        '''Get the MC and data samples and import them in the workspace.'''

        ## Yong's trees with the default CMSSW photon cluster corrections
        chains = esChains.getChains('v13')

        ## Map of variable names and corresponding TTree expressions to
        ## calculate it.
        expression_map = {
            'mmg': 'mmg',
            }

        # Change titles to TTree expressions while saving the original titles.
        title_map = self.replace_variable_titles(expression_map)
        
        data = dataset.get(tree=chains['data'], variable=self.w.var('mmg'),
                           cuts=[], name='data')
        mc = dataset.get(tree=chains['z'], variable=self.w.var('mmg'),
                           cuts=[], name='mc')

        # Change the titles back to their original values.
        self.replace_variable_titles(title_map)
        
        self.w.Import(data)
        self.w.Import(mc)
    ## End of Fitter.get_samples().


    #___________________________________________________________________________
    def replace_variable_titles(self, new_titles):
        '''
        Replaces the titles of variables in the workspace using the given
        dictionary (name)->(new title) and returns the dictionary of the
        original titles (name)->(old title).
        '''
        old_titles = {}
        for name in new_titles:
            old_titles[name] = self.w.var(name).GetTitle()
            self.w.var(name).SetTitle(new_titles[name])
        return old_titles
    ## End of Fitter.build_models().


    #___________________________________________________________________________
    def build_models(self):
        '''Builds the model(s) for the fitting.'''
        pass
    ## End of Fitter.build_models().


    #___________________________________________________________________________
    def fit_models_to_samples(self):
        '''Fits the models to the samples.'''
        pass
    ## End of Fitter.().


    #___________________________________________________________________________
    def make_plots(self):
        '''Makes the plots.'''
        self.plot_mmg_mass()
    ## End of Fitter.make_plots().


    #___________________________________________________________________________
    def plot_mmg_mass(self):
        '''Makes a canvas of the mmg mass for data and MC.'''
        pass
    ## End of Fitter.plot_mmg_mass().    


    #___________________________________________________________________________
    def write_outputs(self):
        '''Write the workspace and canvases to files.'''
        pass
    ## End of Fitter.write_outputs().
    
## End of Fitter



#===============================================================================
if __name__ == '__main__':
    print "Welcome to the test of the rescaling fitter!"
    fitter = Fitter()
    fitter.run()
    fitter.w.Print()
    print "Exiting rescaling fitter test with success."
    import user
    
