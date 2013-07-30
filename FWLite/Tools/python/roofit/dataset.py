'''
Implements the class DataSet.
Jan Veverka, MIT, jan.veverka@cern.ch
30 July 2013
'''
import ROOT
import FWLite.Tools.roofit as roo

class DataSet(ROOT.RooDataSet):
    '''
    Extends ROOT.RooDataSet with a new constructor signature that
    gives more flexibility for importing data from a TTree.
    One can specify the values of the variables and weights
    with TTreeFormula expressions and so one can specify
    additional cuts.
    '''
    pass
 
