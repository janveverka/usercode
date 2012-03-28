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

from FWLite.Tools.legend import Legend
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
        self.cuts = ['mmg + mm < 180', 'mm > 40',
                     'gamenergy / cosh(gameta) > 15']

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
        self.w.factory('weight[1,0,100]').SetTitle('Event Weight')
        self.w.factory('mmg[90,30,150]').SetTitle('m_{#mu#mu#gamma}')
        self.w.factory('mm[90,30,150]').SetTitle('m_{#mu#mu}')
        self.w.factory('gpt[1,0,500]').SetTitle('E_{T}^{#gamma}')
        self.w.factory('geta[1,-3,3]').SetTitle('#eta^{#gamma}')
        self.w.factory('r9[1,0,1.5]').SetTitle('E_{3x3}^{#gamma}/E_{raw}^{SC}')
        self.w.factory('sihih[1,0,1]').SetTitle('#sigma_{i#etai#eta}')

        ## (name) -> (unit, plot binning)
        variable_attributes = {
            'weight' : ('', ROOT.RooUniformBinning(0., 10, 100)),
            'mmg' : ('GeV', ROOT.RooUniformBinning(70, 110, 80)),
            'mm' : ('GeV', ROOT.RooUniformBinning(40, 90, 100)),
            'gpt' : ('GeV', ROOT.RooUniformBinning(0, 100, 100)),
            'geta' : ('', ROOT.RooUniformBinning(-2.5, 2.5, 50)),
            'r9' : ('', ROOT.RooUniformBinning(0.2, 1.1, 90)),
            'sihih' : ('', ROOT.RooUniformBinning(0., 0.1, 100)),
            }

        for xname, (xunit, xbins) in variable_attributes.items():
            self.w.var(xname).setUnit(xunit)
            self.w.var(xname).setBinning(xbins, 'plot')
        
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
            'mm' : 'mm' ,
            'gpt' : 'gamenergy/cosh(gameta)',
            'geta' : 'gameta', 
            'r9' : 'gamr9' ,
            'sihih' : 'gamsigmaIetaIeta',
            'weight' : 'evtweight',
            }

        # Change titles to TTree expressions while saving the original titles.
        title_map = self.replace_variable_titles(expression_map)

        variables = [self.w.var(xname) for xname in expression_map
                     if xname != 'weight']
        weight = self.w.var('weight')
        
        data = dataset.get(tree=chains['data'], variables=variables,
                           weight=weight, cuts=self.cuts[:], name='data')
        mc = dataset.get(tree=chains['z'], variables=variables,
                         weight=weight, cuts=self.cuts[:], name='mc')

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
        ## Inclusive variables
        for xname in 'mmg mm gpt geta'.split():
            self.plot_variable(xname)
            
        ## Variables different for Barrel and Endcaps
        for xname in 'r9 sihih'.split():
            self.plot_variable(xname, 'abs(geta) < 1.5', 'eb', 'Barrel')
            self.plot_variable(xname, 'abs(geta) > 1.5', 'ee', 'Endcaps')
    ## End of Fitter.make_plots().


    #___________________________________________________________________________
    def plot_variable(self, varname, selection='', label='', title=''):
        '''Makes a canvas of the variable spectrum for MC overlayed with data.'''

        hvar = self.w.var(varname)
        hbins = hvar.getBinning('plot')

        if label:
            name = '_'.join([hvar.GetName(), label])
        else:
            name = hvar.GetName()
            
        ## Book the histograms
        htitle = '%s;%s;Events / %g %s' % (title, hvar.GetTitle(),
                                           hbins.averageBinWidth(),
                                           hvar.getUnit())
        
        hmc = ROOT.TH1F('hmc_' + name, htitle, hbins.numBins(), hbins.array())
        hdata = hmc.Clone('hdata_' + name)

        ## Make sure we use PU weights.
        if selection:
            selection = 'weight * (%s)' % selection
        else:
            selection = 'weight'
            
        ## Fill the histograms
        for source, hist in [('mc', hmc), ('data', hdata)]:
            # hist.Sumw2()
            hist.SetStats(0)
            expression = hvar.GetName() + '>>' + hist.GetName()
            self.w.data(source).tree().Draw(expression, selection, 'goff')

        ## Normalize mc to data.
        hmc.Scale(hdata.Integral() / hmc.Integral())

        ## Add the histograms to the workspace
        self.w.Import(hmc)
        self.w.Import(hdata)

        hmc = self.w.obj(hmc.GetName())
        hdata = self.w.obj(hdata.GetName())

        ## Make the canvas
        canvas = canvases.next('c_' + name)
        hmc.Draw('hist')
        hdata.Draw('same e0')
        self.draw_legend({hdata: 'Data', hmc: 'Simulation'})

        self.w.Import(canvas, canvas.GetName())
    ## End of Fitter.plot_mmg_mass().    


    #___________________________________________________________________________
    def draw_legend(self, items):
        '''Draw a legend given the items.'''
        legend = Legend(items.keys(), items.values())
        for entry in list(legend.GetListOfPrimitives()):
            if entry.GetLabel() != 'Data':
                entry.SetOption('l')
        legend.Draw()
        self.legend = legend
    ## End of Fitter.draw_legend().
    

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
    canvases.update()
    print "Exiting rescaling fitter test with success."
    import user
    
