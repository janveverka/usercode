'''
Usage: python -i plot_mass_spectra.py

Takes the data and the models from the official workspaces,
fits the background models to the data and plots the 
data and the fit for each category.
'''


import os
import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.canvases as canvases


#______________________________________________________________________________
def get_inputs():
    '''
    Opens the input files for 7 and 8 TeV and returns a dictionary of the 
    inputs (period) -> (root file).
    '''
    data_path = '/mnt/hadoop/user/bornheim/hgg/2012/ichep2012/common'
    filenames = {
        '7TeV': 'hgg.inputbkgdata_7TeV.root',
        '8TeV': 'hgg.inputbkgdata_8TeV.root',
        }

    inputs = {}
    for period, filename in filenames.items():
        inputs[period] = ROOT.TFile.Open(os.path.join(data_path, filename))
    return inputs
## End of get_inputs()


#______________________________________________________________________________
def get_categories(period):
    '''
    Returns the list of categories for the given period.
    '''
    catmap = {
        '7TeV': ['cat%d' % i for i in range(5)],
        '8TeV': ['mvacat%d' % i for i in range(6)],
        }
    return catmap[period]
## End of get_categories()


#______________________________________________________________________________
def get_workspaces():
    '''
    Retrieves the workspaces from the input files and returns a dictionary
    (period) -> (workspace).
    '''
    inputs = get_inputs()
    workspaces = {}
    for period, root_file in inputs.items():
        workspaces[period] = root_file.Get('wbkg')
    return workspaces
## End of get_workspaces()


#______________________________________________________________________________
def fit_model(category, period):
    '''
    Fits the background model for the given period and category to its data.
    '''
    model = get_model(category, period)
    data = get_data(category, period)
    model.fitTo(data)
## End of fit_model


#______________________________________________________________________________
def get_model(category, period):
    '''
    Gets the specified model from the inputs and returns it.
    '''
    model_name = 'bkgpdf%s_%s' % (category, period)
    return workspaces[period].pdf(model_name)
## End of get_model


#______________________________________________________________________________
def get_data(category, period):
    '''
    Gets the specified data from the inputs and returns it.
    '''
    data_name = 'data_%s_%s' % (category, period)
    return workspaces[period].data(data_name)
## End of get_model


#______________________________________________________________________________
def get_mass(period):
    '''
    Gets the specified mass variable from the inputs and returns it.
    '''
    return workspaces[period].var('CMS_hgg_mass')
## End of get_mass


#______________________________________________________________________________
def make_plot(category, period):
    '''
    Fits the background model for the given period and category to its data.
    Makes a RooPlot of the data and fit and returns it.
    '''
    model = get_model(category, period)
    data = get_data(category, period)
    mass = get_mass(period)
    mass.setBins(80)
    plot = mass.frame()
    plot.SetTitle(', '.join([category, period]))
    data.plotOn(plot)
    model.plotOn(plot)
    return plot
## End of make_plot


#______________________________________________________________________________
def main():
    '''
    Main entry point of execution.
    '''
    global workspaces
    workspaces = get_workspaces()
    plots = []
    global period, category
    for period in '7TeV 8TeV'.split():
        for category in get_categories(period):
            fit_model(category, period)
            plot = make_plot(category, period)
            canvases.next('_'.join([category, period]))
            plot.Draw()
            plots.append(plot)
## End of main


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user
