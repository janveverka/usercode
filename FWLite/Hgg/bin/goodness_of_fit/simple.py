'''
file: FWLite/Hgg/bin/GoodnessOfFit/simple.py
--------------------------------------------

This module generates toy unbinned Normal-distributed datasets
and calculates the distribution of the p-values of the 
observed events given some binning. It produces a canvas showing
a distribution of these p-values.  This is expected to be flat.

Usage: python -i simple.h

Jan Veverka, Caltech, 9 March 2011
'''

import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.canvases as canvases
import FWLite.Tools.cmsstyle

#______________________________________________________________________________
def main():
    '''This is the entry point of execution.'''
    w = ROOT.RooWorkspace('w', 'Per-bin p-value of observed events.')
    build_model(w)
    generate_data(w)
    calculate_pvalues(w)
## End of main()

#______________________________________________________________________________
def build_model(w):
    '''
    void build_model(w)
    Creates a normal PDF in the workspace w.
    '''
    pass
## End of build_model(w)
    
#______________________________________________________________________________
def generate_data(w):
    '''
    void generate_data(w)
    Generates an unbinned dataset using the model in the workspace w.
    '''
    pass
## End of generate_data(w)
    
#______________________________________________________________________________
def calculate_pvalues(w):
    '''
    void calculate_pvalues(w)
    Calculates p-values of the observed number of events in each bin and
    plots its distribution.
    '''
    canvases.next('pvalues')
## End of calculate_pvalues(w)
    
#______________________________________________________________________________
if __name__ == '__main__':
    ## This module is the main python module (it is not being imported).
    ## Run!
    main()
    ## Enable user settings like tab-complete and command history.
    import user
