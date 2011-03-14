import ROOT

file = ROOT.TFile("toy.root", "recreate")
tree = ROOT.TTree("toy", "various random variables")
nevents = 10000

ROOT.gROOT.ProcessLine("struct LeafVars {Double_t a,b,c,m,n,o,u,v,w,x,y,z;};")
leafVars = ROOT.LeafVars()

tree.Branch("aUniform", ROOT.AddressOf(leafVars, "a"), "a/D")
tree.Branch("bUniform", ROOT.AddressOf(leafVars, "b"), "b/D")
tree.Branch("cUniform", ROOT.AddressOf(leafVars, "c"), "c/D")

tree.Branch("mBreitWigner", ROOT.AddressOf(leafVars, "m"), "m/D")
tree.Branch("nBreitWigner", ROOT.AddressOf(leafVars, "n"), "n/D")
tree.Branch("oBreitWigner", ROOT.AddressOf(leafVars, "o"), "o/D")


tree.Branch("uCBShape", ROOT.AddressOf(leafVars, "u"), "u/D")
tree.Branch("vCBShape", ROOT.AddressOf(leafVars, "v"), "v/D")
tree.Branch("wCBShape", ROOT.AddressOf(leafVars, "w"), "w/D")

tree.Branch("xGaus", ROOT.AddressOf(leafVars, "x"), "x/D")
tree.Branch("yGaus", ROOT.AddressOf(leafVars, "y"), "y/D")
tree.Branch("zGaus", ROOT.AddressOf(leafVars, "z"), "z/D")

ws = ROOT.RooWorkspace("ws")
cb = ws.factory("""CBShape::cb(
  cbRes[-100,10],
  cbBias[0],
  cbSigma[1],
  cbCut[1.5],
  cbPower[1.5])""")
bw = ws.factory("""BreitWigner::bw(
    bwMass[0,2],
    bwMean[1],
    bwWidth[0.01]
    """)
cbData = cb.generate(ROOT.RooArgSet(ws.var("cbRes")), 3*nevents)
bwData = bw.generate(ROOT.RooArgSet(ws.var("bwMass")), 3*nevents)

for i in range(nevents):
  leafVars.a = ROOT.gRandom.Uniform()
  leafVars.b = ROOT.gRandom.Uniform()
  leafVars.c = ROOT.gRandom.Uniform()
  
  leafVars.m = bwData.get(3*i + 0).getRealValue("bwMass")
  leafVars.n = bwData.get(3*i + 0).getRealValue("bwMass")
  leafVars.o = bwData.get(3*i + 0).getRealValue("bwMass")
  
  leafVars.u = cbData.get(3*i + 0).getRealValue("cbRes")
  leafVars.v = cbData.get(3*i + 1).getRealValue("cbRes")
  leafVars.w = cbData.get(3*i + 2).getRealValue("cbRes")
  
  leafVars.x = ROOT.gRandom.Gaus(0, 1)
  leafVars.y = ROOT.gRandom.Gaus(0, 1)
  leafVars.z = ROOT.gRandom.Gaus(0, 1)
  #for x in varlist:
    #setattr(uvwxyz, x, ROOT.gRandom.Gaus(0, 1))
  dummy = tree.Fill()

tree.Write()

#>>> tree.Draw("(1+0.01*u)*(1+0.01*v):1+0.01*u+0.01*v", "", "goff")
#10000L
#>>> tree.GetV1()[0]
#1.0005898505647952
#>>> tree.GetV2()[0]
#1.0006138919305101
#>>> tree.GetV3()[0]
#Traceback (most recent call last):
  #File "<stdin>", line 1, in <module>
#IndexError: attempt to index a null-buffer
#>>> prod.setVa
#prod.setVal         prod.setValueDirty
#>>> prod.setVal(tree.GetV1()[0])
#>>> sum.setVal(tree.GetV1()[0])
#>>> data.add.__doc__
#'void RooDataSet::add(const RooArgSet& row, Double_t weight = 1.0, Double_t weightError = 0)\nvoid RooDataSet::add(const RooArgSet& row, Double_t weight, Double_t weightErrorLo, Double_t weightErrorHi)'
#>>> data.add(ROOT.RooArgSet(prod,sum))
#>>> for i in range(1,10000):
#...   prod.setVal(tree.GetV1()[i])
#...   sum.setVal(tree.GetV1()[i])
#...   data.add(ROOT.RooArgSet(prod,sum))

