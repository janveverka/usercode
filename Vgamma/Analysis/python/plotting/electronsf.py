## Produces pdf plots of electrons data/efficiency scale factors in 
## the current location.
## USAGE: python -i photonsf.py

import copy
import os
import ROOT

import FWLite.Tools.canvases as canvases
import FWLite.Tools.cmsstyle as cmsstyle

from FWLite.Tools.latex import Latex

#______________________________________________________________________________
class Plotter:
    '''Holds information about the scale factor data'''
    def makeplot(self):
        '''Produces a canvas with a plot. Assumes configuration 
        Data is present.'''
        self.sourcepath = os.path.join(basepath, 
                                       self.sourcedir, 
                                       self.sourcefilename)
        self.source = ROOT.TFile.Open(self.sourcepath)
        sfhisto = self.source.Get(self.sourcehistoname).Clone()
        ## Set the titles
        for obj, txt in [(sfhisto           , self.title ),
                         (sfhisto.GetXaxis(), self.xtitle), 
                         (sfhisto.GetYaxis(), self.ytitle)]:
            obj.SetTitle(txt)

        sfhisto.SetStats(False)

        self.canvas = canvases.next(self.name)
        sfhisto.DrawCopy('colz texte')
        self.histo = self.canvas.GetListOfPrimitives().FindObject(
            sfhisto.GetName()
            )
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
plot.sourcedir = 'src/Vgamma/Analysis/data/EIDSF'
plot.title = ''
plot.rightlabel = 'CMS Preliminary'
plot.xtitle = 'Vertex Multiplicity'
plot.ytitle = 'Electron p_{T} (GeV)'

## Specific for 2011A/2011B x EB/EE
plot.sourcefilename = 'eleIDSF_2011A.root'
plot.sourcehistoname = 'eleSF_EB'
plot.leftlabel = 'Run 2011A, ECAL Barrel'
plot.name = 'Electron_SF_A_EB'
plots.append(copy.deepcopy(plot))

plot.sourcefilename = 'eleIDSF_2011A.root'
plot.sourcehistoname = 'eleSF_EE'
plot.leftlabel = 'Run 2011A, ECAL Endcap'
plot.name = 'Electron_SF_A_EE'
plots.append(copy.deepcopy(plot))

plot.sourcefilename = 'eleIDSF_2011B.root'
plot.sourcehistoname = 'eleSF_EB'
plot.leftlabel = 'Run 2011B, ECAL Barrel'
plot.name = 'Electron_SF_B_EB'
plots.append(copy.deepcopy(plot))

plot.sourcefilename = 'eleIDSF_2011B.root'
plot.sourcehistoname = 'eleSF_EE'
plot.leftlabel = 'Run 2011B, ECAL Endcap'
plot.name = 'Electron_SF_B_EE'
plots.append(copy.deepcopy(plot))

## Configuration END

ROOT.gStyle.SetPadLeftMargin(0.15)
ROOT.gStyle.SetPadRightMargin(0.15)
ROOT.gStyle.SetPadTopMargin(0.1)
ROOT.gStyle.SetPaintTextFormat('5.3f')
ROOT.gROOT.ForceStyle()

for p in plots:
    p.makeplot()

canvases.make_pdf_from_eps()
