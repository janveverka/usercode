import copy
import FWCore.ParameterSet.Config as cms
from ElectroWeakAnalysis.MultiBosons.Histogramming.histoTools_cff import *
from ElectroWeakAnalysis.MultiBosons.Histogramming.compositeKineHistos_cff import *

testAnalyzer = makeHistoAnalyzer("CandViewHistoAnalyzer",
  histos = compositeKineHistos,
  srcName = "dielectrons",
)
