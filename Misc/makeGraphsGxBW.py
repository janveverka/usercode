import array
import math
import ROOT
from ROOT import *
from parseCBxBWOutput import paramInfo

#gStyle.SetPadLeftMargin(0.2)
#gStyle.SetTitleYOffset(1.5)


## key=filename, value=(workspace name, list of cycles)
dataSource = {
    "GxBWResolutionScan_scale_0.99_10k.root": ("ws", range(1,20)),
    #"GxBWScaleScan_resolution_0.01_10k.root": ("ws", range(
}

xname = "resolution"
xunit = "(%)"
fitrange = (0, 10.5)

trueName = {
    "scale"     : "gMean_True",
    "resolution": "gSigma_True",
    }
    
measName = {
    "scale"     : "gMean",
    "resolution": "gSigma",
    }

trueTransform = {
    "scale": lambda x: 100. * (x - 1.),
    "resolution": lambda x: 100. * x,
    }
    
measTransform = {
    "scale": lambda x: x / 0.9119,
    "resolution": lambda x: x * math.sqrt(2.) / 0.9119,
    }

allData = (trueValue, measValue, trueError, measError) = ({}, {}, {}, {})
for name in trueName.keys():
    for data in allData:
        data[name] = []

for fileName, (workspaceName, cycles) in dataSource.items():
    file = TFile(fileName)

    for cycle in cycles:
        ws = file.Get("%s;%d" % (workspaceName, cycle) )
        if not ws:
            raise RuntimeError, "Didn't find %s;%d in %s" % (workspaceName, cycle, fileName)
        for name in trueName.keys():
            if not ws.var(trueName[name]):
                raise RuntimeError, "Didn't find %s in !" % trueName[name]
            if not ws.var(measName[name]):
                raise RuntimeError, "Didn't find %s in !" % measName[name]
            trueValue[name].append( trueTransform[name]( ws.var(trueName[name]).getVal() ) )
            measValue[name].append( measTransform[name]( ws.var(measName[name]).getVal() ) )
            trueError[name].append( trueTransform[name]( ws.var(trueName[name]).getError() ) )
            measError[name].append( measTransform[name]( ws.var(measName[name]).getError() ) )

gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()


gr = {}
canvas = {}
#ytrue = {
    #"resolution": 1.,
    #"scale":      0.,
    #"cut":        1.,
    #"power":      1.5,
    #}

for name in trueValue.keys():
    yunit = paramInfo[name][2]
    x = array.array("d", trueValue[xname])
    y = array.array("d", measValue[name])
    y0 = array.array("d", trueValue[name])
    ex = array.array("d", trueError[name])
    ey = array.array("d", measError[name])
    for i in range(len(y)):
        y[i] = y[i] - y0[i]
        #if name == name:
            #y[i] = y[i]-x[i]
        #else:
            #y[i] = y[i] - ytrue[name]
    gr[name] = TGraphErrors(len(trueValue[name]), x, y, ex, ey)
    gr[name].GetYaxis().SetTitle(" ".join(["measured - true", name, yunit]))
    gr[name].GetXaxis().SetTitle(" ".join(["true", xname, xunit]))
    gr[name].GetYaxis().SetTitleOffset(1.4)
    gr[name].Fit("pol1", "", "", *fitrange)
    canvas[name] = TCanvas()
    canvas[name].SetLeftMargin(0.2)
    gr[name].Draw("ap")

#for name, c in canvas.items():
    #c.Print(name + "BiasVs" + name.title() + ".eps")
