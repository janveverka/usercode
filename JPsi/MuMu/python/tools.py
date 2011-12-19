import ROOT
import JPsi.MuMu.common.roofit as roo

ROOT.gSystem.Load('libJPsiMuMu')
ROOT.gROOT.ProcessLine('#include "JPsi/MuMu/interface/tools.h"')
effSigma = ROOT.effSigma

##------------------------------------------------------------------------------
def pdf_effsigma(pdf, obs):
    'Returns the effective sigma of pdf of observable obs.'
    ## TODO: use the pdf itself instead of sampling it into a histogram?
    hist = pdf.createHistogram(obs.GetName(), 10000)
    hist.Scale(10000)
    ret = effSigma(hist)
    hist.Delete()
    return ret
## End of pdf_effsigma

##------------------------------------------------------------------------------
def pdf_mode(pdf, obs,
            ## Trick to have static variables zero and minusone
            zero = ROOT.RooConstVar('zero', 'zero', 0),
            minusone = ROOT.RooConstVar('minusone', 'minusone', -1)):
    'Returns the mode of a given pdf in observable RooAbsArg obs.'
    ## Set all parameters constant, remembering their constantness
    saveconst = []
    params = pdf.getParameters(ROOT.RooArgSet(obs))
    itpar = params.createIterator()
    for i in range(params.getSize()):
        p = itpar()
        saveconst.append(p.isConstant())
        p.setConstant(True)
    ## Create the function to be minimized: -pdf
    minuspdf = ROOT.RooPolyVar('minus_' + pdf.GetName(),
                               'Minus ' + pdf.GetTitle(),
                               pdf, ROOT.RooArgList(zero, minusone))
    ## Find the minimum with minuit
    minuit = ROOT.RooMinuit(minuspdf)
    minuit.setPrintLevel(-1)
    minuit.migrad()
    ## Reset the constantness of the parameters of the pdf and
    itpar.Reset()
    for i in range(params.getSize()):
        itpar().setConstant(saveconst[i])
    return obs.getVal()
## End of pdf_mode
