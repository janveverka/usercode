## Produces pdf plots of muon reconstruction 
## efficiencies for (data/MC) x (tracker/stand-alone/matching)
## in the current location.
## USAGE: python -i muonefficiencies.py

import copy
import os
import ROOT

import FWLite.Tools.canvases as canvases
import FWLite.Tools.cmsstyle as cmsstyle

from FWLite.Tools.latex import Latex

#______________________________________________________________________________
class Plotter:
    '''Holds information about the efficiencies data'''
    def makeplot(self):
        '''Produces a canvas with a plot. Assumes configuration 
        Data is present.'''
        self.sourcepath = os.path.join(basepath, 
                                       self.sourcedir, 
                                       self.sourcefilename)
        self.source = ROOT.TFile.Open(self.sourcepath)
        histo = self.source.Get(self.sourcehistoname).Clone()
        ## Set the titles
        for obj, txt in [(histo           , self.title ),
                         (histo.GetXaxis(), self.xtitle), 
                         (histo.GetYaxis(), self.ytitle)]:
            obj.SetTitle(txt)

        histo.SetStats(False)

        self.canvas = canvases.next(self.name)
        histo.DrawCopy('colz')
        self.histo = self.canvas.GetListOfPrimitives().FindObject(
            histo.GetName()
            )
        self.histo.GetZaxis().SetRangeUser(0.9, 1.0)
        Latex([self.leftlabel], (0.15, 0.92), textsize=25).draw()
        Latex([self.rightlabel], (0.615, 0.92), textsize=25).draw()

        canvases.update()
    ## End of makeplot
## End of class Plotter

plots = []
## Configuration BEGIN
basepath = os.environ['CMSSW_BASE']

plot = Plotter()

## Common for all plots
plot.sourcedir = 'src/Vgamma/Analysis/data/muonSF'
plot.title = ''
plot.rightlabel = 'CMS Preliminary'
plot.xtitle = 'Muon #eta'
plot.ytitle = 'Muon p_{T} (GeV)'
plot.sourcefilename = 'EffMapsV2.root'
plot.ztitle = 'Reconstruction Efficiency'

## Specific for Data/MC x TR/SA/MA
plot.sourcehistoname = 'TPTR_MC'
plot.leftlabel = 'Inner Track Reco. Efficiency'
plot.rightlabel = 'CMS Simulation'
plot.name = 'Muon_Reco_Eff_TR_MC'
plots.append(copy.deepcopy(plot))

plot.sourcehistoname = 'TPTR_DATA'
plot.leftlabel = 'Inner Track Reco. Efficiency'
plot.rightlabel = 'CMS Preliminary'
plot.name = 'Muon_Reco_Eff_TR_DATA'
plots.append(copy.deepcopy(plot))

plot.sourcehistoname = 'TPSA_MC'
plot.leftlabel = 'Outer Track Reco. Efficiency'
plot.rightlabel = 'CMS Simulation'
plot.name = 'Muon_Reco_Eff_SA_MC'
plots.append(copy.deepcopy(plot))

plot.sourcehistoname = 'TPSA_DATA'
plot.leftlabel = 'Outer Track Reco. Efficiency'
plot.rightlabel = 'CMS Preliminary'
plot.name = 'Muon_Reco_Eff_SA_DATA'
plots.append(copy.deepcopy(plot))

plot.sourcehistoname = 'TPMA_MC'
plot.leftlabel = 'Matching Efficiency'
plot.rightlabel = 'CMS Simulation'
plot.name = 'Muon_Reco_Eff_MA_MC'
plots.append(copy.deepcopy(plot))

plot.sourcehistoname = 'TPMA_DATA'
plot.leftlabel = 'Matching Efficiency'
plot.rightlabel = 'CMS Preliminary'
plot.name = 'Muon_Reco_Eff_MA_DATA'
plots.append(copy.deepcopy(plot))

## Configuration END

ROOT.gStyle.SetPalette(55)
ROOT.gStyle.SetPadLeftMargin(0.15)
ROOT.gStyle.SetPadRightMargin(0.15)
ROOT.gStyle.SetPadTopMargin(0.1)
ROOT.gStyle.SetPaintTextFormat('5.3f')
ROOT.gROOT.ForceStyle()

for p in plots[:]:
    p.makeplot()

canvases.make_pdf_from_eps()
