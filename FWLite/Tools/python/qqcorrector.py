'''
Implementation of Q-Q Corrections.

Jan Veverka, MIT, 25 July 2013.
'''
import array
import ROOT
## Makes sure that RooFit classes are properly added to PyROOT
import FWLite.Tools.roofit as roo
## Provides RooNumInverse
import FWLite.Tools.tools as tools
import FWLite.Tools.canvases as canvases


def get_inverse(x, f):
    pass

#_______________________________________________________________________________
class QQCorrector(ROOT.RooNumInverse):
    '''
    Implements the QQ correction given the raw and target PDFs xpdf and ypdf.
    '''
    #___________________________________________________________________________
    def __init__(self, xvar, xpdf, yvar, ypdf, precision=1e-4, 
                 cdf_scan_bins=1000, cdf_scan_order=2):
        print 'DEBUG', self.__class__.__name__, '__init__' 
        self.xvar = xvar
        self.xpdf = xpdf
        self.yvar = yvar
        self.ypdf = ypdf
        self.precision = precision
        self.cdf_scan_bins = cdf_scan_bins
        self.cdf_scan_order = cdf_scan_order
        scan_cfg = roo.ScanParameters(cdf_scan_bins, cdf_scan_order)
        self.xcdf = self.xpdf.createCdf(ROOT.RooArgSet(self.xvar), scan_cfg)
        self.ycdf = self.ypdf.createCdf(ROOT.RooArgSet(self.yvar), scan_cfg)
        self.ycdf_inverse = ROOT.RooNumInverse(
            self.ycdf.GetName() + '_inverse',
            'Inverse of ' + self.ycdf.GetTitle(), self.yvar, self.ycdf,
            precision
            )
        self.customizer = ROOT.RooCustomizer(self.ycdf_inverse, 'QQC')
        self.customizer.replaceArg(self.yvar, self.xcdf)
        ROOT.RooNumInverse.__init__(self, self.customizer.build())
        name = '_'.join([self.xvar.GetName(), 'to', 
                         self.yvar.GetName(), 'qqcorrector'])
        title = ' '.join([self.xvar.GetTitle(), 'to', 
                          self.yvar.GetTitle(), 'Q-Q Corrector'])
        self.SetName(name)
        self.SetTitle(title)
        self.hists = []
            
    #___________________________________________________________________________
    def get_hist_func(self, granularity=1000, interpolation_order=2):
        '''
        Samples itself into a fine-binned histogram and returns
        a function based on the sampling.  This can be used for 
        persisting the correction in a file.
        '''
        name, title = self.GetName(), self.GetTitle()
        hist = self.create_sampling_scan_hist(granularity)
        self.data = ROOT.RooDataHist(name + '_data', title + ' Data',
                                     ROOT.RooArgList(self.xvar), hist)
        hist_func = ROOT.RooHistFunc(name, title, ROOT.RooArgSet(self.xvar),
                                     self.data, interpolation_order)
        return hist_func

    #___________________________________________________________________________
    def create_sampling_scan_hist(self, granularity=1000):
        nhist = len(self.hists)
        name = self.GetName()
        title = self.GetTitle()
        self.xvar.setBins(granularity, name + '_scan%d' % nhist)
        hist = self.createHistogram(self.GetName() + '_hist%d' % nhist,
                                    self.xvar, 
                                    roo.Binning(name + '_scan%d' % nhist),
                                    roo.Scaling(False))
        self.hists.append(hist)
        return hist

    #___________________________________________________________________________
    def get_interpolation_graph(self, granularity=1000):
        xvalues, yvalues = [], []
        ## Add a point at the lower boundary of x
        self.xvar.setVal(self.xvar.getMin())
        xvalues.append(self.xvar.getVal())
        yvalues.append(self.getVal())
        ## Fill in points at centers of equidistant bins of givin granularity
        hist = self.create_sampling_scan_hist(granularity)
        for ibin in range(1, hist.GetNbinsX() + 1):
            xvalues.append(hist.GetBinCenter(ibin))
            yvalues.append(hist.GetBinContent(ibin))
        ## Add a point at the upper boundary of x
        self.xvar.setVal(self.xvar.getMax())
        xvalues.append(self.xvar.getVal())
        yvalues.append(self.getVal())
        ## Construct the graph
        graph = ROOT.TGraph(len(xvalues), array.array('d', xvalues),
                            array.array('d', yvalues))
        graph.SetName(self.GetName() + '_%d' % len(self.hists))
        graph.SetTitle(self.GetTitle() + ' Interpolator %d' % len(self.hists))
        graph.SetMarkerStyle(20)
        return graph
        
    #___________________________________________________________________________
    def delete_data(self):
        '''
        Deletes the sampling scan histogram and DataHist objects.
        '''
        if hasattr(self, 'data'):
            self.data.Delete()
            del self.data
        if hasattr(self, 'hist'):
            self.hist.Delete()
            del self.hist        
        
    #___________________________________________________________________________
    def write_to_file(self, filename, recreate=True):
        w = ROOT.RooWorkspace(self.GetName(), self.GetTitle())
        self.import_into(w)
        w.writeToFile(filename, recreate)
    ## End of write_to_file(..)

    #___________________________________________________________________________
    def import_into(self, workspace):
        workspace.Import(self.get_hist_func())
        workspace.Import(self.data)
    ## End of importInto(..)
    
    #___________________________________________________________________________
    def get_correction_plot(self, *args):
        plot = self.xvar.frame()
        plot.SetTitle(self.GetTitle())
        plot.GetXaxis().SetTitle('Raw ' + self.xvar.GetTitle())
        plot.GetYaxis().SetTitle('Corrected ' + self.xvar.GetTitle())
        self.plotOn(plot, *args)
        return plot
    ## End of get_correction_plot(..)
    
    #___________________________________________________________________________
    def get_absolute_difference_plot(self, *args):
        plot = self.xvar.frame()
        plot.SetTitle(self.GetTitle())
        plot.GetXaxis().SetTitle('Raw ' + self.xvar.GetTitle())
        plot.GetYaxis().SetTitle('(Corrected - Raw) #times 100')
        adifference = ROOT.RooFormulaVar('adiff', '@0 - @1', 
                                         ROOT.RooArgList(self, self.xvar))
        adifference.plotOn(plot, *args)
        return plot
    ## End of get_absolute_difference_plot(..)
    
    #___________________________________________________________________________
    def get_relative_difference_plot(self, *args):
        plot = self.xvar.frame()
        plot.SetTitle(self.GetTitle())
        plot.GetXaxis().SetTitle('Raw ' + self.xvar.GetTitle())
        plot.GetYaxis().SetTitle('(Corrected / Raw - 1) #times 100')
        rdifference = ROOT.RooFormulaVar('adiff', '@0 / @1 - 1', 
                                         ROOT.RooArgList(self, self.xvar))
        rdifference.plotOn(plot, *args)
        return plot
    ## End of get_relative_difference_plot(..)
    
## End of class QQCorrector


#_______________________________________________________________________________
def test():
    global w, qq12, qq21, plot
    w = ROOT.RooWorkspace('w', 'Q-Q Corrections test')
    g1 = w.factory('Gaussian::g1(x[-5, 5], m1[0], s1[1])')
    g2 = w.factory('Gamma::g2(y[0,20], beta[2], gamma[2], mu[0])')
    
    qq12 = QQCorrector(w.var('x'), g1, w.var('y'), g2, 1e-3)
    plot12 = w.var('x').frame()
    plot12.SetTitle('')
    plot12.GetXaxis().SetTitle('Raw x')
    plot12.GetYaxis().SetTitle('Corrected x')
    qq12.plotOn(plot12)
    canvases.next('qq12').SetGrid()
    plot12.Draw()
    
    qq21 = QQCorrector(w.var('y'), g2, w.var('x'), g1, 1e-3)
    plot21 = w.var('y').frame()
    plot21.SetTitle('')
    plot21.GetXaxis().SetTitle('Raw y')
    plot21.GetYaxis().SetTitle('Corrected y')
    qq21.plotOn(plot21, roo.LineColor(ROOT.kRed))
    canvases.next('qq21').SetGrid()
    plot21.Draw()

    func12 = qq12.get_hist_func()
    plot12f = w.var('x').frame()
    plot12f.SetTitle('')
    plot12f.GetXaxis().SetTitle('Raw x')
    plot12f.GetYaxis().SetTitle('Corrected x')
    qq12.plotOn(plot12f)
    func12.plotOn(plot12f, roo.LineColor(ROOT.kRed), 
                  roo.LineStyle(ROOT.kDashed))
    canvases.next('qq12f').SetGrid()
    plot12f.Draw()
    
    canvases.update()
## End of test()
    

#_______________________________________________________________________________
if __name__ == '__main__':
    import user
    roo.silence()
    test()
