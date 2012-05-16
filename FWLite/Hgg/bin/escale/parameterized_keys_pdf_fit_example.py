'''
This example takes a RooDataSet from a RooWorkspace in TFile,
splits it in two halfs by odd and even events,
trains ParameterizedKeysPdfs to both halfs and fits
their mode and effective sigmas to the independent halfs to
get their estimates.  It creates plots showing the data with the fitted
model and resulting values.

USAGE: python -i parameterized_keys_pdf_fit_example.py

Jan Veverka, Caltech, 16 March 2012
'''

import os
import ROOT
import FWLite.Tools.roofit as roo

import FWLite.Tools.cmsstyle as cmsstyle
import FWLite.Tools.canvases as canvases
import FWLite.Tools.legend as legend
import FWLite.Tools.latex as latex

from FWLite.Tools.parameterizedkeyspdf import ParameterizedKeysPdfs


#______________________________________________________________________________
def getdata():
    '''
    Returns the RooDataSet to be used.
    '''
    path = '/raid2/veverka/yyTrees/escale'
    filename = ('zeeWsShapev1Smear.DoubleElectronRun2011AB16Jan2012v1AOD.'
                'etcut25.corr451.eleid1.datapu0.mcpu0.m70to110.scale2.'
                'smear0.root')
    workspacename = 'zeeShape'
    datasetname = 'rds_mpair_ebeb'
    
    with ROOT.TFile.Open(os.path.join(path, filename)) as f:
        data = f.Get(workspacename).data(datasetname).Clone()
        
    return data        
## End of getdata().


#______________________________________________________________________________
def main():
    '''This is the entry point to execution.'''
    print 'Welcome to parameterized_keys_pdf_fit_example'
    data = getdata()
    print 'Exiting parameterized_keys_pdf_fit_example with success!'
## End of main().


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user

## End of the module
