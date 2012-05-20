import ROOT
import FWLite.Tools.roofit as roo

ROOT.gSystem.Load('libFWLiteTools')
#ROOT.gROOT.ProcessLine('#include "FWLite/Tools/interface/RooChi2Calculator.h"')
RooRhoKeysPdf = ROOT.RooRhoKeysPdf


#_______________________________________________________________________________
def test():
    '''
    Tests the RooRhoKeysPdf class.
    '''
    import FWLite.Tools.canvases as canvases
    import FWLite.Tools.cmsstyle as cmsstyle

    global w
    w = ROOT.RooWorkspace('w', 'w')
    model = w.factory('Gaussian::model(x[-5, 5], mean[0], sigma[1])')
    x = w.var('x')
    oset = ROOT.RooArgSet(x)
    data = model.generate(oset, 100)
    w.Import(data)
    # rho = w.factory('rho[1, 0, 100]')
    # testpdf = RooRhoKeysPdf('testpdf', 'testpdf', x, rho, data)
    # w.Import(testpdf)
    testpdf = w.factory('RooRhoKeysPdf::testpdf(x, rho[1, 0, 100], modelData)')
    rho = w.var('rho')
    plot = x.frame()
    data.plotOn(plot)
    model.plotOn(plot)
    testpdf.plotOn(plot, roo.LineColor(ROOT.kRed))
    rho.setVal(3)
    testpdf.LoadDataSet(data)
    testpdf.plotOn(plot, roo.LineColor(ROOT.kGreen))
    # testpdf.
    canvases.next('RooRhoKeysPdf_Test')
    plot.Draw()
    canvases.update()
## End of test()



#_______________________________________________________________________________
def main():
    '''
    Main entry point of execution.
    '''
    print 'Welcome to RooRhoKeysPdf test!'
    test()
    print 'Exiting RooRhoKeysPdf test with success.'
## End of main()


#_______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user
    
