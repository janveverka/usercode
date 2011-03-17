import copy
import sys
import math
## Switch to ROOT's batch mode
sys.argv.append("-b")

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
    cb = ws.factory("""CBShape::cb(
        mass[60, 120],
        cbBias[0, -10, 10],
        cbSigma[1.2, 0.001, 10],
        cbCut[1.5, 0, 10],
        cbPower[1.5, 0.1, 10])""")
    bw = ws.factory("""BreitWigner::bw(
        mass,
        bwMean[91.19],
        bwWidth[2.5])""")
    ws.var("mass").setBins(100000, "fft")
    return ws.factory("FFTConvPdf::BWxCB(mass,bw,cb)")

def getData(ws, bias = 0.0, sigma = 0.8, cut = 1.0, power = 1.8, nevents = 10000):
    w = ROOT.RooWorkspace("w")
    w.Import(ws.var("mass"))
    cb = w.factory("""CBShape::cb_true(
        mass,
        bias[%f],
        sigma[%f],
        cut[%f],
        power[%f])""" % (bias, sigma, cut, power)
        )
    bw = w.factory("""BreitWigner::bw_true(
        mass,
        mean[91.12],
        width[2.5])""")
    w.var("mass").setBins(100000, "fft")
    model = w.factory("FFTConvPdf::cb_x_bw_true(mass,bw_true,cb_true)")
    data = model.generate(ROOT.RooArgSet(w.var("mass")), nevents)
    data.SetName("data")
    ws.Import(data)
    ws.Import(cb, RenameAllVariables("true"))
    return data

def getFitPlot(ws):
    plot = ws.var("mass").frame()
    ws.data("data").plotOn(plot)
    model = ws.pdf("BWxCB")
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

def getModelParams(ws, bias = 1.005, sigma = 0.009, cut = 1., power = 1.9, nevents=10000):
    model = buildModel(ws)

    ## Set the parameter values to the "true"
    ws.var("cbBias" ).setVal(bias )
    ws.var("cbSigma").setVal(sigma)
    ws.var("cbCut"  ).setVal(cut  )
    ws.var("cbPower").setVal(power)
    
    ## Store the true params
    #ws.factory( "cbBias_true[%f]" % bias)
    #ws.factory("cbSigma_true[%f]" % sigma)
    #ws.factory(  "cbCut_true[%f]" % cut)
    #ws.factory("cbPower_true[%f]" % power)
    #ws.Print()
    observables = ROOT.RooArgSet(ws.var("mass"))
    parameters = ws.pdf("BWxCB").getParameters(observables)
    ws.defineSet("parameters", parameters)
    ws.saveSnapshot("true_parameters", parameters, ROOT.kTRUE)
    
    
    ## generate data
    data = model.generate(observables, nevents)
    data.SetName("data")
    ws.Import(data)

    ## fix the cut to 1
    ws.var("cbCut").setVal(1.0)
    ws.var("cbCut").setConstant()

    ## perform the fit
    model.fitTo(data, PrintLevel(-1))
    getFitPlot(ws).Draw()
    
    ## save the fitted parameters
    ws.saveSnapshot("fitted_parameters", parameters, ROOT.kTRUE)

    return tuple([ws.var(x) for x in "cbBias cbSigma cbCut cbPower".split()])

#ws = test()
## Shorthand for RooFit namespace functions
exec(usingNamespaceRooFit())
params = []

N = 100000
trueCut = 0.5
if len(sys.argv) > 1:
    trueCut = float(sys.argv[1])
    print "Setting true cut to %f ..." % trueCut

#ws = ROOT.RooWorkspace("ws"); params.append(copy.deepcopy(getModelParams(ws, nevents=N, sigma=0.01)))
#ws = ROOT.RooWorkspace("ws"); params.append(copy.deepcopy(getModelParams(ws, nevents=N, sigma=0.01)))
#ws = ROOT.RooWorkspace("ws"); params.append(copy.deepcopy(getModelParams(ws, nevents=N, sigma=0.01)))
#ws = ROOT.RooWorkspace("ws"); params.append(copy.deepcopy(getModelParams(ws, nevents=N, sigma=0.01)))
#ws = ROOT.RooWorkspace("ws"); params.append(copy.deepcopy(getModelParams(ws, nevents=N, sigma=0.008)))


xvalues = [0.5 + 0.1*i for i in range(20)]
for sigma in xvalues:
    ws = ROOT.RooWorkspace("ws")
    params.append(copy.deepcopy(getModelParams(ws, nevents=N, sigma=sigma, cut=trueCut)))
    ws.Print()
    ws.writeToFile("resolutionScan4_trueCut%.2f_%dk.root" % (trueCut, N/1000), False)

#xvalues = [0.95 + 0.005*i for i in range(3)]
#for bias in xvalues:
    #ws = ROOT.RooWorkspace("ws")
    #params.append(copy.deepcopy(getModelParams(ws, nevents=N, bias=bias, sigma=0.02, cut=1.8, power=1.5)))
    #ws.writeToFile("scaleScan_test10k.root", False)

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
    #print "% 5.3g   0.0   " % (100*(xvalues[i]-1.),),
    print "% 5.3g   0.0   " % (xvalues[i],),
    factor = 1
    print "% 8.4g %8.2g   " % (params[i][0].getVal() * factor, params[i][0].getError() * factor),
    factor = 1
    print "% 8.4g %8.2g   " % (params[i][1].getVal() * factor, params[i][1].getError() * factor),
    for j in range(2, 4):
        print "% 8.4g %8.2g   " % (params[i][j].getVal(), params[i][j].getError(),),
    print

if __name__ == "__main__": import user
