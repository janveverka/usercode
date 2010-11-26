import MuMuGammaChain
from ROOT import *

chains = MuMuGammaChain.getChains(MuMuGammaChain.bfiles,
                                  MuMuGammaChain.bpath
                                  )

# handy shortcuts
for ch in chains.values():
    ch.SetAlias("mm", "mmgDimuon")
    ch.SetAlias("mu1", "dau1[mmgDimuon]")
    ch.SetAlias("mu2", "dau2[mmgDimuon]")
    ch.SetAlias("g", "mmgPhoton")

## Preselection
for name, ch in chains.items():
    lname = "eventList_%s" % name
    ch.Draw(">>%s" % lname, "isBaselineCand")
    ch.SetEventList(gDirectory.Get(lname))

file = TFile("sihihHistos.root", "recreate")

## Make Dimuon invariant mass histos
for dataset, ch in chains.items():
    ## variable title holds the expression for TTree::Draw
    var = RooRealVar("mass", "mass", 60, 120, "GeV")
    var.setBins(60)
    sel = "orderByVProb==0"
    hname = "h_%s_%s" % (var.GetName(), dataset)
    binning = "%d,%f,%f" % (var.getBins(), var.getMin(), var.getMax())
    expr = "%s>>%s(%s)" % (var.GetTitle(), hname, binning)
    ch.Draw(expr, sel, "goff")

file.Write()
# file.Close()

if __name__ == "__main__": import user
