'''
Implements PhotonIdCorrector
Jan Veverka, MIT, jan.veverka@cern.ch
28 July 2013
'''
import ROOT
import FWLite.Tools.roofit as roo
from FWLite.Tools.legend import Legend
from FWLite.Tools.qqcorrector import QQCorrector

#______________________________________________________________________________
class PhotonIdCorrector(QQCorrector):
    '''
    Calculates the Q-Q Corrections for the photon ID inputs.
    '''
    #__________________________________________________________________________
    def __init__(self, raw_data, target_data, rho=1.,
                 mirror=ROOT.RooKeysPdf.NoMirror,
                 raw_color    = ROOT.kRed,
                 target_color = ROOT.kBlack,
                 qq_color     = ROOT.kBlue):
        if raw_data.get().getSize() > 1:
            raise RuntimeError, 'Raw data must contain exactly one variable!'
        self.raw_data = raw_data
        self.target_data = target_data
        self.rho = rho
        self.mirror = mirror
        self.raw_color = raw_color
        self.target_color = target_color
        self.qq_color = qq_color
        self.variable = xvar = raw_data.get().first()
        raw_pdf = ROOT.RooKeysPdf(xvar.GetName() + '_raw_pdf',
                                  xvar.GetTitle() + ' Raw PDF',
                                  xvar, raw_data, mirror, rho)
        target_pdf = ROOT.RooKeysPdf(xvar.GetName() + '_target_pdf',
                                     xvar.GetTitle() + ' Target PDF',
                                     xvar, target_data, mirror, rho)
        QQCorrector.__init__(self, xvar, raw_pdf, xvar, target_pdf)
    ## End of PhotonIdCorrector.__init__(...)

    #__________________________________________________________________________
    def get_validation_plot(self):
        plot = self.variable.frame()
        plot.SetTitle(self.GetTitle() + ' Validation')
        scale = self.target_data.sumEntries() / self.raw_data.sumEntries()
        self.corrected_data = self.get_corrected_data()
        self.target_data.plotOn(plot, roo.Name('target'),
                                *color_args(self.target_color))
        self.raw_data.plotOn(plot, roo.Name('raw'), roo.Rescale(scale),
                             roo.MarkerStyle(24), *color_args(self.raw_color))
        self.corrected_data.plotOn(plot, roo.Name('corrected'), 
                                   roo.Rescale(scale), roo.MarkerStyle(25), 
                                   *color_args(self.qq_color))
        names = 'target raw corrected'.split()
        histos = [plot.findObject(name) for name in names]
        titles = [name.capitalize() for name in names]        
        plot.legend = Legend(histos, titles)        
        ## Some syntactic sugar to get automatic legend drawing
        plot.DrawBase = plot.Draw
        plot.Draw = lambda: plot.DrawBase() or plot.legend.draw()
        return plot
    ## End of PhotonIdCorrector.get_validation_plot(self)
    
    #__________________________________________________________________________
    def get_corrected_data(self):
        '''
        Returns a dataset with the raw data corrected to the target.
        '''
        corrected_data = self.raw_data.Clone()
        corrected_data.addColumn(self)
        #corrected_data.Print('v')
        qq_variable = corrected_data.get()[self.GetName()]
        corrected_data = corrected_data.reduce(ROOT.RooArgSet(qq_variable))
        qq_variable = corrected_data.get()[self.GetName()]        
        qq_variable.SetName(self.variable.GetName())
        #corrected_data.Print('v')
        return corrected_data
    ## End of PhotonIdCorrector.get_corrected_data()    
## End of class PhotonIdCorrector

#__________________________________________________________________________
def color_args(color):
    '''
    Returns the two RooFit commands to set marker and line color to the 
    givne one.
    '''
    return roo.MarkerColor(color), roo.LineColor(color)
## End of color_args


#______________________________________________________________________________
def test():
    '''
    Tests the PhotonIdCorrector class.
    '''
    corr = PhotonIdCorrector()
    pass
## End of test()


#______________________________________________________________________________
if __name__ == '__main__':
    import user
    test()
