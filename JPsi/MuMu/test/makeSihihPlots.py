import sys
import ROOT

from ROOT import *
from MuMuGammaChain import *

##############################################################################
## Common stuff


file = TFile("sihihHistos.root")

gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()
gROOT.ForceStyle()
gStyle.SetPadRightMargin(0.05)
gStyle.SetPadTopMargin(0.05)

latexLabel = TLatex()
latexLabel.SetNDC()

canvases = {}
_module = sys.modules[__name__]

##############################################################################
## Make the dimuon mass plot on linear scale
lumi = 34. # pb^-1
realData = "data38x"
mcSamples = "z qcd w tt".split()
colors = {
    "z"  : kAzure - 9,
    "qcd": kSpring + 5,
    "tt" : kOrange - 2,
    "w"  : kRed + 1,
}

yrange = (0., 2000.)

legendTitles = {
    "z"   : "Z",
    "qcd" : "QCD",
    "tt"  : "t#bar{t}",
    "w"   : "W",
}

var = RooRealVar("mass", "m(#mu^{+}#mu^{-})", 60, 120, "GeV")

c1 = TCanvas(var.GetName(), var.GetName(), 20, 20, 400, 400)
canvases["mass"] = c1

hsname = "hs_%s" % var.GetName()
hs = THStack(hsname, "")
setattr(_module, hsname, hs)
histos = {}
mcIntegral = 0.
for dataset in mcSamples + [realData]:
    hname = "h_%s_%s" % (var.GetName(), dataset)
    setattr(_module, hname, file.Get(hname))
    h = getattr(_module, hname)
    if not h:
        raise RuntimeError, "Didn't find %s in %s!" % (hname, file.GetName())

    if dataset in mcSamples:
        ## Normalize to the expected lumi
        h.Scale(lumi * weight30[dataset] / 30.)

        ## Add to the total integral
        mcIntegral += h.Integral(1, var.getBins())

        ## Set Colors
        h.SetLineColor(colors[dataset])
        h.SetFillColor(colors[dataset])

        histos[dataset] = h

    else:
        hdata = h

    ## Set Titles
    xtitle = var.GetTitle()
    ytitle = "Events / %.2g pb^{-1} / %.2g" % (lumi, h.GetBinWidth(1))
    if var.getUnit():
        xtitle += " [%s]" % var.getUnit()
        ytitle += " %s" % var.getUnit()
    h.GetXaxis().SetTitle(xtitle)
    h.GetYaxis().SetTitle(ytitle)


## Normalize MC to data
kfactor = hdata.Integral(1, var.getBins()) / mcIntegral
for h in histos.values():
    h.Scale(kfactor)

## Sort histos
sortedHistos = histos.values()
sortedHistos.sort(key=lambda h: h.Integral())


## Make stacked histos (THStack can't redraw axis!? -> roottalk)
hstacks = []
for h in sortedHistos:
    hstemp = h.Clone(h.GetName().replace("h_", "hs_"))
    if hstacks:
        hstemp.Add(hstacks[-1])
    hstacks.append(hstemp)

## Draw
hstacks.reverse()
for h in hstacks:
    h.GetYaxis().SetRangeUser(*yrange)
    if hstacks.index(h) == 0: h.DrawCopy()
    else:                     h.DrawCopy("same")
hdata.DrawCopy("e0 same")
c1.RedrawAxis()


## Legend
ihistos = {}
for d, h in histos.items():
    ihistos[h] = d

legend = TLegend(0.75, 0.6, 0.9, 0.9)
legend.SetFillColor(0)
legend.SetShadowColor(0)
legend.SetBorderSize(0)

legend.AddEntry(hdata, "Data", "pl")

sortedHistos.reverse()
for h in sortedHistos:
    legend.AddEntry(h, legendTitles[ihistos[h]], "f")

legend.Draw()

## Final touch
latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")


##############################################################################
## Make the dimuon mass plot on linear scale

yrange = (1.e-2, 1.e5)
c1 = TCanvas(var.GetName() + "_logy", var.GetName() + "_logy", 40, 40, 400, 400)
canvases["mass_logy"] = c1
c1.SetLogy()
c1.cd()

## Draw with new y range
# ymin = 0.5 * min(weight30.values())
for h in hstacks:
    h.GetYaxis().SetRangeUser(*yrange)
    if hstacks.index(h) == 0: h.DrawCopy()
    else                    : h.DrawCopy("same")

hdata.DrawCopy("e0 same")
c1.RedrawAxis()

## Final touches
# legend.DrawClone()
latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
legend.Draw()


##############################################################################
## Make the dimuon mass Data / MC plot

yrange = (0., 2.)
cname = var.GetName() + "_DataOverMC"
c1 = TCanvas(cname, cname, 60, 60, 400, 400)
canvases["mass_ratio"] = c1
c1.SetGridy()
c1.cd()

## Create the ratio
hist = hdata.Clone("h_mass_data38xOverMC")
hist.Sumw2()
hist.Divide(hstacks[0])
hist.GetYaxis().SetRangeUser(*yrange)
hist.GetYaxis().SetTitle("Data / MC")
hist.Draw()

c1.RedrawAxis()

## Final touches
# legend.DrawClone()
latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")


##############################################################################
## Make the mmg mass plot



