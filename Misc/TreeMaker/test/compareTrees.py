from ROOT import *
file1 = TFile("tree_numEvent5.root")
tree = file1.Get("tree/tree2")
testTree = file1.Get("testTree/testTree")
tree.AddFriend(testTree, "ref")
canvases = []
for var in "id.run id.luminosityBlock id.event candPt candEta candPhi".split():
  canvases.append(TCanvas(var, var))
  tree.Draw("%s-ref.%s" % (var,var))

for c in canvases:
  i = canvases.index(c)
  c.SetWindowPosition(20*i, 20*i)

if __name__ == "__main__": import user
