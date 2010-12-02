from ROOT import *

class Var(RooRealVar):
    """store histogram data related to a variable,
    title holds the selection."""
    def __init__(self, name, title, minValue, maxValue, unit, numBins=0):
        RooRealVar.__init__(self, name, title, minValue, maxValue, unit)
        if numBins > 0:
            self.setBins(numBins)

histos = {}
## Dictionary defining histograms in the format
## key = histogram id relating it to definition of cuts
## value.name = variable name used to build the histogram name
## value.title = TTree::Draw expression defining what is drawn
## value.{min,max}Value = x-axis range
## value.unit = variable unit used for axis titles
## value.numBins = number of histogram bins
histos["mass"] = Var("mass", "mass", 30, 130, "GeV", 100)
histos["mmgMass"  ] = Var("mmgMass"  , "mmgMass", 60, 120, "GeV", 60)
histos["mmgMassEB"] = Var("mmgMassEB", "mmgMass", 60, 120, "GeV", 60)
histos["mmgMassEE"] = Var("mmgMassEE", "mmgMass", 60, 120, "GeV", 60)
histos["ebSihih"] = Var("ebSihih", "phoSigmaIetaIeta[g]", 0., 0.03, "", 30)
histos["eeSihih"] = Var("eeSihih", "phoSigmaIetaIeta[g]", 0., 0.1, "", 20)
histos["ubebSihih"] = Var("ubebSihih", "phoSigmaIetaIeta[g]", 0., 0.03, "", 30)
histos["eeSihihVsDR"] = Var("eeSihihVsDR", "phoSigmaIetaIeta[g]:mmgDeltaRNear", 0., 3., "", 150)
histos["phoPt"  ] = Var("phoPt"  , "phoPt[g]", 0, 100, "GeV", 100)
histos["phoPtEB"] = Var("phoPtEB", "phoPt[g]", 0, 100, "GeV", 100)
histos["phoPtEE"] = Var("phoPtEE", "phoPt[g]", 0, 100, "GeV", 100)
histos["phoE"  ] = Var("phoE"  , "phoPt[g]*TMath::CosH(phoEta[g])", 0, 100, "GeV", 100)
histos["phoEEB"] = Var("phoEEB", "phoPt[g]*TMath::CosH(phoEta[g])", 0, 100, "GeV", 100)
histos["phoEEE"] = Var("phoEEE", "phoPt[g]*TMath::CosH(phoEta[g])", 0, 100, "GeV", 100)
histos["kRatio"] = Var("kRatio", "kRatio(mmgMass, mass[mm])", 0, 2, "", 40)
histos["kRatio2"] = Var("kRatio2", "kRatio(mmgMass, mass[mm])", 0, 2, "", 200)
histos["inverseK"] = Var("inverseK", "1./kRatio(mmgMass, mass[mm])", 0, 2, "", 40)
histos["inverseK2"] = Var("inverseK2", "1./kRatio(mmgMass, mass[mm])", 0, 2, "", 200)
histos["minusLogK"] = Var("minusLogK", "-log(kRatio(mmgMass, mass[mm]))", -1, 1, "", 40)
histos["minusLogK2"] = Var("minusLogK2", "-log(kRatio(mmgMass, mass[mm]))", -1, 1, "", 200)

