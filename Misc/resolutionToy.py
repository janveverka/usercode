import ROOT

tree = ROOT.TTree("toy", "6 independent standard normal variables")

ROOT.gROOT.ProcessLine("struct UVWXYZ {Double_t u,v,w,x,y,z;};")
uvwxyz = ROOT.UVWXYZ()
varlist = "u v w x y z".split()

for x in varlist:
  tree.Branch(x, ROOT.AddressOf(uvwxyz, x), x + "/D")

for i in range(10000):
  for x in varlist:
    setattr(uvwxyz, x, ROOT.gRandom.Gaus(0, 1))
  dummy = tree.Fill()

c1 = ROOT.TCanvas("c1", "c1", 900, 900)
c1.Divide(2, 3)

c1.cd(1); tree.Draw("x>>hx(100,-5,5)")
c1.cd(3); tree.Draw("y>>hy(100,-5,5)")
c1.cd(5); tree.Draw("sqrt(x*y)>>hxy(100,-5,5)")

c1.cd(2); tree.Draw("1+x/10>>hfx(1000,-5,5)")
c1.cd(4); tree.Draw("1+y/10>>hfy(1000,-5,5)")
c1.cd(6); tree.Draw("sqrt((1+x/10)*(1+y/10))>>hfxy(1000,-5,5)")
