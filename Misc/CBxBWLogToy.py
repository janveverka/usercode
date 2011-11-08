import copy
import sys
import math
## Switch to ROOT's batch mode
#sys.argv.append("-b")

from ROOT import *
from JPsi.MuMu.common.roofit import *
gSystem.Load('libJPsiMuMu')

setattr(RooWorkspace, "Import", getattr(RooWorkspace, "import"))

def buildModel(wspace):
    mass = wspace.factory('mass[60, 120]')
    logmu = wspace.factory("logmu[-0.5,0.5]")
    ## Mass as a function of logmu
    massf = wspace.factory("FormulaVar::massf('91.2 * exp(logmu)', {logmu})")
    ## logmu as a function of mass
    logmuf = wspace.factory("FormulaVar::logmuf('log(mass/91.2)', {mass})")
    resf = wspace.factory("FormulaVar::resf('exp(2*logmu)', {logmu})")
    
    logmu.setBins(10000, "fft")
    bw = wspace.factory("""BreitWigner::bw(
        massf,
        bwMean[91.19],
        bwWidth[2.5])""")
    cb1 = wspace.factory("""RooLogSqrtCBShape::cb1(
        logmu,
        #Deltam[1, 0.5, 1.5],
        #sigma[0.02, 0.001, 0.1],
        #alpha[1.5, 0, 10],
        n[1.5, 0.1, 10])""")
    cb2 = wspace.factory("RooLogSqrtCBShape::cb2(logmu, #Deltam, #sigma, #alpha, n)")
    bwxcb1 = wspace.factory("FCONV::bwxcb1(logmu,bw,cb1)")
    bwxcb1.setBufferFraction(0.25)
    wspace.Print()

    # bwxcb1xcb2 = wspace.factory("FFTConvPdf::bwxcb1xcb2(logmuf,logmu,bwxcb1,cb2)")
    ## Start hack to workaround RooWorkspace::factory bug preventing usage
    ## of the RooFFTConvPdf constructor with 4 arguments
    bwxcb1xcb2 = RooFFTConvPdf('bwxcb1xcb2', 'bwxcb1xcb2',
                               logmuf, logmu, bwxcb1, cb2)
    wspace.Import(bwxcb1xcb2)
    bwxcb1xcb2.setBufferFraction(0.25)
    wspace.Print()
    return bwxcb1xcb2

def getData(ws, bias = 1., sigma = 0.01, cut = 1.5, power = 1.5, nevents = 5000):
    w = RooWorkspace("w")
    cb = w.factory("""CBShape::cbTrue(
        res[0, 2],
        bias[%f],
        sigma[%f],
        cut[%f],
        power[%f])""" % (bias, sigma, cut, power)
        )
    ws.Import(cb, RenameAllVariables("True"))
    bw = w.factory("""BreitWigner::bw(
        m[50,130],
        mean[91.12],
        width[2.5])""")
    moreEvents = int(1.1*nevents)
    mData = bw.generate(RooArgSet(w.var("m")), moreEvents)
    res1Data = cb.generate(RooArgSet(w.var("res")), moreEvents)
    res2Data = cb.generate(RooArgSet(w.var("res")), moreEvents)
    gROOT.ProcessLine("struct LeafVars {Double_t mass;};")
    leafVars = LeafVars()
    t1 = TTree("t1", "t1")
    t1.Branch("mass", AddressOf(leafVars, "mass"), "mass/D")
    for i in range(moreEvents):
        if t1.GetEntries() >= nevents: break
        m = mData.get(i).getRealValue("m")
        res1 = res1Data.get(i).getRealValue("res")
        res2 = res2Data.get(i).getRealValue("res")
        leafVars.mass = m*math.sqrt(res1*res2)
        if 60. < leafVars.mass and leafVars.mass < 120.:
            t1.Fill()
    mass = ws.var("mass")
    if not mass:
        mass = ws.factory("mass[60,120]")
    data = RooDataSet("data", "toy reco Z->ll mass", t1, RooArgSet(mass))
    ws.Import(data)
    return data

def getFitPlot(ws):
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
    workspace = ROOT.RooWorkspace("testworkspace")
    buildModel(workspace)
    getData(workspace, nevents = 100000, sigma = 0.02, bias=0.96)
    workspace.Print()
    mass = workspace.var("mass")
    mframe = mass.frame()
    #c1 = ROOT.TCanvas()
    #c1.Divide(2,2)
    #c1.cd(1)
    mframe.Draw()
    #c1.cd(2)
    data = workspace.data("data")
    data.plotOn(mframe)
    
    # BWxCB1 = workspace.pdf("bwxcb1")
    # BWxCB1.fitTo(data)
    # BWxCB1.plotOn(mframe)

    BWxCB1xCB2 = workspace.pdf('bwxcb1xcb2')
    BWxCB1xCB2.fitTo(data)
    BWxCB1xCB2.plotOn(mframe, LineColor(ROOT.kRed), LineStyle(ROOT.kDashed))
    BWxCB1xCB2.paramOn(mframe,
                       Format('NEU', AutoPrecision(2) ),
                       Layout(.55, 0.92, 0.92) )

    mframe.Draw()
    return workspace

def getModelParams(ws, bias = 1., sigma = 0.01, cut = 1.5, power = 1.5, nevents=10000):
    model = buildModel(ws)
    data = getData(ws, bias, sigma, cut, power, nevents)
    #mframe = ws.var("mass")
    model.fitTo(data, PrintLevel(-1))
    getFitPlot(ws).Draw()
    ws.var("cbBias").getVal()
    return tuple([ws.var(x) for x in "cbBias cbSigma cbCut cbPower".split()])

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
