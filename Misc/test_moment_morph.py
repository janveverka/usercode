"""
Test the RooMomentMorph class of roofit.
Morph between 3 Gaussians.
"""

import ROOT
import JPsi.MuMu.common.roofit as roofit
import JPsi.MuMu.common.canvases as canvases

w = ROOT.RooWorkspace('w', 'w')

f1 = w.factory('CBShape::f1(x[-10,8],mean1[-5],sigma1[1],alpha1[1],n1[2])')
f2 = w.factory('Gaussian::f2(x,mean2[-1],sigma2[2])')
f3 = w.factory('BreitWigner::f3(x,mean3[4],sigma3[0.5])')
fm = w.factory('MomentMorph::fm(m[0, -10,100], {x}, {f1, f2, f3}, {m1[5], m2[9], m3[14]})')
x = w.var('x')
canvases.next()
xframe = x.frame()
f1.plotOn(xframe, roofit.LineColor(ROOT.kRed))
f2.plotOn(xframe, roofit.LineColor(ROOT.kRed))
f3.plotOn(xframe, roofit.LineColor(ROOT.kRed))
for mval in range(5,15):
  w.var('m').setVal(mval)
  fm.plotOn(xframe, roofit.LineStyle(ROOT.kDashed))
xframe.Draw()
canvases.update()

if __name__ == '__main__':
    import user

