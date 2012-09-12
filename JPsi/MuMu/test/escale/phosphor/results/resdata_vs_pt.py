import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.cmsstyle as cmsstyle
import FWLite.Tools.canvases as canvases

from FWLite.Tools.xychi2fitter import XYChi2Fitter as Fitter

_filename  = '/home/veverka/data/resDataVsPt_HggV2Ression_NoMuonBias_EGMPaperCategories.root'
_stochastic_from_tb = 3.
_noise_from_mc_barrel = 44.0854 # +/- 3.5842
_noise_from_mc_endcaps = 76.6281 # +/- 5.87941

fitters = []

#=========================
# B A R R E L
#=========================

#______________________________________________________________________________
## Float everything
fitter = Fitter(
    filename  = _filename,
    graphname = 'regressions_resdata_EB_jan2012rereco',
    name      = 'PhotonResolutionVsEt_DataFit_Barrel',
    title     = 'Barrel, Data Fit',
    systematics = 0.5,
    )
fitter.run()
fitters.append(fitter)
ebfitter = fitter


#______________________________________________________________________________
## Fix S to TB
fitter = Fitter(
    filename  = _filename,
    graphname = 'regressions_resdata_EB_jan2012rereco',
    name      = 'PhotonResolutionVsEt_DataFit_Barrel_SfromTB',
    title     = 'Barrel, Data Fit, S from TB',
    systematics = 0.5,
    )
fitter.S.setVal(_stochastic_from_tb/1.16)
fitter.N.setVal(ebfitter.N.getVal())
fitter.C.setVal(ebfitter.C.getVal())

fitter.S.setConstant()
fitter.run()
fitters.append(fitter)


#______________________________________________________________________________
## Fix S to TB and N to MC
fitter = Fitter(
    filename  = _filename,
    graphname = 'regressions_resdata_EB_jan2012rereco',
    name      = 'PhotonResolutionVsEt_DataFit_Barrel_SfromTB_NfromMC',
    title     = 'Barrel, Data Fit, S from TB, N from MC',
    systematics = 0.5,
    )
fitter.S.setVal(_stochastic_from_tb/1.16)
fitter.N.setVal(_noise_from_mc_barrel)
fitter.C.setVal(ebfitter.C.getVal())

fitter.S.setConstant()
fitter.N.setConstant()
fitter.run()
fitters.append(fitter)


#=========================
# E N D C A P S
#=========================

#______________________________________________________________________________
## Float everything
fitter = Fitter(
    filename  = _filename,
    graphname = 'regressions_resdata_EE_jan2012rereco',
    name      = 'PhotonResolutionVsEt_DataFit_Endcaps',
    title     = 'Endcaps, Data Fit',
    systematics = 1.0,
    )
fitter.run()
fitters.append(fitter)
eefitter = fitter


#______________________________________________________________________________
## Fix S to TB
fitter = Fitter(
    filename  = _filename,
    graphname = 'regressions_resdata_EE_jan2012rereco',
    name      = 'PhotonResolutionVsEt_DataFit_Endcaps_SfromTB',
    title     = 'Endcaps, Data Fit, S from TB',
    systematics = 1.0,
    )
fitter.S.setVal(_stochastic_from_tb/1.91)
fitter.N.setVal(eefitter.N.getVal())
fitter.C.setVal(eefitter.C.getVal())

fitter.S.setConstant()
fitter.run()
fitters.append(fitter)


#______________________________________________________________________________
## Fix S to TB and N to MC
fitter = Fitter(
    filename  = _filename,
    graphname = 'regressions_resdata_EE_jan2012rereco',
    name      = 'PhotonResolutionVsEt_DataFit_Endcaps_SfromTB_NfromMC',
    title     = 'Endcaps, Data Fit, S from TB, N from MC',
    systematics = 1.0,
    )
fitter.S.setVal(_stochastic_from_tb/1.91)
fitter.N.setVal(_noise_from_mc_endcaps)
fitter.C.setVal(eefitter.C.getVal())

fitter.S.setConstant()
fitter.N.setConstant()
fitter.run()
fitters.append(fitter)


