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
    cb1 = ws.factory("""CBShape::cb1(
        mass[60, 120],
        cbBias[0, -10, 10],
        cbSigma[0.7, 0.001, 10],
        cbCut[1.5, 0, 10],
        cbPower[1.5, 0.1, 10])""")
    cb2 = ws.factory("""CBShape::cb2(
        mass[60, 120],
        cbBias[0, -10, 10],
        cbSigma[0.7, 0.001, 10],
        cbCut[1.5, 0, 10],
        cbPower[1.5, 0.1, 10])""")
    bw = ws.factory("""BreitWigner::bw(
        mass,
        bwMean[91.19],
        bwWidth[2.5])""")
    ws.var("mass").setBins(100000, "fft")
    BWxCB1 = ws.factory("FFTConvPdf::BWxCB1(mass,bw,cb1)")
    return ws.factory("FFTConvPdf::BWxCB1xCB2(mass,BWxCB1,cb2)")

def getData(ws, bias = 1., sigma = 0.01, cut = 1.5, power = 1.5, nevents = 10000):
    w = ROOT.RooWorkspace("w")
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
    mData = bw.generate(ROOT.RooArgSet(w.var("m")), moreEvents)
    res1Data = cb.generate(ROOT.RooArgSet(w.var("res")), moreEvents)
    res2Data = cb.generate(ROOT.RooArgSet(w.var("res")), moreEvents)
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
    model = ws.pdf("BWxCB1xCB2")
    paramsToShow = ROOT.RooArgSet(
        *[ws.var(x) for x in "cbBias cbSigma cbCut cbPower".split()]
        )
    model.paramOn(plot,
        Format("NEU", AutoPrecision(2)),
        Parameters(paramsToShow),
        Layout(.67, .97, .97)
        )
    model.plotOn(plot)
    return plot

def test():
    ws = ROOT.RooWorkspace("testws")
    buildModel(ws)
    getData(ws)
    ws.Print()
    mass = ws.var("mass")
    mframe = mass.frame()
    #c1 = ROOT.TCanvas()
    #c1.Divide(2,2)
    #c1.cd(1)
    mframe.Draw()
    #c1.cd(2)
    ws.data("data").plotOn(mframe)
    BWxCB = ws.pdf("BWxCB")
    BWxCB.fitTo(ws.data("data"))
    BWxCB.plotOn(mframe)
    #ws.pdf("bw").plotOn(mframe, ROOT.RooFit.LineColor(ROOT.kRed))
    mframe.Draw()
    return ws

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
exec(usingNamespaceRooFit())
params = []

N = 1000


xvalues = [0.01, 0.01, 0.01] # + 0.005*i for i in range(20)]
for sigma in xvalues:
    ws = ROOT.RooWorkspace("ws")
    params.append(copy.deepcopy(getModelParams(ws, nevents=N, sigma=sigma)))
    ws.writeToFile("resolutionScan2.root", False)

#xvalues = [0.95 + 0.005*i for i in range(21)]
#for bias in xvalues:
    #ws = ROOT.RooWorkspace("ws")
    #params.append(copy.deepcopy(getModelParams(ws, nevents=N, bias=bias, sigma=0.01)))
    #ws.writeToFile("scaleScan_100k.root", False)

#for power in [1.0 + 0.1*i for i in range(11)]:
    #ws = ROOT.RooWorkspace("ws")
    #params.append(copy.deepcopy(getModelParams(ws, nevents=N, power=power)))
    #ws.writeToFile("powerScan_100k.root", False)

#for cut in [0.1 + 0.1*i for i in range(21)]:
    #ws = ROOT.RooWorkspace("ws")
    #params.append(copy.deepcopy(getModelParams(ws, nevents=N, cut=cut)))
    #ws.writeToFile("cutScan_100k.root", False)

#getFitPlot(ws, "mass", ).Draw()

print "# x, xerr, m0(%), m0_err(%), sigma, sigma_err(%), cut, cut_err, power, power_err"
for i in range(len(xvalues)):
    print "% 5.3g   0.0   " % (100*(xvalues[i]-1.),),
    factor = 100./91.19
    print "% 8.4g %8.2g   " % (params[i][0].getVal() * factor, params[i][0].getError() * factor),
    factor = factor * math.sqrt(2)
    print "% 8.4g %8.2g   " % (params[i][1].getVal() * factor, params[i][1].getError() * factor),
    for j in range(2, 4):
        print "% 8.4g %8.2g   " % (params[i][j].getVal(), params[i][j].getError(),),
    print
if __name__ == "__main__": import user