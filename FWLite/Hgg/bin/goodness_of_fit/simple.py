'''
file: FWLite/Hgg/bin/goodness_of_fit/simple.py
--------------------------------------------

This module generates toy unbinned Normal-distributed datasets
and calculates the distribution of the p-values of the 
observed events given some binning. It produces a canvas showing
a distribution of these p-values.  This is expected to be flat.

To a large extent, this is re-write of the RooFit tuturial macro rf101_basics.C
in PyROOT, see
http://root.cern.ch/root/html/tutorials/roofit/rf101_basics.C.html

The main modifications are (a) refactoring of the code in
smaller routines that communicate with each other via a workspace and
(b) the actual p-value calculation.

Usage: python -i simple.h

Jan Veverka, Caltech, 9 March 2011
'''

import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.canvases as canvases
import FWLite.Tools.cmsstyle

from FWLite.Tools.roochi2calculator import RooChi2Calculator

#______________________________________________________________________________
def main():
    '''
    RooWorkspace main()
    This is the entry point of execution.  Returns a workspace with the results
    '''
    ntoys = 500
    wlist = []    
    for i in range(ntoys):
        w = ROOT.RooWorkspace('w%d' % i, 
                              'Per-bin p-value toy %d' % i)
        setup_model(w)
        generate_events(w)    
        calculate_pvalue_graph(w)
        make_pvalue_hist(w)        
        wlist.append(w)
   
    pvalue_hist_tot = wlist[0].obj('pvalue_hist').Clone('pvalue_hist_tot')
    for w in wlist[1:]:
        pvalue_hist_tot.Add( w.obj('pvalue_hist') )
        
    plot_all(wlist[0])

    canvases.next('pvalue_hist_tot')
    pvalue_hist_tot.Draw('e0')
    canvases.update()
    
    return wlist, pvalue_hist_tot    
## End of main()


def plot_all(w):
    plot_model_and_change_parameter_values(w)
    plot_model_and_data_overlayed(w)
    plot_pulls_and_pvalues(w)
## End of plot_all(w).  


#______________________________________________________________________________
def setup_model(w):
    '''
    void setup_model(w)
    
    Creates a normal PDF `gauss' = N(x|mean, sigma) together with 
    its observable `x' and parameters `mean' and `sigma' in the given 
    workspace w.
    
    Preconditions: There is no object named `guass' in the workspace.
    
    Postconditions: The following object are created in the workspace:
        - RooRealVar x = 0 with range [-10, 10]
        - RooRealVar mean = 1 with range [-10, 10]
        - RooRealVar sigma = 1 with range [0.1, 10]
        - RooGaussian gauss = N(x|mean, sigma)
    '''
    w.factory('Gaussian::gauss(x[-10,10], mean[1,-10,10], sigma[4,0.1,10])')
## End of build_model(w)
    

#______________________________________________________________________________
def plot_model_and_change_parameter_values(w):
    '''
    void plot_model_and_change_parameter_values(w)
    
    Plots model `gaus' and changes the parameter values.
    '''
    ## Construct plot frame in 'x'
    xframe = w.var('x').frame(roo.Title('Gaussian PDF'))
    
    ## Plot gauss in frame (i.e. in x).
    w.pdf('gauss').plotOn(xframe)
    
    ## Change the value of sigma to 3.
    w.var('sigma').setVal(3)
    
    ## Plot gauss in frame (i.e. in x) and draw frame on canvases.
    w.pdf('gauss').plotOn(xframe, roo.LineColor(ROOT.kRed))
    
    ## Create a canvas and draw the plot frame on it.
    canvases.next('Gaussian_PDF')
    xframe.Draw()
## End of plot_model_and_change_parameter_values(w).

#______________________________________________________________________________
def generate_events(w):
    '''
    void generate_events(w)
    
    Generates an unbinned dataset of 10000 samplings of `x' using 
    the PDF `gauss' from the given workspace `w'.
    
    Preconditions: The workspace contains the PDF `gauss' of the observable `x'
        and there is no object `data' present.
        
    Postconditions: The RooDataset `data' is added to the workspace.
    '''
    ## Define the set of observables that will be sampled.
    observables = ROOT.RooArgSet(w.var('x'))
    
    ## Sample the PDF.
    data = w.pdf('gauss').generate(observables, 10000)
    
    ## Rename the event sample to `data' and add it to the workspace.
    data.SetName('data')
    w.Import(data)
    pass
## End of generate_data(w).


#______________________________________________________________________________
def plot_model_and_data_overlayed(w):
    '''
    void plot_model_and_data_overlayed(w)
    
    Plots model `gaus' and dataset `data' overlayed on top of each other.
    
    Preconditions: Model and data are present in the given workspace w.
    
    Postconditions: A canvas `Gaussian_PDF_with_data' is created and displayed.
    '''
    xframe = get_plot_of_data_overlayed_with_model(w)

    ## Create a canvas and draw the plot frame on it.
    canvases.next('Gaussian_PDF_with_data')
    xframe.Draw()
## End of plot_model_and_data_overlayed(w).




#______________________________________________________________________________
def get_plot_of_data_overlayed_with_model(w):
    '''
    RooPlot get_plot_data_overlayed_with_model(w)
    
    Returns a RooPlot of of data overlayed with the model.  It takes if from
    the workspace if present, creates it and adds it to the workspace 
    if needed.
    
    Preconditions: Data and model are in the workspace.
    
    Postconditions: RooPlot gauss_with_data is added to the workspace.
    '''
    
    ## Retrieve the plot from the workspace.
    name = 'gauss_with_data'
    xframe = w.obj(name)
    
    ## Check if it was actually there.
    if xframe:
        ## We are done.
        return xframe
    else:
        ## Construct plot frame in 'x'.
        xframe = w.var('x').frame(roo.Name(name),
                                  roo.Title('Gaussian PDF with data'))
        
        ## Draw the data on the frame.
        w.data('data').plotOn(xframe)
        
        ## Draw the model on the frame.
        w.pdf('gauss').plotOn(xframe)
        
        w.Import(xframe)
        return xframe
## End of get_plot_data_overlayed_with_model(w).



#______________________________________________________________________________
def calculate_pvalue_graph(w):
    '''
    void calculate_pvalue_graph(w)
    
    Calculates p-values of the observed number of events in each bin and
    plots its distribution using Gaussian approximation.
    '''
    ## Get a plot with data and PDF overlayed for a given binning.
    plot = get_plot_of_data_overlayed_with_model(w)
    
    ## Initialize the chi2 calculator.
    chi2_calculator = RooChi2Calculator(plot)
    
    ## Get a graph of the pulls (data - expected) / sqrt(expected)
    ## where expected is an integral over a bin.
    pull_graph = chi2_calculator.pullHist()
    
    ## Create a new graph to store the pull values
    pvalue_graph = ROOT.TGraph(pull_graph.GetN())
    
    ## Loop over the pulls
    for i in range(pull_graph.GetN()):
        ## Get the pull for bin i
        x = pull_graph.GetX()[i]
        pull = pull_graph.GetY()[i]
        ## Calculate the p-value using the complementary error function
        pvalue = ROOT.TMath.Erfc(ROOT.TMath.Abs(pull))
        pvalue_graph.SetPoint(i, x, pvalue)

    ## Add the pull and pvalue graphs to the workspace
    w.Import(pull_graph, 'pull_graph')
    w.Import(pvalue_graph, 'pvalue_graph')
## End of calculate_pvalue_graph(w)


#______________________________________________________________________________
def make_pvalue_hist(w):
    '''
    void make_pvalue_hist(w)
    
    Takes the graph of pulls from the workspace and makes a histogram of the
    pull values it contains.
    
    Preconditions: The workspace contains the graph `pvalue_graph'.
    
    Postconditions: The histogram of `pvalue_hist' is added to the workspace.
    '''
    pvalue_graph = w.obj('pvalue_graph')
    
    pvalue_hist = ROOT.TH1F('pvalue_hist', 'Gaussian;p-value;# of bins',
                            50, 0, 1)
                          
    for i in range(pvalue_graph.GetN()):
        pvalue_hist.Fill( pvalue_graph.GetY()[i] )
    
    w.Import(pvalue_hist, 'pvalue_hist')
## End of make_pvalue_hist(w).


#______________________________________________________________________________
def plot_pulls_and_pvalues(w):
    '''
    void plot_pulls_and_pvalues(w)
    
    Plots the graphs of pulls and pvalues above each other.
    
    Preconditions: The `pull_graph' and `pvalue_graph' are in the given 
        workspace.
        
    Postconditions: There is a canvas with the plotted graphs.
    '''
    ## Get the graphs from the workspace.
    pull_graph = w.obj('pull_graph')
    pvalue_graph = w.obj('pvalue_graph')
    pvalue_hist = w.obj('pvalue_hist')
        
    ## Create a new canvas to display pulls and pvalues together.
    canvas = canvases.next('pulls_and_pvalue_graph')
    canvas.SetGrid()
    canvas.Divide(1,2)

    ## Plot the pull graph.
    pull_graph.SetTitle('')
    canvas.cd(1)
    pull_graph.Draw('ap')
    pull_graph.GetXaxis().SetTitle('x')
    pull_graph.GetYaxis().SetTitle('(observed - expected) / #sqrt{expected}')

    ## Plot the p-value graph.
    pvalue_graph.SetTitle('')
    canvas.cd(2)
    pvalue_graph.Draw('ap')
    pvalue_graph.GetXaxis().SetTitle('x')
    pvalue_graph.GetYaxis().SetTitle('p-value')
    
    ## Plot the p-value histogram.
    canvases.next('pvalue_hist')
    pvalue_hist.Draw()
    
## End of plot_pulls_and_pvalues(w).


#______________________________________________________________________________
if __name__ == '__main__':
    ## This module is the main python module (it is not being imported).
    ## Run!
    results = main()
    ## Enable user settings like tab-complete and command history.
    import user

## End of FWLite/Hgg/bin/goodness_of_fit/simple.py