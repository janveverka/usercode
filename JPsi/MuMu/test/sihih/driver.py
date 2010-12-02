import sys
import histos
import cuts
from ROOT import *
from common import *


filename = "kHistos.root"
# histosToMake = "mass mmgMass".split()
# histosToMake = "mmgMassEB mmgMassEE phoPt phoPtEB phoPtEE phoE phoEEB phoEEE".split()
histosToMake = "kRatio inverseK minusLogK kRatio2 inverseK2 minusLogK2".split()
# profilesToMake = ["eeSihihVsDR"]
profilesToMake = []

## Preselection
#print "Applying preselection ...\n  ",
#for name, ch in chains.items():
    #print name,; flush()
    #lname = "eventList_%s" % name
    ##ch.Draw(">>%s" % lname, "isBaselineCand")
    #ch.Draw(">>%s" % lname, makeSelection(cuts.lyonCuts))
    #ch.SetEventList(gDirectory.Get(lname))

file = TFile(filename, "recreate")

###############################################################################
## Make histos

print "Starting loop over histos ..."
for x in histosToMake:
    makeHistos(chains, histos.histos[x], cuts.cuts[x], ["zmg"])

print "Starting loop over profiles ... "
for x in profilesToMake:
    makeHistos(chains, histos.histos[x], cuts.cuts[x], ["zmg"], "profile")

print "Saving output to %s ... " % file.GetName()
file.Write()

print "Exitting with great success!"
