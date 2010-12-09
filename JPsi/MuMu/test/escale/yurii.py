from ROOT import *

mcTree = TTree("mcTree", "MC tree")
dataTree = TTree("dataTree", "tree with real data")

mcTree.ReadFile("ikRatio_LyonSelection_Zmumu-powheg-Summer10.txt", "ik/F:pt:eta:r9")
dataTree.ReadFile("ikRatio-LyonSelection_data34ipb.txt", "ik/F:pt:eta:r9")

def nll(scale, selection=""):
    "Calculate the negative log likelihood of data with PDF from MC"
    mcTree.Draw("(1. + %f/100.) * ik >> hmc(200,0,2)" % scale, selection, "goff")
    hmc = gDirectory.Get("hmc")
    ## Normalize area to 1
    hmc.Scale( 1./hmc.Integral()/hmc.GetBinWidth(1) )
    ## Fit with Gauss; use the fit to get an estimate for the tails where there is no data
    hmc.Fit("gaus", "Q0")
    fit = hmc.GetFunction("gaus")
    ## Get the real data
    dataTree.Draw("ik>>hdata(20,0,2)", selection, "goff")
    ## Sum the negative log likelihood over all the data
    sum = 0.
    for i in range( dataTree.GetSelectedRows() ):
        ik = dataTree.GetV1()[i]
        likelihood = hmc.Interpolate(ik)
        ## Make sure we have a positive likelihood value
        if likelihood <= 0.:
            likelihood = fit.Eval(ik)
        sum -= log(likelihood)
    return sum

def chi2(scale, selection="", nbins = 20, xmin = 0., xmax = 2.):
    "Calculate the chi2 test of data and MC as a function of the scale"
    mcTree.Draw("(1. + %f/100.) * ik >> hmc(%d,%d,%d)" % (scale, nbins, xmin, xmax), selection, "goff")
    hmc = gDirectory.Get("hmc")
    ## Get the real data
    dataTree.Draw("ik>>hdata(%d,%d,%d)" % (nbins, xmin, xmax), selection, "goff")
    hdata = gDirectory.Get("hdata")
    ## Normalize MC to data
    hmc.Scale( hdata.Integral() / hmc.Integral() )
    return hmc.ChiTest(hdata)

if __name__ == "__main__": import user