'''
Explore QQ Corrections
Jan Vevera, MIT, 23 July 2013
'''
import math
import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.canvases as canvases

w = ROOT.RooWorkspace("qq", "QQ Corrections")

fX = w.factory("Gaussian::fX(x[-3,3], m[0], s[1])")
fY = w.factory("Lognormal::fY(y[%f, %f], 1, %f)" % (math.exp(-3), math.exp(3), math.exp(1)))
fU = w.factory("Uniform::fU(u[-0.5,1.5])")
# fZ = w.factory("Gamma::fZ(z[0,20], beta[2], gamma[2], mu[2])")
# FZ = fZ.createCdf(ROOT.RooArgSet(w.var('z')))

yvar = w.factory('FormulaVar::yvar("exp(x)", {x})')
xvar = w.factory('FormulaVar::xvar("log(y)", {y})')
uvar = w.factory('FormulaVar::uvar("0.5*(1 + TMath::Erf(x/TMath::Sqrt(2)))", {x})')
yvar.SetNameTitle('y', 'y')
uvar.SetNameTitle('u', 'u')
# fZ.SetNameTitle('uz', 'u')

data = fX.generate(ROOT.RooArgSet(w.var('x')), 10000)
#data.merge(fZ.generate(ROOT.RooArgSet(w.var('z')), 10000))
data.addColumn(yvar)
data.addColumn(uvar)
#data.addColumn(FZ)

xplot = w.var('x').frame()
xplot.SetTitle('')
data.plotOn(xplot)
fX.plotOn(xplot)
canvases.next('fX').SetGrid()
xplot.Draw()

xyplot = w.var('x').frame()
xyplot.SetTitle('')
xyplot.GetYaxis().SetTitle('y')
yvar.plotOn(xyplot)
canvases.next('exp_of_x').SetGrid()
xyplot.Draw()

yxplot = w.var('y').frame()
yxplot.SetTitle('')
yxplot.GetYaxis().SetTitle('x')
xvar.plotOn(yxplot)
canvases.next('log_of_y').SetGrid()
yxplot.Draw()

yplot = w.var('y').frame(roo.Range(0, 5))
yplot.SetTitle('')
data.plotOn(yplot)
fY.plotOn(yplot)
canvases.next('fY').SetGrid()
yplot.Draw()

xuplot = w.var('x').frame()
xuplot.SetTitle('')
xuplot.GetYaxis().SetTitle('u')
uvar.plotOn(xuplot)
canvases.next('cdf_of_x').SetGrid()
xuplot.Draw()

uplot = w.var('u').frame()
yplot.SetTitle('')
data.plotOn(uplot)
fU.plotOn(uplot, roo.Range(0, 1))
canvases.next('fU').SetGrid()
uplot.Draw()

# zplot = w.var('z').frame()
# zplot.SetTitle('')
# data.plotOn(zplot)
# canvases.next('z').SetGrid()
# zplot.Draw()

canvases.update()

if __name__ == '__main__':
    import user
    
