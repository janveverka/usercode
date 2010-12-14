import caltech
import lyon
import ROOT
from ROOT import *

tree = TTree("compare", "compare Lyon and Caltech events")
canvases = []
gROOT.LoadMacro("../tdrstyle.C")
ROOT.setTDRStyle()

## Process Lyon events
lines = file("dump_Selected.txt").readlines(30000)
eventList = [lyon.Event(line) for line in lines if line.strip()[0] != "#"]
lyonEvents = {}
for e in eventList:
    lyonEvents[e.eid] = e

gROOT.ProcessLine( e.cppStruct("LyonLeafs") )
from ROOT import LyonLeafs
lleafs = LyonLeafs()
e.makeBranches(tree, lleafs, "lyon_")

## Process Caltech events
lines = file("mmgEvents_LyonSelection_34ipb.dat").readlines(30000)
eventList = [caltech.Event(line) for line in lines if line.strip()[0] != "#"]
caltechEvents = {}
for e in eventList:
    caltechEvents[e.eid] = e

gROOT.ProcessLine( e.cppStruct("CaltechLeafs") )
from ROOT import CaltechLeafs
cleafs = CaltechLeafs()
e.makeBranches(tree, cleafs, "caltech_")

for eid in caltechEvents.keys():
    if eid in lyonEvents.keys():
        caltechEvents[eid].setLeafs(cleafs)
        lyonEvents[eid].setLeafs(lleafs)
        tree.Fill()
    #e.setLeafs(lleafs)
    #tree.Fill()

for xname in caltech.Event.varNames:
    if not xname in lyon.Event.varNames: continue
    canvases.append(TCanvas(xname + "Ratio", xname + "Ratio"))
    tree.Draw("lyon_%s/caltech_%s" % (xname, xname))
    canvases.append(TCanvas(xname + "Difference", xname + "Difference"))
    tree.Draw("lyon_%s-caltech_%s" % (xname, xname))

for c in canvases:
    i = canvases.index(c)
    c.SetWindowPosition(10+20*i, 10+20*i)
    c.Print("plots/" + c.GetName() + ".png")


if __name__ == "__main__": import user
