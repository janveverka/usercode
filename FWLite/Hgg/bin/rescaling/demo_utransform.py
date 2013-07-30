'''
Demonstrate transform to a uniform variable
Jan Vevera, MIT, 23 July 2013
'''
import math
import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.canvases as canvases

w = ROOT.RooWorkspace("utransform", "utransform")

# Configure titles of x, fX, and u

fX = w.factory("Gaussian::fX(x[-3,3], m[0], s[1])")
fU = w.factory("Uniform::fU(u[-0.5,1.5])")
FX = fX.createCdf(ROOT.RooArgSet(w.var('x')))

FX.SetNameTitle('u', 'u')

data = fX.generate(ROOT.RooArgSet(w.var('x')), 10000)
data.addColumn(FX)

xplot = w.var('x').frame()
xplot.SetTitle('')
data.plotOn(xplot)
fX.plotOn(xplot)
canvases.next('fX').SetGrid()
xplot.Draw()

xuplot = w.var('x').frame()
xuplot.SetTitle('')
xuplot.GetYaxis().SetTitle('u')
FX.plotOn(xuplot)
canvases.next('FX').SetGrid()
xuplot.Draw()

uplot = w.var('u').frame()
uplot.SetTitle('')
data.plotOn(uplot)
fU.plotOn(uplot, roo.Range(0, 1))
canvases.next('fU').SetGrid()
uplot.Draw()

canvases.update()

if __name__ == '__main__':
    import user
    
