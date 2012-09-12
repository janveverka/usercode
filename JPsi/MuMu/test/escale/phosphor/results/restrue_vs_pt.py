import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.cmsstyle as cmsstyle
import FWLite.Tools.canvases as canvases

from FWLite.Tools.xychi2fitter import XYChi2Fitter as Fitter

#==============================================================================
## Define global data attributes
_filename  = '/home/veverka/data/resTrueVsPt_HggV2Ression_NoMuonBias_EGMPaperCategories.root'
_stochastic_from_tb = 3.
_noise_from_tb      = 21.

fitters = []

ROOT.RooAbsReal.defaultIntegratorConfig().setEpsAbs(1e-08)
ROOT.RooAbsReal.defaultIntegratorConfig().setEpsRel(1e-08)

#==============================================================================
def main():
    '''
    Main entry point of execution
    '''
    do_barrel_allr9_fits()
    do_barrel_highr9_fits()
    do_endcap_allr9_fits()
## End of main().


#==============================================================================
def do_barrel_allr9_fits():
    '''
    B A R R E L   A L L   R 9
    '''
    
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EB_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel',
        title     = 'Barrel, MC Truth'
        )
    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter


    #______________________________________________________________________________
    ## S from TB
    fitter = Fitter(
        filename  = _filename,
        graphname = fitter.graphname,
        name      = fitter.name + '_stochastic_from_tb',
        title     = 'Barrel, MC Truth, S from TB'
        )
    fitter.S.setVal(_stochastic_from_tb/1.16)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)


    #______________________________________________________________________________
    ## N from TB 
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EB_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_noise_from_tb',
        title     = 'Barrel, MC Truth, N from TB'
        )
    fitter.S.setVal(ebfitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/1.37)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_barrel_allr9_fits()


#==============================================================================
def do_barrel_highr9_fits():
    '''
    B A R R E L   H I G H   R 9
    '''
    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EB_highR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_highR9',
        title     = 'Barrel, R9 > 0.94, MC Truth'
        )

    fitter.S.setVal(4.258)
    fitter.N.setVal(_noise_from_tb/1.37)
    fitter.C.setVal(0.5098)

    fitter.run()
    fitters.append(fitter)
    ebfitter = fitter


    #______________________________________________________________________________
    ## S from TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EB_highR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_highR9_stochastic_from_tb',
        title     = 'Barrel, R9 > 0.94, MC Truth, S from TB',
        yrange    = (-1, 5),
        )
    fitter.S.setVal(_stochastic_from_tb/1.16)
    fitter.N.setVal(ebfitter.N.getVal())
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)


    #______________________________________________________________________________
    ## N from TB 
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EB_highR9_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Barrel_highR9_noise_from_tb',
        title     = 'Barrel, R9 > 0.94, MC Truth, N from TB',
        yrange    = (-1, 5),
        )
    fitter.S.setVal(ebfitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/1.37)
    fitter.C.setVal(ebfitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_barrel_highr9_fits()


#==============================================================================
def do_endcap_allr9_fits():
    '''
    E N D C A P S   A L L   R 9
    '''

    #______________________________________________________________________________
    ## Float everything
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EE_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps',
        title     = 'Endcaps, MC Truth'
        )
    fitter.run()
    fitters.append(fitter)
    eefitter = fitter


    #______________________________________________________________________________
    ## Fix S to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EE_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_stochastic_from_tb',
        title     = 'Endcaps, MC Truth, S from TB'
        )
    fitter.S.setVal(_stochastic_from_tb/1.91)
    fitter.N.setVal(eefitter.N.getVal())
    fitter.C.setVal(eefitter.C.getVal())

    fitter.S.setConstant()
    fitter.run()
    fitters.append(fitter)


    #______________________________________________________________________________
    ## Fix N to TB
    fitter = Fitter(
        filename  = _filename,
        graphname = 'regressions_restrue_EE_jan2012rereco',
        name      = 'PhotonResolutionVsEt_MCTruth_Endcaps_noise_from_tb',
        title     = 'Endcaps, MC Truth, N from TB'
        )
    fitter.S.setVal(eefitter.S.getVal())
    fitter.N.setVal(_noise_from_tb/3.70)
    fitter.C.setVal(eefitter.C.getVal())

    fitter.N.setConstant()
    fitter.run()
    fitters.append(fitter)
## End of do_endcap_allr9_fits()


#==============================================================================
if __name__ == '__main__':
    main()
    import user
