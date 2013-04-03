## Produces pdf plots of electron reconstruction 
## efficiencies for (data/MC) x (barrel/endcap) x (2011A/2011B)
## in the current location.
## USAGE: python -i electronefficiencies.py

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
plot.sourcedir = 'src/Vgamma/Analysis/data/EleRecoEfficiency'
plot.title = ''
plot.rightlabel = 'CMS Preliminary'
plot.xtitle = 'Vertex Multiplicity'
plot.ytitle = 'Electron p_{T} (GeV)'

## Specific for 2011A/2011B x Data/MC x EB/EE
plot.sourcefilename = 'Efficiency_2011A/Efficiency.root'
plot.sourcehistoname = 'MC_Barrel'
plot.leftlabel = 'Run 2011A, ECAL Barrel'
plot.rightlabel = 'CMS Simulation'
plot.name = 'Electron_Reco_Eff_EB_A_MC'
plots.append(copy.deepcopy(plot))

plot.sourcefilename = 'Efficiency_2011A/Efficiency.root'
plot.sourcehistoname = 'DataA_Barrel'
plot.leftlabel = 'Run 2011A, ECAL Barrel'
plot.rightlabel = 'CMS Preliminary'
plot.name = 'Electron_Reco_Eff_EB_A_Data'
plots.append(copy.deepcopy(plot))

plot.sourcefilename = 'Efficiency_2011A/Efficiency.root'
plot.sourcehistoname = 'MC_Endcap'
plot.leftlabel = 'Run 2011B, ECAL Endcap'
plot.rightlabel = 'CMS Simulation'
plot.name = 'Electron_Reco_Eff_EE_A_MC'
plots.append(copy.deepcopy(plot))

plot.sourcefilename = 'Efficiency_2011A/Efficiency.root'
plot.sourcehistoname = 'DataA_Endcap'
plot.leftlabel = 'Run 2011A, ECAL Endcap'
plot.rightlabel = 'CMS Preliminary'
plot.name = 'Electron_Reco_Eff_EE_A_Data'
plots.append(copy.deepcopy(plot))

plot.sourcefilename = 'Efficiency_2011B/Efficiency.root'
plot.sourcehistoname = 'MC_Barrel'
plot.leftlabel = 'Run 2011B, ECAL Barrel'
plot.rightlabel = 'CMS Simulation'
plot.name = 'Electron_Reco_Eff_EB_B_MC'
plots.append(copy.deepcopy(plot))

plot.sourcefilename = 'Efficiency_2011B/Efficiency.root'
plot.sourcehistoname = 'DataB_Barrel'
plot.leftlabel = 'Run 2011B, ECAL Barrel'
plot.rightlabel = 'CMS Preliminary'
plot.name = 'Electron_Reco_Eff_EB_B_Data'
plots.append(copy.deepcopy(plot))

plot.sourcefilename = 'Efficiency_2011B/Efficiency.root'
plot.sourcehistoname = 'MC_Endcap'
plot.leftlabel = 'Run 2011B, ECAL Endcap'
plot.rightlabel = 'CMS Simulation'
plot.name = 'Electron_Reco_Eff_EE_B_MC'
plots.append(copy.deepcopy(plot))

plot.sourcefilename = 'Efficiency_2011B/Efficiency.root'
plot.sourcehistoname = 'DataB_Endcap'
plot.leftlabel = 'Run 2011B, ECAL Endcap'
plot.rightlabel = 'CMS Preliminary'
plot.name = 'Electron_Reco_Eff_EE_B_Data'
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
