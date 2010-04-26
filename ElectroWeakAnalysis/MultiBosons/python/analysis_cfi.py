import FWCore.ParameterSet.Config as cms
from ElectroWeakAnalysis.MultiBosons.analyzers.muonAnalyzer_cfi import *
from ElectroWeakAnalysis.MultiBosons.analyzers.photonAnalyzer_cfi import *
from ElectroWeakAnalysis.MultiBosons.analyzers.dimuonAnalyzer_cfi import *
from ElectroWeakAnalysis.MultiBosons.analyzers.mmgAnalyzer_cfi import *

p = cms.Path(muonAnalysis+
  photonAnalysis+
  dimuonAnalysis+
  mmgAnalysis
)