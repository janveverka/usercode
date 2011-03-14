import sys
import ROOT

ws = ROOT.RooWorkspace("ws")

res = ws.factory("res[0.8,1.1]")
res.setBins(100)

cb1 = ws.factory("""CBShape::cb1(
  res,
  cbBias1[1],
  cbSigma1[0.01],
  cbCut1[1.5],
  cbPower1[1.5])""")

cb2 = ws.factory("""CBShape::cb2(
  res,
  cbBias2[0],
  cbSigma2[0.01],
  cbCut2[1.5],
  cbPower2[1.5,0.1,20])""")

cb3 = ws.factory("""CBShape::cb3(
  res,
  cbBias3[1,0.8,1.1],
  cbSigma3[0.014,0.0001,0.05],
  cbCut3[1.5,0,10],
  cbPower3[1.5,0.1,20])""")

res.setBins(100000, "fft")
CB1xCB2 = ws.factory("FFTConvPdf::CB1xCB2(res,cb1,cb2)")

# import all workspace variables
thisModule = sys.modules[__name__]
for varName in ws.allVars().contentsString().split(","):
    if hasattr(thisModule, varName):
        print varName, "already exists."
    else:
        print varName, "imported to", __name__
        setattr(thisModule, varName, ws.var(varName))


#data = CB1xCB2.generate(ROOT.RooArgSet(m), 10000)
data = CB1xCB2.generateBinned(ROOT.RooArgSet(res), 10000)

cb3.fitTo(data)

frame = res.frame()
ROOT.RooAbsData.plotOn(data, frame)
plotParams = ROOT.RooArgSet(cbBias3, cbSigma3, cbCut3, cbPower3)
cb3.paramOn(frame,
    ROOT.RooFit.Format("NEU", ROOT.RooFit.AutoPrecision(2) ),
    ROOT.RooFit.Parameters(plotParams),
    ROOT.RooFit.Layout(.67, 0.97, 0.97)
    )
cb3.plotOn(frame)

frame.Draw()
