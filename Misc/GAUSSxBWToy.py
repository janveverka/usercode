import copy
import sys
import math
## Switch to ROOT's batch mode
#sys.argv.append("-b")

import ROOT

def usingNamespaceRooFit():
    return """
import re
import sys
titlePattern = re.compile("^[A-Z]")
for method in dir(ROOT.RooFit):
    if callable(getattr(ROOT.RooFit, method)) and re.search(titlePattern, method):
        if hasattr(sys.modules[__name__], method):
            print "% not imported since it already exists!" % method
        else:
            setattr(sys.modules[__name__], method, getattr(ROOT.RooFit, method))
"""

setattr(ROOT.RooWorkspace, "Import", getattr(ROOT.RooWorkspace, "import"))

def buildModel(ws):
    g = ws.factory("Gaussian::g(mass[60, 120], gMean[0, -10, 10],gSigma[1.2, 0.001, 10])")
    bw = ws.factory("""BreitWigner::bw(
        mass,
        bwMean[91.19],
        bwWidth[2.5])""")
    ws.var("mass").setBins(100000, "fft")
    return ws.factory("FFTConvPdf::BWxG(mass,bw,g)")

def getData(ws, mean = 1., sigma = 0.02, nevents = 10000):
    w = ROOT.RooWorkspace("w")
    g = w.factory("Gaussian::gTrue(res[0, 2],gMean[%f],gSigma[%f])" % (mean, sigma))
    ws.Import(g, RenameAllVariables("True"))
    bw = w.factory("""BreitWigner::bw(
        m[50,130],
        mean[91.12],
        width[2.5])""")
    moreEvents = int(1.1*nevents)
    mData = bw.generate(ROOT.RooArgSet(w.var("m")), moreEvents)
    res1Data = g.generate(ROOT.RooArgSet(w.var("res")), moreEvents)
    res2Data = g.generate(ROOT.RooArgSet(w.var("res")), moreEvents)
    ROOT.gROOT.ProcessLine("struct LeafVars {Double_t mass;};")
    leafVars = ROOT.LeafVars()
    t1 = ROOT.TTree("t1", "t1")
    t1.Branch("mass", ROOT.AddressOf(leafVars, "mass"), "mass/D")
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
    data = ROOT.RooDataSet("data", "toy reco Z->ll mass", t1, ROOT.RooArgSet(mass))
    ws.Import(data)
    return data

def getFitPlot(ws):
    plot = ws.var("mass").frame()
    ws.data("data").plotOn(plot)
    model = ws.pdf("BWxG")
    paramsToShow = ROOT.RooArgSet(
        *[ws.var(x) for x in "gMean gSigma".split()]
        )
    model.paramOn(plot,
        Format("NEU", AutoPrecision(2)),
        Parameters(paramsToShow),
        Layout(.67, .97, .97)
        )
    model.plotOn(plot)
    return plot

def getModelParams(ws, mean = 1., sigma = 0.02, nevents=10000):
    model = buildModel(ws)
    data = getData(ws, mean, sigma, nevents)
    #mframe = ws.var("mass")
    model.fitTo(data, PrintLevel(-1))
    getFitPlot(ws).Draw()
    ROOT.gPad.Update()
    ws.var("gMean").getVal()
    return tuple([ws.var(x) for x in "gMean gSigma".split()])

## Shorthand for RooFit namespace functions
exec(usingNamespaceRooFit())
params = []

N = 100000

scale = 1.00
resolution = 0.01

xvalues = [0.005 + 0.001*i for i in range(5)]
for sigma in xvalues:
    ws = ROOT.RooWorkspace("ws")
    params.append(copy.deepcopy(getModelParams(ws, nevents=N, sigma=sigma, mean=scale)))
    ws.writeToFile("GxBWResolutionScan_test10k.root", False)

# xvalues = [0.95 + 0.005*i for i in range(21)]
# for scale in xvalues:
#     ws = ROOT.RooWorkspace("ws")
#     params.append(copy.deepcopy(getModelParams(ws, nevents=N, mean=scale, sigma=resolution)))
#     ws.writeToFile("GxBWScaleScan_resolution_0.01_10k.root", False)

print "# x, xerr, mean(%), mean_err(%), sigma, sigma_err(%)"
for i in range(len(xvalues)):
    print "% 5.3g   0.0   " % (100*(xvalues[i]),),
    factor = 100./91.19
    print "% 8.4g %8.2g   " % (params[i][0].getVal() * factor, params[i][0].getError() * factor),
    factor = factor * math.sqrt(2)
    print "% 8.4g %8.2g   " % (params[i][1].getVal() * factor, params[i][1].getError() * factor)
if __name__ == "__main__": import user
