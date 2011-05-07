from ROOT import *

file = TFile("bumpTree_wjets.root")
# file = TFile("bumpTree.root")
tree = file.Get("tree/tree")

def selection(minPt):
    return "min(eg.ele.pt,eg.pho.pt)>%s & max(eg.ele.pt,eg.pho.pt) > 40" % minPt

# tree.Draw("eg.mass>>h20(40,80,160)", selection(20))
# tree.Draw("eg.mass>>h30(40,80,160)", selection(30), "same")
c1 = TCanvas()
tree.Draw("eg.mass>>h40(40,80,160)", selection(40))
c2 = TCanvas()
tree.Draw("eg.mass>>h40(50,0,250)", selection(40))
# tree.Draw("eg.mass>>h50(40,80,160)", selection(50), "same")
