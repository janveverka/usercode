import copy
import sys
## Switch to ROOT's batch mode
#sys.argv.append("-b")
import JPsi.MuMu.common.roofit

from math import log
from math import sqrt

from ROOT import gSystem
from ROOT import RooWorkspace
from ROOT import RooFFTConvPdf
from ROOT import RooArgSet
from ROOT import RooDataSet
#from ROOT import 

from JPsi.MuMu.common.roofit import RenameAllVariables
from JPsi.MuMu.common.roofit import Range
from JPsi.MuMu.common.roofit import Format
from JPsi.MuMu.common.roofit import AutoPrecision
from JPsi.MuMu.common.roofit import Layout
from JPsi.MuMu.common.roofit import NumCPU

gSystem.Load('libJPsiMuMu')

setattr(RooWorkspace, "Import", getattr(RooWorkspace, "import"))

def buildModel(w):
    ## Gen level invariant mass variable
    mass = w.factory('mass[40, 140]')
    ## Transformed gen level invariant mass variable
    t = w.factory("t[%f,%f]" % (log(mass.getMin()/91.2),
                                log(mass.getMax()/91.2)))
    ## m = m(t) tranformation: mass as a function of t
    massFunc = w.factory("FormulaVar::massFunc('91.2 * exp(t)', {t})")
    ## inverse transformation t = t(m): t as a function of mass
    tFunc = w.factory("FormulaVar::tFunc('log(mass/91.2)', {mass})")
    ## 
    # resf = w.factory("FormulaVar::resf('exp(2*logmu)', {logmu})")
    
    t.setBins(10000, "fft")
    ## PDF for t defined through a transformation of the PDF for m
    tPdf = w.factory("""BreitWigner::tPdf(
        massFunc,
        bwMean[91.19],
        bwWidth[2.5])""")
    ## Start a hack to work around a RooFit limitation preventing observable
    ## transform of the 2nd PDF in the FFT convolution.  Use custom PDF
    ## RooLogCBShape instead of transforming RooCBShape.
    dt1Pdf = w.factory("""RooLogSqrtGaussian::dt1Pdf(
        t,
        #Deltam[1, 0.5, 1.5],
        #sigma[0.02, 0.001, 0.1])""")
    dt2Pdf = w.factory("RooLogSqrtGaussian::dt2Pdf(t, #Deltam, #sigma)")
    TxDT1 = w.factory("FCONV::TxDT1(t,tPdf,dt1Pdf)")
    TxDT1.setBufferFraction(0.5)
    w.Print()

    ## Ideally would like to do:
    ## model = w.factory("FCONV::model(tFunc, t, TxDT1, dt2Pdf)")
    ## But that doesn't work for some reason.
    ## Start a hack to workaround RooWorkspace::factory bug preventing such usage
    ## of the RooFFTConvPdf constructor with 4 arguments
    model = RooFFTConvPdf('model', 'model', tFunc, t, TxDT1, dt2Pdf)
    w.Import(model)
    model.setBufferFraction(0.25)
    w.Print()
    return model

def getData(workspace,
            mean1 = 1., sigma1 = 0.01,
            mean2 = 1., sigma2 = 0.01, nevents = 5000):

    ## Make a local workspace to use as a factory.
    w = RooWorkspace('w', 'w')

    ## Define the PDF's for m, f1 and f2 in m*sqrt(f1*f2)
    mPdf = w.factory("BreitWigner::mPdf(m[50,130], MZ[91.12], GammaZ[2.5])")
    f1Pdf = w.factory("Gaussian::f1Pdf(f1[0.5, 2], mean1[%f], sigma1[%f])" %
                      (mean1, sigma1))
    f2Pdf = w.factory("Gaussian::f2Pdf(f2[0.5, 2], mean2[%f], sigma2[%f])" %
                      (mean2, sigma2))

    ## Import the PDF's in the given workspace.
    workspace.Import(mPdf, RenameAllVariables("True"))
    workspace.Import(f1Pdf, RenameAllVariables("True"))
    workspace.Import(f2Pdf, RenameAllVariables("True"))

    ## Generate samples of M, F1 and F2 with a 10% margin for boundaries.
    moreEvents = int(2*nevents)
    mData = mPdf.generate(RooArgSet(w.var("m")), moreEvents, NumCPU(3))
    f1Data = f1Pdf.generate(RooArgSet(w.var("f1")), moreEvents, NumCPU(3))
    f2Data = f2Pdf.generate(RooArgSet(w.var("f2")), moreEvents, NumCPU(3))

    ## Create the new data with toy reco mass
    data = RooDataSet('data', 'toy reco Z->ll mass data',
                      RooArgSet(w.factory('mass[40,140]')))
    entry = data.get()

    ## Loop over the generated values and fill the new reco mass data.
    for i in range(moreEvents):
        ## Do we have enough entries already?
        if data.sumEntries() >= nevents:
            break
        ## Get the values of the random variables m, f1, f2.
        m  = mData.get(i).first().getVal()
        f1 = f1Data.get(i).first().getVal()
        f2 = f2Data.get(i).first().getVal()
        ## Here comes the formula!!
        mass = m * sqrt(f1*f2)
        ## Is the reco mass within its range?
        if 60. < mass and mass < 120.:
            ## Add the reco mass to the data
            entry.first().setVal(mass)
            data.addFast(entry)
    ## End of loop over the generated values
            
    workspace.Import(data)
    return data

def getFitPlot(ws1):
    ## plot = ws.var("mass").frame()
    ## ws.data("data").plotOn(plot)
    ## model = ws.pdf("BWxCB")
    ## paramsToShow = RooArgSet(
    ##     *[ws.var(x) for x in "cbBias cbSigma cbCut cbPower".split()]
    ##     )
    ## model.paramOn(plot,
    ##     Format("NEU", AutoPrecision(2)),
    ##     Parameters(paramsToShow),
    ##     Layout(.67, .97, .97)
    ##     )
    ## model.plotOn(plot)
    ## return plot
    pass

def test():
    workspace = RooWorkspace("testworkspace")

    model = buildModel(workspace)
    mass = workspace.var('mass')
    # data = model.generate(RooArgSet(mass), 1000)
    data = getData(workspace, nevents = 10000,
                   sigma1 = 0.015, mean1=1.,
                   sigma2 = 0.015, mean2=1.)


    model.fitTo(data, NumCPU(3))

    mframe = mass.frame(Range(50,130))
    data.plotOn(mframe)
    model.plotOn(mframe) #, Range(50,130)) #, LineColor(ROOT.kRed), LineStyle(ROOT.kDashed))
    model.paramOn(mframe,
                  Format('NEU', AutoPrecision(2) ),
                  Layout(.55, 0.92, 0.92) )

    mframe.Draw()
    return workspace

## def getModelParams(ws, bias = 1., sigma = 0.01, cut = 1.5, power = 1.5, nevents=10000):
##     model = buildModel(ws)
##     data = getData(ws, bias, sigma, cut, power, nevents)
##     #mframe = ws.var("mass")
##     model.fitTo(data, PrintLevel(-1))
##     getFitPlot(ws).Draw()
##     ws.var("cbBias").getVal()
##     return tuple([ws.var(x) for x in "cbBias cbSigma cbCut cbPower".split()])

#ws = test()
## Shorthand for RooFit namespace functions
#exec(usingNamespaceRooFit())
#params = []

N = 100000
#ws = RooWorkspace("ws"); params.append(copy.deepcopy(getModelParams(ws, nevents=N, sigma=0.01)))
#ws = RooWorkspace("ws"); params.append(copy.deepcopy(getModelParams(ws, nevents=N, sigma=0.01)))
#ws = RooWorkspace("ws"); params.append(copy.deepcopy(getModelParams(ws, nevents=N, sigma=0.01)))
#ws = RooWorkspace("ws"); params.append(copy.deepcopy(getModelParams(ws, nevents=N, sigma=0.01)))
#ws = RooWorkspace("ws"); params.append(copy.deepcopy(getModelParams(ws, nevents=N, sigma=0.01)))

## xvalues = [0.005 + 0.005*i for i in range(20)]
## for sigma in xvalues:
##     ws = RooWorkspace("ws")
##     params.append(copy.deepcopy(getModelParams(ws, nevents=N, sigma=sigma)))
##     ws.writeToFile("resolutionScan.root", False)

#xvalues = [0.95 + 0.005*i for i in range(21)]
#for bias in xvalues:
    #ws = RooWorkspace("ws")
    #params.append(copy.deepcopy(getModelParams(ws, nevents=N, bias=bias)))
    #ws.writeToFile("scaleScan.root", False)

#for power in [1.0, 1.25, 1.5, 1.75, 2.0]:
    #ws = RooWorkspace("ws")
    #params.append(copy.deepcopy(getModelParams(ws, nevents=N, power=power)))

#for cut in [1.0, 1.25, 1.5, 1.75, 2.0]:
    #ws = RooWorkspace("ws")
    #params.append(copy.deepcopy(getModelParams(ws, nevents=N, cut=cut)))

#getFitPlot(ws, "mass", ).Draw()

## print "# x, xerr, m0(%), m0_err(%), sigma, sigma_err(%), cut, cut_err, power, power_err"
## for i in range(len(xvalues)):
##     print "% 5.3g 0.0   " % (100*(xvalues[i]-1.),),
##     factor = 100./91.19
##     print "% 8.3g %8.2g   " % (params[i][0].getVal() * factor, params[i][0].getError() * factor),
##     factor = factor * math.sqrt(2)
##     print "% 8.3g %8.2g   " % (params[i][1].getVal() * factor, params[i][1].getError() * factor),
##     for j in range(2, 4):
##         print "% 8.3g %8.2g   " % (params[i][j].getVal(), params[i][j].getError(),),
##     print
if __name__ == "__main__":
    import user
    w = test()
