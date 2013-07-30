'''
Demonstrate transform to a uniform variable
Jan Vevera, MIT, 23 July 2013
'''
import math
import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.canvases as canvases
import FWLite.Tools.tools as tools

from qqcorrector import QQCorrector

class Uniformizer:
    '''
    Given a PDF, it generates toy data and
    transforms it to the standard uniform density 
    '''
    #___________________________________________________________________________
    def __init__(self, xvar, xpdf, size=10000, color=ROOT.kBlue):
        self.xvar = xvar
        self.xpdf = xpdf
        self.size = size
        self.color = color
        self.init()

    #___________________________________________________________________________
    def init(self):
        '''
        Initialize variables, PDFs, Functions and data.
        '''
        self.uniform_var = ROOT.RooRealVar('u',
                                           'u(' + self.xvar.GetTitle() + ')',
                                           -0.5, 1.5)
        self.uniform_pdf = ROOT.RooUniform('fU', 'fU',
                                           ROOT.RooArgSet(self.uniform_var))
        self.xcdf = self.xpdf.createCdf(ROOT.RooArgSet(self.xvar))
        self.xcdf.SetNameTitle(self.uniform_var.GetName(),
                               self.uniform_var.GetTitle())
        self.data = self.xpdf.generate(ROOT.RooArgSet(self.xvar), self.size)
        self.data.addColumn(self.xcdf)
        self.data.Print('v')

    #___________________________________________________________________________
    def make_plots(self):
        '''
        Create canvases with plots demonstrating the transform and the
        original and transformed distributions.
        '''
        self.plot_x()
        self.plot_transform()
        self.plot_inverse_transform()
        self.plot_uniform()
        canvases.update()

    #___________________________________________________________________________
    def plot_x(self):
        '''
        Create a canvas with x data overlayed with its PDF.
        '''
        self.xplot = self.xvar.frame()
        self.data.plotOn(self.xplot, roo.LineColor(self.color),
                         roo.MarkerColor(self.color))
        self.xpdf.plotOn(self.xplot, roo.LineColor(self.color))
        canvases.next(self.xvar.GetTitle()).SetGrid()
        self.xplot.SetTitle('')
        self.xplot.Draw()

    #___________________________________________________________________________
    def plot_transform(self):
        '''
        Create a canvas showing the transform.
        '''
        self.make_tplot()
        canvases.next(self.xvar.GetTitle() + '_transform').SetGrid()
        self.tplot.SetTitle('')
        self.tplot.GetYaxis().SetTitle(self.uniform_var.GetTitle())
        self.tplot.Draw()

    #___________________________________________________________________________
    def make_tplot(self):
        '''
        Create the plot of the transform
        '''
        self.tplot = self.xvar.frame()
        self.xcdf.plotOn(self.tplot, roo.LineColor(self.color))
        
    #___________________________________________________________________________
    def plot_inverse_transform(self):
        '''
        Create a canvas showing the inverse of the transform.
        '''
        if not self.tplot:
            self.make_tplot()
        tcurve = self.tplot.getCurve()
        self.itgraph = ROOT.TGraph(tcurve.GetN(), tcurve.GetY(), tcurve.GetX())
        self.itgraph.Sort()
        cname = '_'.join([self.uniform_var.GetName(), 'to',
                         self.xvar.GetName(), 'transform'])
        indexes = range(1, self.itgraph.GetN())
        indexes.reverse()
        for i in indexes:
            #print "i=", i, "x=", self.itgraph.GetX()[i],
            #print  "y=", self.itgraph.GetY()[i]
            if self.itgraph.GetX()[i] <= self.itgraph.GetX()[i-1]:
                print 'Removing point', i, 'of', cname
                self.itgraph.RemovePoint(i)
        canvases.next(cname).SetGrid()
        self.itgraph.SetLineWidth(3)
        self.itgraph.SetLineColor(self.color)
        self.itgraph.SetTitle('')
        self.itgraph.Draw("ac")
        xtitle = self.uniform_var.GetTitle().replace("(" + self.xvar.GetTitle()
                                                     + ")", "")
        ytitle = self.xvar.GetTitle() + "(" + xtitle + ")"
        self.itgraph.GetXaxis().SetTitle(xtitle)
        self.itgraph.GetYaxis().SetTitle(ytitle)

    #___________________________________________________________________________
    def plot_uniform(self):
        '''
        Create a canvas with transformed x data overlayed with a uniform pdf.
        '''
        self.uplot = self.uniform_var.frame()
        self.data.plotOn(self.uplot, roo.LineColor(self.color),
                         roo.MarkerColor(self.color))
        self.uniform_pdf.plotOn(self.uplot, roo.Range(0, 1),
                                roo.LineColor(self.color))
        cname = '_'.join([self.uniform_var.GetName(), 'of', self.xvar.GetName()])
        canvases.next(cname).SetGrid()
        self.uplot.SetTitle('')
        self.uplot.Draw()
## End of class Uniformizer


#_______________________________________________________________________________
def test():
    global w, ux, uy, uuplots, xyplot, yxplot
    w = ROOT.RooWorkspace("test", "test")
    fX = w.factory("Gaussian::fX(x[-3,3], m[0], s[1])")
    fY = w.factory("Gamma::fY(y[0,20], beta[2], gamma[2], mu[0])")
    ux = Uniformizer(w.var('x'), fX)
    uy = Uniformizer(w.var('y'), fY, color=ROOT.kRed)
    ux.make_plots()
    uy.make_plots()
    uuplot = make_uuplot(ux, uy)
    xyplot, yxplot = make_qqplots(ux, uy)
    canvases.update()

#_______________________________________________________________________________
def make_uuplot(ux, uy):
    plot = ux.uniform_var.frame()
    ux.data.plotOn(plot, roo.LineColor(ux.color), roo.MarkerColor(ux.color))
    ux.uniform_pdf.plotOn(plot, roo.LineColor(ux.color), roo.Range(0,1))
    uy.uniform_pdf.plotOn(plot, roo.LineColor(uy.color), roo.Range(0,1),
                          roo.LineStyle(ROOT.kDashed))
    uy.data.plotOn(plot, roo.LineColor(uy.color), roo.MarkerColor(uy.color),
                   roo.MarkerStyle(4))
    canvases.next('uu')
    plot.Draw()
    return plot

#_______________________________________________________________________________
def make_qqplots(ux, uy):
    xyplot = uy.xvar.frame()
    xyplot.SetTitle('')
    xycorr = QQCorrector(ux.xvar, ux.xpdf, uy.xvar, uy.xpdf)
    xycorr.SetName('y')
    ux.data.addColumn(xycorr)
    uy.data.plotOn(xyplot, roo.LineColor(uy.color),
                   roo.MarkerColor(uy.color))
    uy.xpdf.plotOn(xyplot, roo.LineColor(uy.color))
    ux.data.plotOn(xyplot, roo.LineColor(ux.color),
                   roo.MarkerColor(ux.color))

    yxplot = ux.xvar.frame()
    yxplot.SetTitle('')
    yxcorr = QQCorrector(uy.xvar, uy.xpdf, ux.xvar, ux.xpdf)
    yxcorr.SetName('x')
    uy.data.addColumn(yxcorr)
    ux.data.plotOn(yxplot, roo.LineColor(ux.color),
                   roo.MarkerColor(ux.color))
    ux.xpdf.plotOn(yxplot, roo.LineColor(ux.color))
    uy.data.plotOn(yxplot, roo.LineColor(uy.color),
                   roo.MarkerColor(uy.color))

    canvases.next('qqxy')
    xyplot.Draw()

    canvases.next('qqyx')
    yxplot.Draw()
    
    return xyplot, yxplot

#_______________________________________________________________________________
if __name__ == '__main__':
    test()
    import user
    
