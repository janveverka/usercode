import ROOT
import FWLite.Tools.roofit as roo
from FWLite.Tools.resampler import Resampler


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

    ROOT.RooRandom.randomGenerator().SetSeed(2)
    global gnlls, hrhoval, hrhoerr
    hrhoval = ROOT.TH1F('hrhoval', 'hrhoval', 100, 0, 5)
    hrhoerr = ROOT.TH1F('hrhoerr', 'hrhoerr', 100, 0, 1)
    gnlls = []
    for itoy in range(1):
        global w
        w = ROOT.RooWorkspace('w', 'w')
        # model = w.factory('Gaussian::model(x[-50, 50], mean[0], sigma[1])')
        model = w.factory('BreitWigner::model(x[-5, 5], mean[0], sigma[1])')
        x = w.var('x')
        oset = ROOT.RooArgSet(x)
        data = model.generate(oset, 1000)
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

        rho.setVal(2)
        testpdf.LoadDataSet(data)
        testpdf.plotOn(plot, roo.LineColor(ROOT.kGreen))

        rho.setVal(3)
        testpdf.LoadDataSet(data)
        testpdf.plotOn(plot, roo.LineColor(ROOT.kBlack))

        canvases.next('RooRhoKeysPdf_Test%d' % itoy)
        plot.Draw()
        canvases.update()

        resampler = Resampler(data)
        data0 = resampler.prescale(2, [0], 'data0')
        data1 = resampler.prescale(2, [1], 'data1')
        w.Import(data0)
        w.Import(data1)
        testpdf0 = w.factory('RooRhoKeysPdf::testpdf0(x, rho, data0)')
        testpdf1 = w.factory('RooRhoKeysPdf::testpdf1(x, rho, data1)')

        gnll = ROOT.TGraph()
        for rhoval in [0.5 + 0.05 * i for i in range(50)]:
            rho.setVal(rhoval)
            testpdf0.LoadDataSet(data0)
            testpdf1.LoadDataSet(data1)
            nll = 0
            nll += testpdf0.createNLL(data1).getVal()
            nll += testpdf1.createNLL(data0).getVal()
            # print rhoval, nll
            gnll.SetPoint(gnll.GetN(), rhoval, nll)

        locmin = ROOT.TMath.LocMin(gnll.GetN(), gnll.GetY())
        xmin = gnll.GetX()[max(locmin-5, 0)]
        xmax = gnll.GetX()[min(locmin+5, gnll.GetN()-1)]
        fres = gnll.Fit('pol2', 's', '', xmin, xmax)
        p1 = fres.Get().GetParams()[1]
        p2 = fres.Get().GetParams()[2]
        rhoval =  - 0.5 * p1 / p2
        rhoerr = 1/ROOT.TMath.Sqrt(2 * p2)
        hrhoval.Fill(rhoval)
        hrhoerr.Fill(rhoerr)
        
        canvases.next('gnll%d' % itoy)
        gnll.Draw('ap')
        gnll.GetXaxis().SetTitle('#rho')
        gnll.GetYaxis().SetTitle('- log L')
        gnlls.append(gnll)
    canvases.next('rhoerr')
    hrhoerr.Draw()
    canvases.next('rhoval')
    hrhoval.Draw()
    canvases.update()

    from FWLite.Tools.modalinterval import ModalInterval
    global mi
    mi = ModalInterval(w.data('data0'))
    print mi.halfSampleMode()
    
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
    
