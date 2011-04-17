import sys
from ROOT import *

filename = "tree_numEvent55.root"
if len(sys.argv) >= 2:
  filename = sys.argv[1]

print "Comparing trees from " + filename + "."

file1 = TFile(filename)

file
tree = file1.Get("tree/tree")
testTree = file1.Get("testTree/testTree")

tree.AddFriend(testTree, "ref")
canvases = []

print "== var   entries mean rms =="
for var in "id.run id.luminosityBlock ncands id.event candPt candEta candPhi".split():
  canvases.append(TCanvas(var, var))
  tree.Draw("%s-ref.%s>>h%s" % (var,var,var))
  hist = gDirectory.Get("h" + var)
  print "%20s: %5d  %.2g  %.2g" % \
      ( var, int(hist.GetEntries()), hist.GetMean(), hist.GetRMS() )

for c in canvases:
  i = canvases.index(c)
  c.SetWindowPosition(20*i, 20*i)
  #c.Print(c.GetName() + ".png")

if __name__ == "__main__": import user
