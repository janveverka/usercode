import sys
from ROOT import *

filename = "tree_numEvent100.root"
if len(sys.argv) == 2:
  filename = sys.argv[1]

file1 = TFile(filename)

file
tree = file1.Get("tree/tree")
testTree = file1.Get("testTree/testTree")

tree.AddFriend(testTree, "ref")
canvases = []

for var in "id.run id.luminosityBlock ncands id.event candPt candEta candPhi".split():
  canvases.append(TCanvas(var, var))
  tree.Draw("%s-ref.%s" % (var,var))

for c in canvases:
  i = canvases.index(c)
  c.SetWindowPosition(20*i, 20*i)

if __name__ == "__main__": import user
