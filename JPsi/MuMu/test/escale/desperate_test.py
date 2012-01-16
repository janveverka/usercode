'''
Test if it is possible to build a 2D model with correlation using composition
of a model of 2 independent variables and then substitutin for one of them
an expression depending on the other.

f(x,y,mx,sx,my,sy) = Gauss(x,mx,sx)*Gauss(y,my,sy)
mx -> mxf = a + b*y
f -> fc
fc(x,y|a,b,sx,my,sy) = Gauss(x,mx,sx|y)*Gauss(y,my,sy)

The composition + susbstitution seems to produce the same result as the
traditional conditional product described in the RooFit manual.

A culprit: Both the substituted variable and the function substituting
have to have the same name, "mx" here.  This brings difficulties persisting
them both simultaneously in a workspace.
'''

import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.cmsstyle import cmsstyle

w = ROOT.RooWorkspace('w', 'w')

def plotxy(pdf, xyexpr = 'x:y'):
    h_pdf = pdf.createHistogram(xyexpr)
    h_pdf.SetLineColor(ROOT.kBlue)
    canvases.next(h_pdf.GetName())
    h_pdf.Draw('surf')

## The Classic way -------------------------------------------------------------
gx = w.factory('Gaussian::gx(x[-5,5],mx[0],sx[0.5])')
gy = w.factory('Gaussian::gy(y[-5,5],my[0],sy[3])')
fprod = w.factory('PROD::fprod(gx, gy)')
plotxy(fprod)

cust = ROOT.RooCustomizer(gx, 'shift')
mxf = w.factory('PolyVar::mxf(y, {0, -0.4})')
cust.replaceArg(w.var('mx'), mxf)
gx_shift = cust.build()
w.Import(gx_shift)
fcond = w.factory('PROD::fcond(gx_shift|y, gy)')
plotxy(fcond)

## The Test way ----------------------------------------------------------------
## Compose the independent 2D model
fxy = w.factory('''expr::fxy("sqrt((x-mx)^2/sx^2 + (y-my)^2/sy^2)",
                             {x, mx, sx, y, my, sy})''')
gxy = w.factory('Gaussian::gxy(fxy, 0, 1)')
plotxy(gxy)

## Introduce the correlation through substitution
mxf.SetName('mx')
gxy_cust = ROOT.RooCustomizer(gxy, 'cond')
## The formula would not compile if the the substitution had a different name.
gxy_cust.replaceArg(w.var('mx'), mxf)
gxy_cond = gxy_cust.build()
w.Import(gxy_cond, True)
plotxy(gxy_cond)

w.Print()
canvases.update()
print 'Exiting with success!'
