import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.canvases as canvases
## Provides RooCauchy
import FWLite.Tools.tools as tools

from FWLite.Tools.qqcorrector import QQCorrector

#______________________________________________________________________________
# Setup
w = ROOT.RooWorkspace('w', 'Q-Q Corrections test')
g1 = w.factory('Gaussian::g1(x[-5, 5], m1[0], s1[1])')
g2 = w.factory('BreitWigner::g2(y[-5, 7], m2[1], s2[1.2])')

#______________________________________________________________________________
xplot = w.var('x').frame()
g1.plotOn(xplot)
canvases.next('g1_x').SetGrid()
xplot.Draw()

#______________________________________________________________________________
yplot = w.var('y').frame()
g2.plotOn(yplot)
canvases.next('g2_y').SetGrid()
yplot.Draw()

#______________________________________________________________________________
qq12 = QQCorrector(w.var('x'), g1, w.var('y'), g2, 1e-4)
plot12 = w.var('x').frame()
plot12.SetTitle('')
plot12.GetXaxis().SetTitle('Raw x')
plot12.GetYaxis().SetTitle('Corrected x')
qq12.plotOn(plot12)
canvases.next('qq12').SetGrid()
plot12.Draw()

#______________________________________________________________________________
plot12v2 = qq12.get_correction_plot()
canvases.next('qq12v2').SetGrid()
plot12v2.Draw()

#______________________________________________________________________________
## Persist the corrector in a file as RooHistFunc
qq12.SetName('qqcorr')
qq12.write_to_file('test_qqcorrector.root')

#______________________________________________________________________________
## Persist the corrector in a file as RooHistFunc
qqfile = ROOT.TFile.Open('test_qqcorrector.root', 'update')
graph = qq12.get_interpolation_graph(granularity=20)
graph.SetName('qqcorr_graph')
graph.Write()
qqfile.Close()

#______________________________________________________________________________
## Read the corrector from a file and plot on top of the original
qqfile = ROOT.TFile.Open('test_qqcorrector.root')
qqfile.ls()
workspace = qqfile.Get('qqcorr')
workspace.Print()
func12 = workspace.function('qqcorr')
plot12f = w.var('x').frame()
plot12f.SetTitle('')
plot12f.GetXaxis().SetTitle('Raw x')
plot12f.GetYaxis().SetTitle('Corrected x')
qq12.plotOn(plot12f)
func12.plotOn(plot12f, roo.LineColor(ROOT.kRed), 
              roo.LineStyle(ROOT.kDashed))
graph = qqfile.Get('qqcorr_graph')
canvases.next('qq12f').SetGrid()
plot12f.Draw()
graph.Draw('p')

canvases.update()
#qqfile.Close()

#______________________________________________________________________________
if __name__ == '__main__':
    import user
