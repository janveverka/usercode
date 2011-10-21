import os
import math
import copy
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.energyScaleChains as esChains

from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *
from JPsi.MuMu.common.plotData import PlotData
from JPsi.MuMu.common.padDivider import residPullDivide

#------------------------------------------------------------------------------
class Def():
    """ScaleFitter definition that can act on an instance and modify it's
    name, title and labels to reflect a fit performed for events
    in a specific category.  This is a base class for other definitions
    implementing data source (real data/MC), fittig model and cuts."""
    def __init__(self, name, title, labels):
        self.name, self.title, self.labels = name, title, labels

    def __call__(self, fitter):
        if fitter.name:
            fitter.name += '_'
        fitter.name += self.name

        if fitter.title:
            fitter.title += ', '
        fitter.title += self.title

        fitter.labels += self.labels

    def __str__(self):
        args = []
        for attr in dir(self):
            if callable(getattr(self, attr)) or attr[0] == '_':
                continue
            value = getattr(self, attr)
            args.append(''.join([attr, '=', repr(value)]))
        args = ', '.join(args)
        return ''.join([self.__class__.__name__, '(', args, ')'])
## end of class Cut


#------------------------------------------------------------------------------
class Model(Def):
    """ScaleFitter model definition that can act on an instance and modify it's
    name, title, labels and fit model to reflect that the fit is performed
    using the specified model."""
    def __init__(self, name):
        if name == 'gauss':
            Def.__init__(self, name, 'Gauss', ['Gaussian Fit'])
            self.model = 'gauss'
        elif name == 'lognormal':
            Def.__init__(self, name, 'Lognormal', ['Lognormal Fit'])
            self.model = 'lognormal'
        elif name == 'bifurGauss':
            Def.__init__(self, name, 'Bifur.-Gauss', ['Bifur. Gaussian Fit'])
            self.model = 'bifurGauss'
        elif name == 'cbShape':
            Def.__init__(self, name, 'CB', ['Crystal Ball Fit'])
            self.model = 'cbShape'
        elif name == 'gamma':
            Def.__init__(self, name, 'Gamma', ['Gamma Fit'])
            self.model = 'gamma'
        elif name == 'cruijff':
            Def.__init__(self, name, 'Cruijff', ['Cruijff Fit'])
            self.model = 'cruijff'
        else:
            raise ValueError, 'model %s not supported!' % name

    def __call__(self, fitter):
        Def.__call__(self, fitter)
        fitter.pdf = self.model
## end of class Model

#------------------------------------------------------------------------------
class Source(Def):
    """ScaleFitter source definition that can act on an instance and modify it's
    name, title, labels and data source to reflect that the fit is performed
    using the specified data source."""
    def __init__(self, name, title, labels, source):
        Def.__init__(self, name, title, labels)
        self.source = source

    def __call__(self, fitter):
        Def.__call__(self, fitter)
        fitter.source = self.source
## end of class Source


#------------------------------------------------------------------------------
class Cut(Def):
    """ScaleFitter cut definition that can act on an instance and modify it's
    name, title, labels and cuts to reflect a fit performed for events
    satisfying the cut."""
    def __init__(self, name, title, labels, cuts):
        Def.__init__(self, name, title, labels)
        self.cuts = cuts

    def __call__(self, fitter):
        Def.__call__(self, fitter)
        fitter.cuts += self.cuts

#     def __str__(self):
#         args = ', '.join(repr(arg) for arg in [self.name, self.title,
#                                                self.labels, self.cuts,])
#         return ''.join([self.__class__.__name__, '(', args, ')'])
## end of class Cut


#------------------------------------------------------------------------------
class PhoEtBin(Cut):
    """Can act on a ScaleFitter object and modify it's name,
    title, labels and cuts to reflect a fit performed for photon within the
    given Et bin [low,high) GeV."""
    def __init__(self, low, high):
        bin_range = (low, high)
        self.bin_range = bin_range
        Cut.__init__(self,
            name = 'PhoEt%g-%g' % bin_range,
            title = 'photon Et in [%g, %g) GeV' % bin_range,
            labels = ['E_{T}^{#gamma} #in [%g, %g) GeV' % bin_range],
            cuts = ['%g <= phoPt' % low, 'phoPt < %g' % high],
        )

    def __str__(self):
        return self.__class__.__name__ + '(%g, %g)' % self.bin_range
## end of class PhoEtBin


#------------------------------------------------------------------------------
class DimuonMassMax(Cut):
    """Can act on a ScaleFitter object and modify it's name,
    title, labels and cuts to reflect a fit performed for dimuons below the
    given mass in GeV."""
    def __init__(self, max):
        self.max = max
        Cut.__init__(self,
            name = 'mmMass%g' % max,
            title = 'mmMass < %g GeV' % max,
            labels = ['m_{#mu^{+}#mu^{-}} < %g GeV' % max],
            cuts = ['mmMass <= %g' % max],
        )

    def __str__(self):
        return self.__class__.__name__ + '(%g)' % self.max
## end of class PhoEtBin


#------------------------------------------------------------------------------
class ICut():
    """Iterator over instances of Cut. The constructor arguments are
      * names - list of strings to form filenames
      * titles - list of strings for log files and ASCII reports
      * labels - list of lists of latex strings for canvases and latex reports
      * cuts - list of lists of TTree::Draw expression strings."""
    def __init__(self, names, titles, labels, cuts):
        self.name, self.title = iter(names), iter(titles)
        self.labels, self.cuts = iter(labels), iter(cuts)

    def __iter__(self):
        return self

    def next(self):
        return Cut(self.name.next(), self.title.next(),
                   self.labels.next(), self.cuts.next())
## end of ICut


class ScaleFitter(PlotData):
    """Fits the Crystal Ball line shape to s = Ereco / Ekin - 1"""
    #--------------------------------------------------------------------------
    def __init__( self, name, title, source, xExpression, cuts, labels,
                  **kwargs ):
        self.xName = 's'
        self.xTitle = 's = E_{RECO}/E_{KIN} - 1'
        self.nBins = 40
        self.xRange = (-30, 50)
        self.xUnit = '%'
        self.fitRange = (-30, 30)
        self.massWindow = None
        self.massWindowScale = 2
        self.fitResults = []
        self.canvases = []
        self.pads = []
        self.pdf = 'model'
        self.chi2s = []
        self.definitions = []
        self.paramLayout = (.57, 0.92, 0.92)
        self.labelsLayout = (0.61, 0.6)

        ## Chi2 statistic follows the chi2 PDF (and one can trust the p-value
        ## from ROOT if int(f(x), x in bin_i) = nu_i > 5, see explanation
        ## near (33.34) on page 13 of the 2011 PDG Statistics Review
        ## http://pdg.lbl.gov/2011/reviews/rpp2011-rev-statistics.pdf
        ## Use bin content n_i >= 10 to be on the safe side (nu_i != n_i)
        self.binContentMin = 10

        PlotData.__init__( self, name, title, source, xExpression, cuts,
                           labels, **kwargs )

    ## <-- __init__ -----------------------------------------------------------

    #--------------------------------------------------------------------------
    def applyDefinitions(self, definitions=[]):
        """Applies definitions."""
        self.definitions.extend(definitions)
        ## The definitions are applied in the same order as they appear in the
        ## list.  They will be `pop'-ped from the tail of the reversed list.
        self.definitions.reverse()
        ## Unfinite loop
        while True:
            try:
                ## Get the next definition and remove it from the list.
                definition = self.definitions.pop()
                ## Apply the definition.
                definition(self)
            except IndexError:
                ## The list of definitions is empty.
                break
        ## end of unfinite while loop
        return self
    ## end of applyDefinitions

    #--------------------------------------------------------------------------
    def getMassCut(self, workspace):
        """Uses the mmg invariant mass distribution to center the invariant
        mass window and adust its size. Appends the invariant mass cut to
        the list of cuts."""

        ## Check if mass window is explicitly given
        if self.massWindow:
            ## Append the given mass window to the list of cuts
            mean = 0.5 * (self.massWindow[0] + self.massWindow[1])
            width = 0.5 * (self.massWindow[1] - self.massWindow[0])
            self.cuts.append( 'abs(mmgMass-%.2f) < %.2f' % (mean, width) )
            ## Return without making the fit
            return

        mean = 91.2
        width = 4.
        mmgMass = workspace.var('mmgMass')
        mmgMass.SetTitle('mmgMass')
        data = dataset.get(
            tree = self.source,
            variable = mmgMass,
            weight = workspace.var('w'),
            cuts = self.cuts
        )
        m3Model = workspace.pdf('m3Model')
        m3Model.fitTo(data, SumW2Error(kTRUE))
        workspace.saveSnapshot( 'm3_' + self.name,
                                workspace.set('m3Model_params') )
        canvas = TCanvas( 'm3_' + self.name, 'Mass fit, ' + self.title )
        self.canvases.append( canvas )
        i = len(gROOT.GetListOfCanvases())
        canvas.SetWindowPosition(20*(i%50), 20*(i%5))
        canvas.SetGrid()

        ## Extract the approximate mass cut and append it to the current cuts
        center = workspace.var('mZ').getVal() + workspace.var('#Deltam').getVal()
        sigmaCB = workspace.var('#sigmaCB').getVal()
        sigmaBW = workspace.var('#GammaZ').getVal()
        oplus = lambda x, y: math.sqrt(x*x + y*y)
        width = self.massWindowScale * oplus(sigmaCB, sigmaBW)

        ## Tune the position of the mass window by sample the signal pdf
        nsamples = 1000
        xlo, dx = center - width, 2*width/(nsamples-1)
        signal = workspace.pdf('signal')
        xmax, ymax = -1, -1
        for x in [xlo + i*dx for i in range(nsamples)]:
            mmgMass.setVal(x)
            y = signal.getVal()
            if y > ymax:
                xmax, ymax = x, y
        self.cuts.append( 'abs(mmgMass-%.2f) < %.2f' % (xmax, width) )
        self.massWindow = (xmax - width, xmax + width)

        ## Plot the fit result
        mmgMass.SetTitle('m_{#mu#mu#gamma}')
        plot = mmgMass.frame(Range(60,120))
        plot.SetTitle('')
        data.plotOn(plot)
        m3Model.paramOn( plot,
                         Format('NEU', AutoPrecision(2) ),
                         Layout(.65, 0.92, 0.92) )
        m3Model.plotOn(plot)
        plot.Draw()

        ## Initialize latex label
        latexLabel = TLatex()
        latexLabel.SetNDC()
        ## Font size in pixels
        latexLabel.SetTextFont(10*(latexLabel.GetTextFont()/10) + 3)
        latexLabel.SetTextSize(18)

        ## Add mass window label
        latexLabel.DrawLatex( 0.65, 0.6 - 5 * 0.055,
                              '%.2f #pm %.2f GeV' % (xmax, width) )

        ## Plot the mass window
        canvas.Update()
        mmgMass.setVal(center)
        xlo = xmax - width
        xhi = xmax + width
        ylo = 0.
        yhi = 0.8 * canvas.GetY2()
        line1 = ROOT.TLine(xlo, ylo, xlo, yhi)
        line2 = ROOT.TLine(xhi, ylo, xhi, yhi)
        arrow1 = ROOT.TArrow(xlo, 0.5*yhi, xhi, 0.5*yhi, 0.01, '<>')
        for piece in [line1, line2, arrow1]:
            try:
                self.primitives.append(piece)
            except AttributeError:
                self.primitives = []
                self.primitives.append(piece)
            piece.Draw()

        ## Save the plot
        if hasattr(self, 'graphicsExtensions'):
            for ext in self.graphicsExtensions:
                canvas.Print( 'massFit_' + self.name + '.' + ext )
    ## <-- getMassCut ---------------------------------------------------------

    #--------------------------------------------------------------------------
    def getData(self, workspace):
        """Gets the data and imports it in the workspace."""
        ## Pull fitted variable x, its weight w, the model
        ## and its parameters from the workspace
        self.x = workspace.var(self.xName)
        self.x.Print()
        self.w = workspace.var('w')

        self.x.SetTitle( self.xExpression )
        self.data = dataset.get(
            tree = self.source,
            variable = self.x,
            weight = self.w,
            cuts = self.cuts
        )
        self.data.SetName( 'data_' + self.name )
        self.data.SetTitle( self.title )
        workspace.Import(self.data)
    ## <-- getData ------------------------------------------------------------

    #--------------------------------------------------------------------------
    def fitToData(self, workspace, saveName = ''):
        # print "+++ Entering scaleFitter.fitToData(..)"
        self.model = workspace.pdf(self.pdf).Clone( 'model_' + self.name )
        workspace.Import( self.model )
        self.parameters = workspace.set(self.pdf + '_params')
        # print "+++ Parameters:"
        #self.parameters.Print()
        ## Fit data
#         self.x.setRange( 'fitRange_' + self.name, *self.fitRange )
        self.data.SetName( self.name )
        #print "+++ fitting"
        self.fitResults.append(
            self.model.fitTo( self.data, Save(),
                              Range(*self.fitRange),
#                               Range('fitRange_' + self.name),
                              SumW2Error(kTRUE),
                              PrintLevel(-1) )
        )

        if saveName == '':
            workspace.saveSnapshot('sFit_' + self.name, self.parameters, True)
        else:
            workspace.saveSnapshot( saveName, self.parameters, True )
    ## <-- fitToData ----------------------------------------------------------

    #--------------------------------------------------------------------------
    def _customizeAxis(self, axis, labelOffset=0.005, titleOffset=1):
        ## Switch to fixed pixel size fonts
        precision = axis.GetLabelFont() % 10
        axis.SetLabelFont( axis.GetLabelFont() - precision + 3 )
        axis.SetLabelSize(18)
        precision = axis.GetTitleFont() % 10
        axis.SetTitleFont( axis.GetTitleFont() - precision + 3)
        axis.SetTitleSize(18)
        ## Scale offsets
        axis.SetLabelOffset( labelOffset )
        axis.SetTitleOffset( titleOffset )
    # end of customize axis

    #--------------------------------------------------------------------------
    def _getBinning(self):
        'Get bins with more than self.binContentMin. Useful for chi2 statistic'
        'that obeys the chi2 PDF.'

        ## Histogram the data
        self.x.setBins(self.nBins)
        self.x.SetTitle(self.xTitle)

        plot = self.x.frame(Range(*self.xRange))
        self.data.plotOn(plot)
        hist = plot.getHist()

        ## Determine the range of the binning
        xstart, xstop = self.xRange

        ## Create the target binning
        bins = ROOT.RooBinning(xstart, xstop)
        bins.Print()
        boundaries = []
        contents = []
        
        ## Loop over all the default bins forward, copy to the new binning,
        ## merge them if needed.
        binContent = 0.
        for i in range(hist.GetN()):
            xlo = hist.GetX()[i] - hist.GetErrorXlow(i)
            xhi = hist.GetX()[i] + hist.GetErrorXhigh(i)
            binContent += hist.GetY()[i]

            ## Only consider bins inside of the range
            if xlo < xstart or xstop < xhi:
                continue

            if binContent >= self.binContentMin:
                if bins.hasBoundary(xhi):
                    continue
                boundaries.append(xhi)
                contents.append(binContent)
                binContent = 0.
            ## End of forward loop over bins

        ## The last bin may have too low content. Walk over the new bins
        ## backward and remove boundaries as needed.
        ## Create a new histogram with the new bins
        boundaries.reverse()
        contents.reverse()
        for boundary, content in zip(boundaries, contents):
            if binContent >= self.binContentMin:
                break
            binContent += content
            boundaries.remove(boundary)
        ## End of backward loop over the new boundaries

        for boundary in boundaries:
            bins.addBoundary(boundary)
            
        return bins
    ## end of _getBinning

                
    #--------------------------------------------------------------------------
    def makePlot(self, workspace):
        ## Get custom binning with at least self.binContentMin events per bin.
        self.bins = self._getBinning()

        self.x.SetTitle(self.xTitle)
        self.x.setBinning(self.bins)
        ## Make a frame
        self.plot = self.x.frame()
 
        ## Add the data and model to the frame
        self.data.plotOn(self.plot, Binning(self.bins))
        self.model.plotOn(self.plot,
                          Normalization(
                              float(self.bins.numBins()) / self.nBins
                              )
                          )
        self.chi2s.append( self.plot.chiSquare( self.parameters.getSize() ) )
        self.model.paramOn( self.plot,
                            Format('NEU', AutoPrecision(2) ),
                            Parameters( self.parameters ),
                            Layout(*self.paramLayout) )

        ## Make a canvas
        self.canvas = TCanvas( self.name, self.name, 400, 800 )
        self.canvases.append( self.canvas )
        i = len( gROOT.GetListOfCanvases() )
        self.canvas.SetWindowPosition(20*(i%50), 20*(i%5))
        self.pads.extend( residPullDivide(self.canvas) )

        # self.canvas.cd(1)

        ## To get a well defined chi2 statistics, merge bins
        ## with less than 10 events.
        
        ## Get the residual and pull dists
        hresid = self.plot.residHist()
        hpull  = self.plot.pullHist()
        self.plot2 = self.x.frame( Range( *self.xRange ) )
        self.plot3 = self.x.frame( Range( *self.xRange ) )
        self.plot2.SetYTitle('#chi^{2} Residuals')
        self.plot3.SetYTitle('#chi^{2} Pulls')
        self.plot2.addPlotable(hresid, 'P')
        self.plot3.addPlotable(hpull, 'P')

        ## Customize
        self.plot.SetTitle('')
        self.plot2.SetTitle('')
        self.plot3.SetTitle('')

        self._customizeAxis( self.plot.GetYaxis(), 0.01, 3 )
        self._customizeAxis( self.plot2.GetYaxis(), 0.01, 3 )
        self._customizeAxis( self.plot3.GetYaxis(), 0.01, 3 )
        self._customizeAxis( self.plot3.GetXaxis(), 0.01, 3.5 )

        ## Draw the frames
        for pad, plot in [ (self.canvas.cd(1), self.plot),
                           (self.canvas.cd(2), self.plot2),
                           (self.canvas.cd(3), self.plot3), ]:
            pad.cd()
            pad.SetGrid()
            plot.GetYaxis().CenterTitle()
            plot.Draw()

        self.canvas.cd(1)

        ## Save the chi2 and ndof in the workspace
        if workspace.var('reducedChi2'):
            reducedChi2 = workspace.var('reducedChi2')
            ndof = workspace.var('ndof')
            chi2Prob = workspace.var('chi2Prob')
        else:
            reducedChi2 = RooRealVar( 'reducedChi2', 'fit #chi^{2}/ndof', -1 )
            ndof = RooRealVar( "ndof", "fit n.d.o.f.", -1 )
            chi2Prob = RooRealVar( 'chi2Prob', '#chi^{2} probability', -1 )
            workspace.Import(reducedChi2)
            workspace.Import(ndof)
            workspace.Import(chi2Prob)
        reducedChi2.setVal( self.chi2s[-1] )
        ndof.setVal( self.plot2.getHist().GetN() - self.parameters.getSize() )
        chi2Prob.setVal( TMath.Prob( reducedChi2.getVal() * ndof.getVal(),
                                    int( ndof.getVal() ) ) )
        chi2 = RooArgSet( reducedChi2, ndof, chi2Prob )
        workspace.saveSnapshot( 'chi2_' + self.name, chi2, True )

        ## Initialize latex label
        latexLabel = TLatex()
        latexLabel.SetNDC()
        ## Font size in pixels
        latexLabel.SetTextFont( 10*(latexLabel.GetTextFont()/10) + 3)
        latexLabel.SetTextSize(18)

        ## Add labels
        for i in range( len( self.labels ) ):
            latexLabel.DrawLatex(self.labelsLayout[0],
                                 self.labelsLayout[1] - i*0.055, self.labels[i])

        ## Add the total number of events used
        numLabels = len( self.labels )
        latexLabel.DrawLatex( self.labelsLayout[0],
                              self.labelsLayout[1] - numLabels * 0.055,
                              '%d events' % self.data.numEntries() )
        ## Add the reduced chi2
        latexLabel.DrawLatex( self.labelsLayout[0],
                              self.labelsLayout[1] - (numLabels+1) * 0.055,
                              '#chi^{2}/ndof: %.2g' % reducedChi2.getVal() )
        ## Add the chi2 and ndof
        self.canvas.cd(2)
        chi2Val = reducedChi2.getVal() * ndof.getVal()
        ndofVal = int( ndof.getVal() )
        latexLabel.DrawLatex( self.labelsLayout[0], 0.85, '#chi^{2}: %.2g' % chi2Val)
        latexLabel.DrawLatex( self.labelsLayout[0], 0.75, 'ndof: %d' % ndofVal)

        ## Add the chi2 probability
        self.canvas.cd(3)
        latexLabel.DrawLatex(self.labelsLayout[0], 0.867, 'Prob: %.2g' % chi2Prob.getVal())

        ## Save the plots
        if hasattr(self, 'graphicsExtensions'):
            for ext in self.graphicsExtensions:
                self.canvas.Print( 'sFit_' + self.name + '.' + ext )
    ## <-- makePlot -----------------------------------------------------------

    #--------------------------------------------------------------------------
    def fit(self, workspace, saveName = ''):
        self.getMassCut(workspace)
        self.getData(workspace)
        self.fitToData(workspace, saveName)
        self.makePlot(workspace)
    ## <-- fit ----------------------------------------------------------------

## <-- ScaleFitter ------------------------------------------------------------

subdet_r9_categories = ICut(
    names = 'EB_lowR9 EB_highR9 EE_lowR9 EE_highR9'.split(),
    titles = ('Barrel, R9 < 0.94',
              'Barrel, R9 > 0.94',
              'Endcaps, R9 < 0.95',
              'Endcaps, R9 > 0.95'),
    ## For latex labels on plots
    labels = (('Barrel', 'R_{9}^{#gamma} < 0.94'),
              ('Barrel', 'R_{9}^{#gamma} > 0.94'),
              ('Endcaps', 'R_{9}^{#gamma} < 0.95'),
              ('Endcaps', 'R_{9}^{#gamma} > 0.95'),),
    ## For TTree selection expressions
    cuts = (('phoIsEB' , 'phoR9 < 0.94'),
            ('phoIsEB' , 'phoR9 > 0.94'),
            ('!phoIsEB' , 'phoR9 < 0.95'),
            ('!phoIsEB' , 'phoR9 > 0.95'),)
)

## model_names = 'gauss cbShape lognormal curijff gamma'.split()
## model_titles = 'Gauss CB Lognaormal Cruijff Gamma'.split()
## model_labels = [[i] for i in model_titles]
## models = {}
## for args in zip(model_names, model_titles, model_labels, model_names):
##     models[ars[0]] = Model(*args)

if __name__ == "__main__":
    test_fitter = ScaleFitter(
        name = 's',
        title = 's-Fit',
        cuts = ['mmMass < 80'],
        labels = [],
        source = '_chains["z"]',
        xExpression = '100 * (1/kRatio - 1)',
        xRange = (-20, 40),
        nBins = 120,
        fitRange = (-100, 100),
        pdf = 'lognormal',
        graphicsExtensions = [],
        massWindowScale = 1.5,
        fitScale = 2.0,
    )

    print test_fitter.applyDefinitions().pydump()

    eb_lor9, eb_hir9, ee_lor9, ee_hir9 = list(subdet_r9_categories)

    print "Applying", eb_lor9.title
    print test_fitter.applyDefinitions([eb_lor9]).pydump()

    pt10_15 = PhoEtBin(10, 15)
    print "Applying", pt10_15.title
    print test_fitter.applyDefinitions([pt10_15]).pydump()

    import user
