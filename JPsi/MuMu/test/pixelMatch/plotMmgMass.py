import os
from ROOT import *
from array import array

path = "/home/veverka/Work/data/pmv"

fileName = {
    "data": "pmvTree_Mu_Run2010AB-Dec22ReReco_v1_json_V3.root",
    #"z"   : "pmvTree_DYToMuMu_M-20-powheg-pythia_Winter10-v1_V3.root",
    "z"  : "pmvTree_DYToMuMu_M-20-powheg-pythia_Winter10-v2_V3.root",
    "tt"  : "pmvTree_TTJets_TuneZ2-madgraph-Winter10_V3.root",
    "w"   : "pmvTree_WJetsToLNu_TuneZ2_7TeV-madgraph_Winter10_V3.root",
    "qcd" : "pmvTree_QCD_Pt-20_MuEnrichedPt-15_Winter10_V3.root",
}

weight = {
    "data": 1.,
    "z"  : 0.030541912803076,
    "qcd": 0.10306919044126,
    "w"  : 0.074139194512438,
    "tt" : 0.005083191122289,
}

canvases = []
graphs = []

## Set TDR style
macroPath = "tdrstyle.C"
if os.path.exists(macroPath):
    gROOT.LoadMacro(macroPath)
    ROOT.setTDRStyle()
    gROOT.ForceStyle()

gStyle.SetPadRightMargin(0.05)
gStyle.SetPadTopMargin(0.05)
wWidth = 600
wHeight = 600
canvasDX = 20
canvasDY = 20

latexLabel = TLatex()
latexLabel.SetNDC()

## open files
file = {}
for tag, name in fileName.items():
    file[tag] = TFile(os.path.join(path, name))

## get trees
tree = {}
for tag, f in file.items():
    tree[tag] = f.Get("pmvTree/pmv")

## make histos of pmv vs mmgMass

ebSelection = "phoIsEB & abs(mmgMass-90)<15 & (minDEta > 0.04 | minDPhi > 0.3)"
eeSelection = "!phoIsEB & abs(mmgMass-90)<15 & (minDEta > 0.08 | minDPhi > 0.3)"

###############################################################################
# Plot mmgMass in data for EB
c1 = TCanvas()
canvases.append(c1)

#h_mmgMass = {}
#h_mmgMass["data"] = TH1F("h_mmgMass_data_eb", "min #Delta #eta (#mu, #gamma)", 60, 60, 120)
h_mmgMass = TH1F("h_mmgMass_data_eb", "min #Delta #eta (#mu, #gamma)", 60, 60, 120)

tree["data"].Draw("mmgMass>>h_mmgMass_data_eb", ebSelection)
htot = h_mmgMass.Clone(h_mmgMass.GetName() + "_tot")

tree["data"].Draw("mmgMass>>" + h_mmgMass.GetName(), ebSelection + "& !phoHasPixelMatch")
hpass = h_mmgMass.Clone(h_mmgMass.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("p_{T}^{#gamma}")
geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency")
geff.SetTitle("Dec22ReReco, L = 35.9 pb^{-1}")
geff.Draw("ap")
graphs.append(geff)

latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
latexLabel.DrawLatex(0.7, 0.2, "Barrel")
c1.Update()


###############################################################################
# Plot PMV eff. vs mmgMass in MC for EB
c1 = TCanvas()
canvases.append(c1)

xbins = [float(i) for i in range(41)] + [40., 45., 50., 60., 75., 100.]

h_mmgMass = TH1F("h_mmgMass_mc_eb", "min #Delta #eta (#mu, #gamma)", len(xbins)-1, array("d", xbins))

tree["z"].Draw("mmgMass>>" + h_mmgMass.GetName(), ebSelection)
htot = h_mmgMass.Clone(h_mmgMass.GetName() + "_tot")

tree["z"].Draw("mmgMass>>" + h_mmgMass.GetName(), ebSelection + "& !phoHasPixelMatch")
hpass = h_mmgMass.Clone(h_mmgMass.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("p_{T}^{#gamma}");
geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency");
geff.Draw("ap");
graphs.append(geff)

latexLabel.DrawLatex(0.15, 0.96, "Powheg/Pythia Z#rightarrow#mu#mu+X")
latexLabel.DrawLatex(0.75, 0.96, "Winter10")
latexLabel.DrawLatex(0.7, 0.2, "Barrel")
c1.Update()


###############################################################################
# Plot PMV eff. vs mmgMass in data for EE
c1 = TCanvas()
canvases.append(c1)

xbins = [0., 5., 15., 50., 100.]

h_mmgMass = TH1F("h_mmgMass_data_ee", "min #Delta #eta (#mu, #gamma)", len(xbins)-1, array("d", xbins))

tree["data"].Draw("mmgMass>>" + h_mmgMass.GetName(), eeSelection)
htot = h_mmgMass.Clone(h_mmgMass.GetName() + "_tot")

tree["data"].Draw("mmgMass>>" + h_mmgMass.GetName(), eeSelection + "& !phoHasPixelMatch")
hpass = h_mmgMass.Clone(h_mmgMass.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("p_{T}^{#gamma}")
geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency")
geff.SetTitle("Dec22ReReco, L = 35.9 pb^{-1}")
geff.Draw("ap")
graphs.append(geff)

latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2010")
latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
latexLabel.DrawLatex(0.7, 0.2, "Endcaps")
c1.Update()


###############################################################################
# Plot PMV eff. vs mmgMass in MC for EE
c1 = TCanvas()
canvases.append(c1)

xbins = [float(i) for i in range(41)] + [40., 45., 50., 60., 75., 100.]

h_mmgMass = TH1F("h_mmgMass_mc_ee", "min #Delta #eta (#mu, #gamma)", len(xbins)-1, array("d", xbins))

tree["z"].Draw("mmgMass>>" + h_mmgMass.GetName(), eeSelection)
htot = h_mmgMass.Clone(h_mmgMass.GetName() + "_tot")

tree["z"].Draw("mmgMass>>" + h_mmgMass.GetName(), eeSelection + " & !phoHasPixelMatch")
hpass = h_mmgMass.Clone(h_mmgMass.GetName() + "_pass")

geff = TGraphAsymmErrors()
geff.BayesDivide(hpass,htot)
geff.GetXaxis().SetTitle("p_{T}^{#gamma}");
geff.GetYaxis().SetTitle("Pixel Match Veto Efficiency");
geff.Draw("ap");
graphs.append(geff)

latexLabel.DrawLatex(0.15, 0.96, "Powheg/Pythia Z#rightarrow#mu#mu+X")
latexLabel.DrawLatex(0.75, 0.96, "Winter10")
latexLabel.DrawLatex(0.7, 0.2, "Endcaps")
c1.Update()


#geff_mmgMass_mc.BayesDivide(h_mmgMass_mc_pass, h_mmgMass_mc_tot)

#tree["z"].Draw("mmgMass>>h_mmgMass", "isEB & abs(mmgMass-90)<15")
#h_mmgMass_z_tot = h_mmgMass.Clone("h_mmgMass_z_tot")

#tree["z"].Draw("mmgMass>>h_mmgMass", "isEB & abs(mmgMass-90)<15 & !phoHasPixelMatch")
#h_mmgMass_z_pass = h_mmgMass.Clone("h_mmgMass_z_pass")

#geff.SetTitle("POWHEG+Pythia Z#rightarrow#mu#mu Fall10 MC, FSR events");
