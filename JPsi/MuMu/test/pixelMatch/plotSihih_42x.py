import os
import JPsi.MuMu.tools as tools
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases

from array import array
from ROOT import *
from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.latex import Latex
from JPsi.MuMu.common.legend import Legend

name = 'sihih_EE'
realData = "data"
mcSamples = "z qcd w tt".split()

cweight = {
    "data": 1.,
    ## Fall 11 MC weights
    'z'  :  0.258663958360874,
    'qcd': 64.4429447069508,
    'w'  :  1.77770452633322,
    'tt' :  0.046348624723768,
}


puWeight = {
    'data': '1.',

    'z'  : 'pileup.weight',
    'tt' : 'pileup.weight',
    'w'  : 'pileup.weight',
    'qcd': 'pileup.weight',
}

colors = {
    "z"     : kAzure - 9,
    'zj'    : kSpring + 5,
    "qcd"   : kYellow - 7,
    "tt"    : kOrange - 2,
    "w"     : kRed -3,
}

legendTitles = {
    "z"   : "FSR",
    'zj'  : 'Z+jets',
    "qcd" : "QCD",
    "tt"  : "t#bar{t}",
    "w"   : "W",
}

graphs = []

## Set TDR style
# macroPath = "tdrstyle.C"
# if os.path.exists(macroPath):
#     gROOT.LoadMacro(macroPath)
#     ROOT.setTDRStyle()
#     gROOT.ForceStyle()

# gStyle.SetPadRightMargin(0.05)
print 'PadTopMargin:', gStyle.GetPadTopMargin()
gStyle.SetPadTopMargin(0.15)
print 'PadTopMargin:', gStyle.GetPadTopMargin()
# wWidth = 600
# wHeight = 600
# canvasDX = 20
# canvasDY = 20

latexLabel = TLatex()
latexLabel.SetNDC()

import JPsi.MuMu.common.pmvTrees as pmvTrees
chains = pmvTrees.getChains('v19')
tree = {}
for tag in 'data z qcd w tt'.split():
  tree[tag] = chains[tag]


if 'EB' in name:
    selection = '&'.join([
        'phoIsEB',
        'phoPt > 25',
        'scEt > 10',
        'phoHoE < 0.5',
        'abs(abs(muNearIEtaX - phoIEtaX) - 2) > 1'
        ])
else:
    selection = '&'.join([
        '!phoIsEB',
        'phoPt > 25',
        'scEt > 10',
        'phoHoE < 0.5',
        # 'abs(abs(muNearIEtaX - phoIEtaX) - 2) > 1'
        ])

###############################################################################
# Plot a quantity in data for EB
if 'EB' in name:
    yRange = (1e-4, 700.)
else:
    yRange = (1e-4, 250.)

c1 = canvases.next(name, name)
c1.SetTopMargin(0.1)

if 'EB' in name:
    ## Shifting for Barrel from AN 11/251 Vg
    var = RooRealVar("1000*phoSigmaIetaIeta - 0.11",
                     "Photon #sigma_{i#etai#eta} #times 10^{3}", 3, 15)
    varData = RooRealVar("1000*phoSigmaIetaIeta",
                         "Photon #sigma_{i#etai#eta} #times 10^{3}", 3, 15)
    var.setBins(48)
    
else:
    ## Shifting for Endcap from AN 11/251 Vg
    var = RooRealVar("1000*phoSigmaIetaIeta - 0.16",
                     "Photon #sigma_{i#etai#eta} #times 10^{3}", 10, 40)
    varData = RooRealVar("1000*phoSigmaIetaIeta",
                         "Photon #sigma_{i#etai#eta} #times 10^{3}", 10, 40)
    var.setBins(60)
    

h_temp = TH1F("h_temp", "", var.getBins(), var.getMin(), var.getMax() )
h_temp.GetXaxis().SetTitle( var.GetTitle() )
if 'EB' in name.split('_'):
    h_temp.GetYaxis().SetTitle("Events / 0.25")
else:
    h_temp.GetYaxis().SetTitle("Events / 0.5")
h_temp.SetTitle("")
h_temp.SetStats(0)
histos = {}
for tag, t in tree.items():
    sel = '(%s)' % (selection,)
    if tag == 'z':
        sel += ' && isFSR'
    if tag == 'data':
        continue
    sel = '%s * %f * (%s) ' % (puWeight[tag], cweight[tag], sel,)
    print tag, ':', sel
    t.Draw(var.GetName() + '>>h_temp', sel )
    histos[tag] = h_temp.Clone( 'h_' + tag )

sel = "%s * %f * ( (%s) && !isFSR )" % (puWeight['z'], cweight['z'], selection)
tree['z'].Draw(var.GetName() + '>>h_temp', sel)
histos['zj'] = h_temp.Clone( 'h_zj' )

tree['data'].Draw(varData.GetName() + '>>h_temp', selection )
hdata = h_temp.Clone( 'hdata' )

for tag in mcSamples + ['zj']:
    histos[tag].SetFillColor( colors[tag] )
    histos[tag].SetLineColor( colors[tag] )


## Sort histos
sortedHistos = histos.values()
sortedHistos.sort( key=lambda h: h.Integral() )

## Make stacked histos (THStack can't redraw axis!? -> roottalk)
hstacks = []
for h in sortedHistos:
    hstemp = h.Clone( h.GetName().replace("h_", "hs_") )
    if hstacks:
        hstemp.Add( hstacks[-1] )
    hstacks.append( hstemp )

## Draw
hstacks.reverse()

## Normalize MC to data
mcIntegral = hstacks[0].Integral( 1, var.getBins() )
scale = hdata.Integral(1, var.getBins() ) / mcIntegral
#scale = 1.0
print "Scaling MC by: ", scale
for hist in hstacks:
    hist.Scale( scale )


for h in hstacks:
    h.GetYaxis().SetRangeUser(*yRange)
    if hstacks.index(h) == 0: h.Draw()
    else:                     h.Draw("same")




hdata.Draw("e1 same")
c1.RedrawAxis()

## CMS Preliminary:
Latex(['CMS Preliminary 2011,  #sqrt{s} = 7 TeV'], 
      position=(0.17, 0.93), textsize=22).draw()

labels = [
    'L = 4.9 fb^{-1}',
    'E_{T}^{#gamma} > 25 GeV',
    ]

## EB or EE
if 'EB' in name:
    labels.append('ECAL Barrel')
else:
    labels.append('ECAL Endcaps')

Latex(labels, position=(0.22, 0.8), textsize=22, 
      rowheight=0.07
      ).draw()

legend = Legend([hdata] + hstacks[:3],
                ['Data', 'Z #rightarrow #mu#mu#gamma',
                 'Z #rightarrow #mu#mu + jets', 't#bar{t}'],
                position = (0.65, 0.55, 0.9, 0.85),
                optlist = ['pl', 'f', 'f', 'f']
                )
legend.draw()

# latexLabel.SetTextFont(gStyle.GetTitleFont())
# latexLabel.DrawLatex(0.17, 0.96, "CMS Preliminary 2011, #sqrt{s} = 7 TeV")
# #latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
# latexLabel.DrawLatex(0.2, 0.575, "Barrel")
# # latexLabel.DrawLatex(0.2, 0.575, "Endcaps")
# latexLabel.DrawLatex(0.2, 0.875, "16Jan Re-reco + Fall11 MC")
# latexLabel.DrawLatex(0.2, 0.8,
#                      "Total events: %d" % \
#                      int( hdata.Integral(1, var.getBins() ) )
#                      )
# # latexLabel.DrawLatex(0.2, 0.725, "L = 332 pb^{-1}")
# latexLabel.DrawLatex(0.2, 0.725, "L = 4.89 fb^{-1}")
# #latexLabel.DrawLatex(0.2, 0.65, "E_{T}^{#gamma} #in [5,10] GeV")
# #latexLabel.DrawLatex(0.2, 0.65, "E_{T}^{#gamma} #in [10,15] GeV")
# # latexLabel.DrawLatex(0.2, 0.65, "E_{T}^{#gamma} #in [15,20] GeV")
# latexLabel.DrawLatex(0.2, 0.65, "E_{T}^{#gamma} > 25 GeV")


# # latexLabel.DrawLatex(0.15, 0.96, "CMS Preliminary 2011")
# # latexLabel.DrawLatex(0.75, 0.96, "#sqrt{s} = 7 TeV")
# # #latexLabel.DrawLatex(0.7, 0.2, "Barrel")
# # #latexLabel.DrawLatex(0.7, 0.2, "Endcaps")
# # latexLabel.DrawLatex(0.2, 0.875, "42X data and MC")
# # latexLabel.DrawLatex(0.2, 0.8, "Total events: %d" % (int( hdata.GetEntries() ),) )
# # latexLabel.DrawLatex(0.2, 0.725, "L = 332 pb^{-1}")
# # latexLabel.DrawLatex(0.2, 0.65, "E_{T}^{#gamma} > 10 GeV")

c1.Update()

## Print yields:
print "--++ Yields and Purities"
for i in range( len(hstacks) ):
    if i < len(hstacks) - 1:
        res = hstacks[i].Integral() - hstacks[i+1].Integral()
    else:
        res = hstacks[i].Integral()
    print "%10s %10.2f %10.4g%%" % ( hstacks[i].GetName().replace('hs_', ''),
                                 res,
                                 100. * res/hdata.Integral(1, var.getBins() ) )

if __name__ == '__main__': import user
