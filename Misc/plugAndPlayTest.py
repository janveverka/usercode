from ROOT import *

ws = RooWorkspace("ws")
sig_left = ws.factory("Gaussian::sig_left(x[-10,10], mean[0,-10,10], sigma[1,0,10])")
mean_shifted = ws.factory('FormulaVar::mean_shifted("mean+shift", {mean, shift[3]})')
sig_right = ws.factory("Gaussian::sig_right(x, mean_shifted, sigma)")
sig = ws.factory("AddPdf::sig(sig_left, sig_right, frac_left[0.7,0,1])")
plot = ws.var("x").frame()
ws.var("mean").setVal(-3)
sig.plotOn(plot)
ws.var("mean").setVal(3)
sig.plotOn(plot, RooFit.LineColor(kRed))
ws.var("shift").setVal(4)
sig.plotOn(plot, RooFit.LineColor(kBlack))
c1 = TCanvas()
plot.Draw()

xhalf = ws.factory('FormulaVar::xhalf("x/2.", {x})')
sig_half = ws.factory("Gaussian::sig_half(xhalf, mean, sigma)")
plot = ws.var("x").frame()
sig_left.plotOn(plot)
sig_half.plotOn(plot, RooFit.LineColor(kRed))
c2 = TCanvas()
plot.Draw()