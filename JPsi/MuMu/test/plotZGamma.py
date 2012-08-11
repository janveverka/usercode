from basicRoot import *
from MuMuGammaChain import chain as ch
from math import sqrt

# handy shortcut
ch.SetAlias("mm", "mmgDimuon")
ch.SetAlias("g", "mmgPhoton")
canvases = []
legends = []
plotNames = {}
gROOT.ProcessLine(".L tdrstyle.C")
gStyle.SetOptTitle(kFALSE)
gStyle.SetOptStat(kFALSE)
gStyle.SetTitleOffset(1.2, "Y")
gStyle.SetPadLeftMargin(.12)



def customizeTH2(h, xname, yname):
  h.SetMarkerStyle(20)
  h.GetXaxis().SetTitle(xname)
  h.GetYaxis().SetTitle(yname)

def makeTHStack(hlist):
  hs = THStack()
  for h in hlist:
    h.SetFillColor(h.GetLineColor())
    hs.Add(h)
  return hs

def drawTH1s(histos):
  ymax = 0.
  keys = ["r", "b", "s"]
  for k in keys:
    if histos[k].GetMaximum() > ymax:
      ymax = histos[k].GetBinContent(histos[k].GetMaximumBin())
  ymax = ymax + sqrt(ymax) + 1
  for k in keys:
    histos[k].SetMaximum(ymax)
  histos["r"].Draw()
  histos["b"].Draw("ex0 same")
  histos["s"].Draw("ex0 same")
  legend = TLegend(0.7,0.7,0.85,0.85)
  legend.AddEntry(histos["s"], "FSR", "p").SetTextColor(kRed)
  legend.AddEntry(histos["r"], "loose #gamma", "l")
#   legend.AddEntry(histos["b"], "fake #gamma", "p").SetTextColor(kBlue)
  legend.SetLineColor(kWhite)
  legend.SetFillColor(kWhite)
  legend.Draw()
  c = canvases[-1]
  c.RedrawAxis()
  plotNames[c] = histos["all"].GetName()
  legends.append(legend)

def drawTH2s(histos):
  histos["r"].Draw()
  histos["b"].Draw("same")
  histos["s"].Draw("same")
  legend = TLegend(0.7,0.7,0.85,0.85)
  legend.AddEntry(histos["s"], "FSR", "p").SetTextColor(kRed)
  legend.AddEntry(histos["r"], "loose #gamma", "p")
#   legend.AddEntry(histos["b"], "fake #gamma", "p").SetTextColor(kBlue)
  legend.SetLineColor(kWhite)
  legend.SetFillColor(kWhite)
  legend.Draw()
  c = canvases[-1]
  c.RedrawAxis()
  plotNames[c] = histos["all"].GetName()
  legends.append(legend)

def deleteExistingHisto(hname):
  if gDirectory.Get(hname):
    print "Replacing existing histogram", hname, "..."
    gDirectory.Get(hname).Delete()

# Preselection
ch.Draw(">>elist", "isZCand[mm] & charge[mm]==0 & nPhotons > 0 & backToBack < 0.95")
ch.SetEventList(gDirectory.Get("elist"))

sel = "isZCand[mm] & 45<mass[mm] & 45<mmgMass & mmgPhoton==0"
selMoreSignal = "mmgDeltaRNear < 1 & mass[mm] < 85"
# selMoreSignal = "mass[mm] < 85"
selMoreBkd = "mmgDeltaRNear > 1.5 & mass[mm] > 89 & mmgMass > 95 & 0"
selOthers = "!({s})&!({b})".format(s=selMoreSignal, b=selMoreBkd)

selBkd = sel + "& {s}".format(s=selMoreBkd)
selSig = sel+ "& {s}".format(s=selMoreSignal)
selRest = sel + "& {s}".format(s=selOthers)

def plotXY(xy = "mmgMass:mass[mm]",
           hname = "mass3vs2",
           xname = "m(#mu#mu) (GeV/c^{2})",
           yname = "m(#mu#mu#gamma) (GeV/c^{2})",
           binning = ""
           ):

  if len(binning) > 0 and binning[0] != "(":
    binning = "(" + binning + ")"

  # Plot Mass(mmg) vs Mass(mm) for background
  deleteExistingHisto(hname)
  ch.Draw(xy + ">>" + hname + binning, sel)
  h = gDirectory.Get(hname)
  customizeTH2(h, xname, yname)
  h.DrawCopy()

  deleteExistingHisto(hname+"B")
  ch.Draw(xy + ">>" + hname + "B" + binning, selBkd, "same")
  hb = gDirectory.Get(hname + "B")
  customizeTH2(hb, xname, yname)
  hb.SetMarkerColor(kBlue)
  hb.SetLineColor(kBlue)
  hb.DrawCopy("same")

  deleteExistingHisto(hname+"S")
  ch.Draw(xy + ">>" + hname + "S" + binning, selSig, "same")
  hs = gDirectory.Get(hname + "S")
  customizeTH2(hs, xname, yname)
  hs.SetMarkerColor(kRed)
  hs.SetLineColor(kRed)
  hs.DrawCopy("same")

  deleteExistingHisto(hname+"R")
  ch.Draw(xy + ">>" + hname + "R" + binning, selRest, "same")
  hr = gDirectory.Get(hname + "R")
  customizeTH2(hr, xname, yname)
  hs.DrawCopy("same")

  return {"all": h, "s": hs, "b": hb, "r": hr}


def savePlots(prefix = "hZGamma_", extension = "png"):
  for c in canvases:
    c.Print(prefix + plotNames[c] + "." + extension)

# # 1
# canvases.append(TCanvas())
# hMass3v2 = plotXY()
# drawTH2s(hMass3v2)
#
# # 2
# canvases.append(TCanvas())
# hDeltaR = plotXY("mmgDeltaRNear",
#   "deltaR",
#   "min #DeltaR(#mu^{#pm}#gamma)",
#   "Events / 0.2",
#   "20,0,4"
#   )
# drawTH1s(hDeltaR)
#
# # 3
# muFootprint = "({cut1} & {cut2})".format(
#   cut1 = "abs(phoTrackIso[g] - muPt[dau2[mm]]) < 1",
#   cut2 = "mmgDeltaRNear < 0.3"
# )
# trackIsoExpr = "phoTrackIso[g] - muPt[dau2[mm]] * " + muFootprint
# combinedIsoExpr = "phoEcalIso[g] + phoHcalIso[g] + " + trackIsoExpr
# canvases.append(TCanvas())
# hCombinedIso = plotXY(combinedIsoExpr,
#   "combinedIso",
#   "TRACK+ECAL+HCAL isolation (GeV)",
#   "Events / GeV",
#   "100,0,100"
#   )
# drawTH1s(hCombinedIso)
#
# # 4
# canvases.append(TCanvas())
# hCombinedIsoMod = plotXY("1./(1. + phoEcalIso[g]+phoHcalIso[g]+" + trackIsoExpr + ")",
#   "combinedIsoMod",
#   "1/(1 GeV + I), I = TRACK+ECAL+HCAL isolation (GeV)",
#   "Events / bin",
#   "100,0,1"
#   )
# drawTH1s(hCombinedIsoMod)
#
# # 5
# canvases.append(TCanvas())
# hTrackIso = plotXY(trackIsoExpr,
#   "trackIso",
#   "tracker isolation (GeV)",
#   "Events / 0.5 GeV",
#   "100,0,50"
#   )
# drawTH1s(hTrackIso)
#
# # 6
# canvases.append(TCanvas())
# hEcalIso = plotXY("phoEcalIso[g]",
#   "ecalIso",
#   "ECAL isolation (GeV)",
#   "Events / GeV",
#   "20,0,20"
#   )
# drawTH1s(hEcalIso)
#
# # 7
# canvases.append(TCanvas())
# hHcalIso = plotXY("phoHcalIso[g]",
#   "hcalIso",
#   "HCAL isolation (GeV)",
#   "Events / GeV",
#   "20,0,20"
#   )
# drawTH1s(hHcalIso)
#
# # 8
# canvases.append(TCanvas())
# hHadronicOverEm = plotXY("phoHadronicOverEm[g]",
#   "hadronicOverEm",
#   "H/E",
#   "Events / 0.05",
#   "20,0,1"
#   )
# drawTH1s(hHadronicOverEm)
#
# # 9
# canvases.append(TCanvas())
# hSigmaIetaIeta = plotXY("phoSigmaIetaIeta[g]",
#   "sigmaIetaIeta",
#   "#sigma_{i#etai#eta}",
#   "Events / 0.001",
#   "60,0,0.06"
#   )
# drawTH1s(hSigmaIetaIeta)
#
# # 10
# canvases.append(TCanvas())
# hSigmaIetaIetaVsCombinedIso = plotXY("phoSigmaIetaIeta[g]:" + combinedIsoExpr,
#   "sigmaIetaIetaVsCombinedIso",
#   "TRACK + ECAL + HCAL isolation (GeV)",
#   "#sigma_{i#etai#eta}",
#   )
# drawTH2s(hSigmaIetaIetaVsCombinedIso)
# canvases[-1].RedrawAxis()
#
# # 11
# canvases.append(TCanvas())
# hPt = plotXY("phoPt[g]",
#   "hPt",
#   "p_{#perp}^{#gamma} (GeV)",
#   "Events / 2 GeV",
#   "(25,0,50)"
#   )
# drawTH1s(hPt)
# canvases[-1].RedrawAxis()
#
# # 12
# canvases.append(TCanvas())
# hEta = plotXY("phoEta[g]",
#   "hEta",
#   "#eta",
#   "Events / 0.5",
#   "(12,-3,3)"
#   )
# drawTH1s(hEta)
# canvases[-1].RedrawAxis()
#
# # 13
# canvases.append(TCanvas())
# from math import pi as math_pi
# hPhi = plotXY("phoPhi[g]",
#   "hPhi",
#   "#phi",
#   "Events / 0.2 #pi",
#   "(10,-{pi},{pi})".format(pi=math_pi)
#   )
# drawTH1s(hPhi)
# canvases[-1].RedrawAxis()
#
# # 14
# canvases.append(TCanvas())
pdgMassZ = 91.1876
phoMuonE = "0.5*({Mz}*{Mz} - {Mmm}*{Mmm})/{Mmm}".format(Mz=pdgMassZ, Mmm="mass[mm]")
phoEcalE = "phoPt[g] / sin(2*atan(exp(-phoEta[g])))"
from propagateErrors import phoMuErr, phoEcalErr
phoEcalErr = "(" + phoEcalErr.format(e=phoEcalE) + ")"
nsel = ch.Draw(
  "{m}:{m}*{mErr}:{e}:{e}*{eErr}".format(
    e=phoEcalE, eErr=phoEcalErr, m=phoMuonE, mErr=phoMuErr
    ),
  selSig, "goff"
  )
xlist, exlist, ylist, eylist = [], [], [], []
print "E(muon) ( error ) E(ecal) (error)"
for i in range(nsel):
  xlist.append(ch.GetV1()[i])
  exlist.append(ch.GetV2()[i])
  ylist.append(ch.GetV3()[i])
  eylist.append(ch.GetV4()[i])
  print i, xlist[i], "(", exlist[i], ")", ylist[i], "(", eylist[i], ")"

gr = TGraphErrors(nsel, array("f", xlist), array("f", ylist), array("f", exlist), array("f", eylist))
canvases.append(TCanvas())
gr.SetMarkerStyle(20)
gStyle.SetOptFit(1)
fit2 = TF1("fit2", "pol1(0)", 0, 100)
fit2.FixParameter(0,0)
gr.Fit(fit2)
gr.GetXaxis().SetTitle("E(#gamma) from muons")
gr.GetYaxis().SetTitle("E(#gamma) from ECAL")
gr.Draw("azp")

print "E(gamma) ECAL/Muons, (err(mu)/mu \Oplus err(ECAL)/ECAL)^{-2}"
Oplus = lambda x, y: sqrt(x*x + y*y)
for i in range(len(xlist)):
  print ylist[i] / xlist[i], pow(Oplus(exlist[i]/xlist[i], eylist[i]/ylist[i]), -2)

# ch.GetV1()
# hPhoMeasVsExpectE = plotXY(phoMeasE + ":" + phoExpectE,
#   "phoMeasVsExpectE",
#   "E(#gamma) expected from muon kineamtics",
#   "measured E(#gamma)",
#   )
# fit = TF1("fit", "pol1(0)", 0, 100)
# fit.SetLineColor(kRed)
# fit.FixParameter(0,0)
# hPhoMeasVsExpectE["s"].SetStats()
# hPhoMeasVsExpectE["s"].Fit(fit)
# drawTH2s(hPhoMeasVsExpectE)
# canvases[-1].RedrawAxis()

# 15
# canvases.append(TCanvas())
# hMmgMass = plotXY("mmgMass",
#   "mmgMass",
#   "m(#mu#mu#gamma) (GeV/c^{2})",
#   "Events / 4 GeV",
#   "(10,80,120)"
#   )
# hs = hMmgMass["s"]
# hb = hMmgMass["b"]
# hr = hMmgMass["r"]
# hr.Add(hb)
# hr.SetFillStyle(0)
# hs.SetFillStyle(3002)
# hs.SetFillColor(kRed)
# hs.Draw("ex0 hist")
# hr.Draw("ex0 hist same")
# fit = TF1("fit2", "gaus(0)", 85, 95)
# fit.SetLineColor(kRed)
# fit.FixParameter(0,0)
# hs.SetStats()
# hs.Fit(fit)
# hs.Draw("ex0 same")

# canvases[-1].RedrawAxis()
# legend = TLegend(0.72,0.65,0.88,0.85)
# legend.AddEntry(hs, "FSR", "lpf").SetTextColor(kRed)
# legend.AddEntry(hr, "loose #gamma", "lp")
# legend.SetLineColor(kWhite)
# legend.SetFillColor(kWhite)
# legend.Draw()


# # 16
# canvases.append(TCanvas())
# hDimuonMass = plotXY("mass[mm]",
#   "hDimuonMass",
#   "m(#mu#mu) (GeV/c^{2})",
#   "Events / 4 GeV",
#   "(15,60,120)"
#   )
# drawTH1s(hDimuonMass)

# order canvases
for c in canvases:
  i = canvases.index(c)
  c.SetWindowPosition(10+20*i, 10+20*i)

if __name__ == "__main__": import user
