import sys
import ROOT

ws = ROOT.RooWorkspace("ws")

cb1 = ws.factory("""CBShape::cb1(
  m[-50,0,50],
  cbBias1[0,-10,10],
  cbSigma1[1.5,0.001,5],
  cbCut1[1.5,0,10],
  cbPower1[1.5,0.1,20]
  """)

cb2 = ws.factory("""CBShape::cb2(
  m[-50,0,50],
  cbBias2[0,-10,10],
  cbSigma2[1.5,0.001,5],
  cbCut2[1.5,0,10],
  cbPower2[1.5,0.1,20]")
  """)

cb3 = ws.factory("""CBShape::cb3(
  m[-50,0,50],
  cbBias3[0,-10,10],
  cbSigma3[2.1,0.001,5],
  cbCut3[1.5,0,10],
  cbPower2[1.5,0.1,20]")
  """)

CB1xCB2 = ws.factory("FFTConvPdf::CB1xCB2(m,cb1,cb2)")

data = CB1xCB2.generateBinned(ROOT.RooArgSet(ws.var("m")), 10000)