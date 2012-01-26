"""
Test the RooMomentMorph class of roofit.
Morph between 2 Gaussians and 2 HistPdfs.
"""

import ROOT
import JPsi.MuMu.common.roofit as roofit
import JPsi.MuMu.common.canvases as canvases

w = ROOT.RooWorkspace('w', 'w')

g1 = w.factory('Gaussian::g1(x[-10,10],0,1)')
g2 = w.factory('Gaussian::g2(x,0,2)')
g3 = w.factory('Gaussian::g3(x,0,3)')
gm = w.factory('MomentMorph::gm(m[1, 0.1, 10], {x}, {g1, g3}, {1,3})')
x = w.var('x')
g2Data = g2.generate(ROOT.RooArgSet(x), 1000)
gm.fitTo(g2Data)

canvases.next().SetLogy()
xframe = x.frame()
g2Data.plotOn(xframe)
gm.plotOn(xframe)
gm.paramOn(xframe)
xframe.Draw()
canvases.update()

xs =  ROOT.RooArgSet(x)
xl =  ROOT.RooArgList(x)

h1 = g1.createHistogram('h1', x)
h3 = g3.createHistogram('h3', x)

d1 = ROOT.RooDataHist('h1', 'h1', xl, h1)
d3 = ROOT.RooDataHist('h3', 'h3', xl, h3)

f1i0 = ROOT.RooHistPdf('f1i0', 'f1i0', xs, d1, 0)
f3i0 = ROOT.RooHistPdf('f3i0', 'f3i0', xs, d3, 0)

f1i1 = ROOT.RooHistPdf('f1i1', 'f1i1', xs, d1, 1)
f3i1 = ROOT.RooHistPdf('f3i1', 'f3i1', xs, d3, 1)

f1i2 = ROOT.RooHistPdf('f1i2', 'f1i2', xs, d1, 2)
f3i2 = ROOT.RooHistPdf('f3i2', 'f3i2', xs, d3, 2)

w.Import(f1i0)
w.Import(f3i0)

w.Import(f1i1)
w.Import(f3i1)

w.Import(f1i2)
w.Import(f3i2)

fmi0 = w.factory('MomentMorph::fmi0(m, {x}, {f1i0, f3i0}, {1,3})')
fmi1 = w.factory('MomentMorph::fmi1(m, {x}, {f1i1, f3i1}, {1,3})')
fmi2 = w.factory('MomentMorph::fmi2(m, {x}, {f1i2, f3i2}, {1,3})')

fmi0.fitTo(g2Data)

canvases.next().SetLogy()
xframe = x.frame()
g2Data.plotOn(xframe)
fmi0.plotOn(xframe)
fmi0.paramOn(xframe)
xframe.Draw()

fmi1.fitTo(g2Data)

canvases.next().SetLogy()
xframe = x.frame()
g2Data.plotOn(xframe)
fmi1.plotOn(xframe)
fmi1.paramOn(xframe)
xframe.Draw()

fmi2.fitTo(g2Data)

canvases.next().SetLogy()
xframe = x.frame()
g2Data.plotOn(xframe)
fmi2.plotOn(xframe)
fmi2.paramOn(xframe)
xframe.Draw()

canvases.update()

if __name__ == '__main__':
    import user

