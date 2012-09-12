import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.cmsstyle as cmsstyle
import FWLite.Tools.canvases as canvases

from FWLite.Tools.xychi2fitter import XYChi2Fitter as Fitter

_filename  = '/home/veverka/data/resMC4of4VsPt_HggV2Ression_NoMuonBias_EGMPaperCategories.root'

fitters = []

#=========================
# B A R R E L
#=========================

#______________________________________________________________________________
## Float everything
fitter = Fitter(
    filename  = _filename,
    graphname = 'regressions_resmc_EB_jan2012rereco',
    name      = 'PhotonResolutionVsEt_MCFit_Barrel',
    title     = 'Barrel, MC Fit',
    systematics = 0.5,
    )
fitter.run()
fitters.append(fitter)
ebfitter = fitter


#______________________________________________________________________________
## Fix S to TB
fitter = Fitter(
    filename  = _filename,
    graphname = 'regressions_resmc_EB_jan2012rereco',
    name      = 'PhotonResolutionVsEt_MCFit_Barrel_SfromTB',
    title     = 'Barrel, MC Fit, S from TB',
    systematics = 0.5,
    )
fitter.S.setVal(3./1.16)
fitter.N.setVal(ebfitter.N.getVal())
fitter.C.setVal(ebfitter.C.getVal())

fitter.S.setConstant()
fitter.run()
fitters.append(fitter)


#______________________________________________________________________________
## Fix S to TB and N to MC
fitter = Fitter(
    filename  = _filename,
    graphname = 'regressions_resmc_EB_jan2012rereco',
    name      = 'PhotonResolutionVsEt_MCFit_Barrel_SfromTB_NfromMC',
    title     = 'Barrel, MC Fit, S from TB, N from MC',
    systematics = 0.5,
    )
fitter.S.setVal(3./1.16)
fitter.N.setVal(44.7)
fitter.C.setVal(ebfitter.C.getVal())

fitter.S.setConstant()
fitter.N.setConstant()
fitter.run()
fitters.append(fitter)


#=============================
# B A R R E L   H I G H   R 9
#=============================

#______________________________________________________________________________
## Float everything
fitter = Fitter(
    filename  = _filename,
    graphname = 'regressions_resmc_EB_highR9_jan2012rereco',
    name      = 'PhotonResolutionVsEt_MCFit_Barrel_highR9',
    title     = 'Barrel, R9 > 0.94, MC Fit',
    systematics = 0.5,
    )
fitter.run()
fitters.append(fitter)
ebfitter = fitter


##______________________________________________________________________________
### Fix S to TB
#fitter = Fitter(
    #filename  = _filename,
    #graphname = 'regressions_resmc_EB_jan2012rereco',
    #name      = 'PhotonResolutionVsEt_MCFit_Barrel_SfromTB',
    #title     = 'Barrel, MC Fit, S from TB',
    #systematics = 0.5,
    #)
#fitter.S.setVal(3./1.16)
#fitter.N.setVal(ebfitter.N.getVal())
#fitter.C.setVal(ebfitter.C.getVal())

#fitter.S.setConstant()
#fitter.run()
#fitters.append(fitter)


##______________________________________________________________________________
### Fix S to TB and N to MC
#fitter = Fitter(
    #filename  = _filename,
    #graphname = 'regressions_resmc_EB_jan2012rereco',
    #name      = 'PhotonResolutionVsEt_MCFit_Barrel_SfromTB_NfromMC',
    #title     = 'Barrel, MC Fit, S from TB, N from MC',
    #systematics = 0.5,
    #)
#fitter.S.setVal(3./1.16)
#fitter.N.setVal(44.7)
#fitter.C.setVal(ebfitter.C.getVal())

#fitter.S.setConstant()
#fitter.N.setConstant()
#fitter.run()
#fitters.append(fitter)


#=========================
# E N D C A P S
#=========================

#______________________________________________________________________________
## Float everything
fitter = Fitter(
    filename  = _filename,
    graphname = 'regressions_resmc_EE_jan2012rereco',
    name      = 'PhotonResolutionVsEt_MCFit_Endcaps',
    title     = 'Endcaps, MC Fit',
    systematics = 1.0,
    )
fitter.run()
fitters.append(fitter)
eefitter = fitter


#______________________________________________________________________________
## Fix S to TB
fitter = Fitter(
    filename  = _filename,
    graphname = 'regressions_resmc_EE_jan2012rereco',
    name      = 'PhotonResolutionVsEt_MCFit_Endcaps_SfromTB',
    title     = 'Endcaps, MC Fit, S from TB',
    systematics = 1.0,
    )
fitter.S.setVal(3./1.91)
fitter.N.setVal(eefitter.N.getVal())
fitter.C.setVal(eefitter.C.getVal())

fitter.S.setConstant()
fitter.run()
fitters.append(fitter)


#______________________________________________________________________________
## Fix S to TB and N to MC
fitter = Fitter(
    filename  = _filename,
    graphname = 'regressions_resmc_EE_jan2012rereco',
    name      = 'PhotonResolutionVsEt_MCFit_Endcaps_SfromTB_NfromMC',
    title     = 'Endcaps, MC Fit, S from TB, N from MC',
    systematics = 1.0,
    )
fitter.S.setVal(3./1.91)
fitter.N.setVal(72.3)
fitter.C.setVal(eefitter.C.getVal())

fitter.S.setConstant()
fitter.N.setConstant()
fitter.run()
fitters.append(fitter)


