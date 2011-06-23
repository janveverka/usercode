#------------------------------------------------------------------------------
## Common ROOT objects
from ROOT import gDirectory, gROOT, gStyle
from ROOT import TChain, TCanvas, TH1F, THStack, TLegend, TF1, TGraphErrors
## Colors
from ROOT import kBlue, kViolet, kMagenta, kPink, kRed, kOrange, kYellow
from ROOT import kSpring, kGreen, kTeal, kCyan, kAzure, kWhite, kBlack, kGray
from ROOT import kTRUE, kFALSE, TLatex
#------------------------------------------------------------------------------
## Common RooFit objects
from ROOT import RooRealVar, RooArgSet, RooArgList, RooDataSet, RooCategory, \
                 RooWorkspace, RooAbsData

from array import array

## Workaround the python's `import' keyword
setattr( RooWorkspace, 'Import', getattr(RooWorkspace, 'import') )
