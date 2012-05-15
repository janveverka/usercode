import ROOT
ROOT.gSystem.Load('libFWLiteTools')
#ROOT.gROOT.ProcessLine('#include "FWLite/Tools/interface/ModalInterval.h"')
ROOT.gROOT.ProcessLine('typedef vector<double> VDouble')
# ModalInterval = ROOT.cit.ModalInterval
ModalInterval = ROOT.ModalInterval
VDouble = ROOT.VDouble
