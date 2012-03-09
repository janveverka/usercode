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


#______________________________________________________________________________
def main():
    '''
    RooWorkspace main()
    This is the entry point of execution.  Returns a workspace with the results
    '''
    w = ROOT.RooWorkspace('w', 'Per-bin p-value of observed events.')
    setup_model(w)
    plot_model_and_change_parameter_values(w)
    generate_events(w)
    plot_model_and_data_overlayed(w)
    calculate_pvalues(w)
    return w
## End of main()


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
    w.factory('Gaussian::gauss(x[-10,10], mean[1,-10,10], sigma[1,0.1,10])')
    pass
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
    ## Construct plot frame in 'x'.
    xframe = w.var('x').frame(roo.Title('Gaussian PDF with data'))
    
    ## Draw the data on the frame.
    w.data('data').plotOn(xframe)
    
    ## Draw the model on the frame.
    w.pdf('gauss').plotOn(xframe)

    ## Create a canvas and draw the plot frame on it.
    canvases.next('Gaussian_PDF_with_data')
    xframe.Draw()
## End of plot_model_and_data_overlayed(w).


#______________________________________________________________________________
def calculate_pvalues(w):
    '''
    void calculate_pvalues(w)
    
    Calculates p-values of the observed number of events in each bin and
    plots its distribution using Gaussian approximation.
    '''
    canvases.next('pvalues')
## End of calculate_pvalues(w)


#______________________________________________________________________________
if __name__ == '__main__':
    ## This module is the main python module (it is not being imported).
    ## Run!
    w = main()
    w.Print()
    ## Enable user settings like tab-complete and command history.
    import user

## End of FWLite/Hgg/bin/goodness_of_fit/simple.py