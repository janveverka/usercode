### Black Magic to Make RooFit work on MacOS X --------------------------------
import sys
if sys.platform == 'darwin':
    try:
        import libRooFit
    except ImportError:
        pass

#------------------------------------------------------------------------------
## Common ROOT objects
## Globals
from ROOT import gDirectory, gROOT, gStyle

## Classes
from ROOT import TChain, TCanvas, TH1F, THStack, TLegend, TF1, TGraphErrors, \
                 TTree, Form
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
