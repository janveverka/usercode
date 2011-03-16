import array
import math
import ROOT
from ROOT import *
from parseCBxBWOutput import xdata, ydata, exdata, eydata, paramInfo

#gStyle.SetPadLeftMargin(0.2)
#gStyle.SetTitleYOffset(1.5)


## key=filename, value=(workspace name, list of cycles)
dataSource = {
    #"scaleScan2_100k.root": ("ws", range(26,30) + range(31,47)), # cycle 30 doesn't converge nicely
    #"scaleScan2_10k.root": ("ws", range(1,7) + range(8,16) + range(18,22)),
#     "resolutionScan.root": ("ws", [1] + range(3,21)),
#     "resolutionScan2.root": ("ws", [10]),
    #"cutScan_100k.root": ("ws", range(1,22)),
    #"powerScan_100k.root": ("ws", range(1,11)),
    #"resolutionScan2.root": ("ws", [10]),
    "resolutionScan4_trueCut1.00_20k.root": ("ws", range(1,6) ),
}

xname = "resolution"
xunit = "(Gev)"
# fitrange = (0, 10.5)
fitrange = (0, 2)

wsyname = {
    "scale"     : "cbBias" ,
    "resolution": "cbSigma",
    "cut"       : "cbCut"  ,
    "power"     : "cbPower"
    }

wsxname = {}
for key, value in wsyname.items():
    wsxname[key] = value + "_true"

xtransform = {
    "scale": lambda x: x / 0.9119,
    "resolution": lambda x: x,
    "cut": lambda x: x,
    "power": lambda x: x
    }

ytransform = {
    "scale": lambda x: x / 0.9119,
    "resolution": lambda x: x,
    "cut": lambda x: x,
    "power": lambda x: x
    }

alldata = (ydata, xdata, eydata, exdata) = ({}, {}, {}, {})
for yname in wsyname.keys():
    for data in alldata:
        data[yname] = []

for fileName, (workspaceName, cycles) in dataSource.items():
    file = TFile(fileName)

    for cycle in cycles:
        ws = file.Get("%s;%d" % (workspaceName, cycle) )
        if not ws: break
        for yname in xdata.keys():
            if not ws.var(wsxname[xname]):
                raise RuntimeError, "Didn't find %s in !" % wsxname[xname]
            if not ws.var(wsyname[yname]):
                raise RuntimeError, "Didn't find %s in !" % wsyname[yname]
            xdata[yname].append( xtransform[yname]( ws.var(wsxname[yname]).getVal() ) )
            ydata[yname].append( ytransform[yname]( ws.var(wsyname[yname]).getVal() ) )
            exdata[yname].append( xtransform[yname]( ws.var(wsxname[yname]).getError() ) )
            eydata[yname].append( ytransform[yname]( ws.var(wsyname[yname]).getError() ) )

gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()


c1 = TCanvas("c1", "c1", 300,900)
c1.Divide(1,4)

gr = {}
canvas = {}
#ytrue = {
    #"resolution": 1.,
    #"scale":      0.,
    #"cut":        1.,
    #"power":      1.5,
    #}

for yname in "scale resolution cut power".split():
    yunit = paramInfo[yname][2]
    x = array.array("d", xdata[xname])
    y = array.array("d", ydata[yname])
    y0 = array.array("d", xdata[yname])
    ex = array.array("d", exdata[yname])
    ey = array.array("d", eydata[yname])
    for i in range(len(y)):
        y[i] = y[i] - y0[i]
        #if yname == xname:
            #y[i] = y[i]-x[i]
        #else:
            #y[i] = y[i] - ytrue[yname]
    gr[yname] = TGraphErrors(len(xdata[yname]), x, y, ex, ey)
    gr[yname].GetYaxis().SetTitle(" ".join(["measured - true", yname, yunit]))
    gr[yname].GetXaxis().SetTitle(" ".join(["true", xname, xunit]))
    gr[yname].GetYaxis().SetTitleOffset(1.4)
    gr[yname].Fit("pol1", "", "", *fitrange)
#     canvas[yname] = TCanvas()
    canvas[yname] = c1.cd(len(canvas.values()) + 1)
    canvas[yname].SetLeftMargin(0.2)
    gr[yname].Draw("ap")

# for yname, c in canvas.items():
#     c.Print(yname + "BiasVs" + xname.title() + ".eps")

c1.Print(xname + "Scan.eps")