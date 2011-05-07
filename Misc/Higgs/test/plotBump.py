from ROOT import *

tags = "zg zjets wg wjets".split()
#tags = "zg".split()

file, tree = {}, {}
for tag in tags:
    file[tag] = TFile("bumpTree_%s.root" % tag)
    tree[tag] = file[tag].Get("tree/tree") 

weight100ipb = {
    "wg"    : 0.03901,
    "wjets" : 0.30664,
    "zjets" : 0.11729,
    "zg"    : 0.01308,
}

def selection(minPt, tag):
    return "( min(eg.ele.pt,eg.pho.pt) > %s &  " % minPt + \
           "  max(eg.ele.pt,eg.pho.pt) > 40 &  " + \
           "  !eg.pho.hasPixelSeed ) * %f" % weight100ipb[tag]

canvas = {}
hist = {}
for tag in tags:
    canvas[tag] = TCanvas()
    tree[tag].Draw( "eg.mass>>h40_%s(25,0,250)" % tag, selection(40, tag) )
    hist[tag] = gDirectory.Get("h40_" + tag)
    canvas[tag].Print( tag + ".png" )

