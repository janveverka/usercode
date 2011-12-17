'''
Given a selection and photon scale and resolution,
fetch a RooDataSet of mmgMass MC data smeared such that the photon detector
responce Ereco/Etrue has the same shape as the nominal MC but has the given
scale and resolution.
'''
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.energyScaleChains import getChains
from JPsi.MuMu.common.latex import Latex
from JPsi.MuMu.common.parametrizedkeyspdf import ParametrizedKeysPdf

## Target photon energy scale and resolution of the smeared data.
targets = 0
targetr = 5

##------------------------------------------------------------------------------
## Here starts the meat.

## Selection
cuts = ['phoIsEB',
        'phoR9 > 0.94',
        '20 < phoPt & phoPt < 25',
        'mmMass + mmgMass < 190',
        'isFSR',
        'phoGenE > 0',
        ]
cutlabels = [
    'reco E_{T}^{#gamma} #in [20, 25] GeV',
    'm_{#mu#mu} + m_{#mu#mu#gamma} < 190 GeV',
    'Barrel',
    'R_{9} > 0.94',
    'FSR'
    ]

## Create the default workspace
w = ROOT.RooWorkspace('w')

## Define data variables 
mmgMass = w.factory('mmgMass[40, 140]')
mmMass = w.factory('mmMass[10, 140]')
phoERes = w.factory('phoERes[-70, 100]')
weight = w.factory('weight[1]')

## The TFormula expression defining the data is given in the titles.
weight.SetTitle('pileup.weight')
phoERes.SetTitle('100 * phoERes')

## Create a preselected tree
zchain = getChains('v11')['z']
tree = zchain.CopyTree('&'.join(cuts))
## Have to copy aliases by hand
for a in zchain.GetListOfAliases():
    tree.SetAlias(a.GetName(), a.GetTitle())

## Get the nominal dataset
data = dataset.get(tree=tree, weight=weight, cuts=cuts,
                   variables=[mmgMass, mmMass, phoERes,])

## Give the titles the original meaning
phoERes.SetTitle('E_{reco}^{#gamma}/E_{gen}^{#gamma} - 1')
phoERes.setUnit('%')

##------------------------------------------------------------------------------
## Build model
phoScale = w.factory('phoScale[0,-50,50]')
phoRes = w.factory('phoRes[5,0.01,50]')

for x in [phoScale, phoRes]:
    x.setUnit('%')

range_save = (phoERes.getMin(), phoERes.getMax())
## Enlarge the range of the observable to get vanishing tails.
phoERes.setRange(-90, 150)
phoEResPdf = ParametrizedKeysPdf('phoEResPdf', 'phoEResPdf',
                                 phoERes, phoScale, phoRes, data,
                                 ROOT.RooKeysPdf.NoMirror, 1.5)
phoERes.setRange(*range_save)

##------------------------------------------------------------------------------
## Extract the MC truth scale and resolution from MC
phoEResPdf.fitTo(data, roo.PrintLevel(-1), roo.SumW2Error(False))
phoScaleRef = phoScale.getVal()
phoResRef = phoRes.getVal()

##------------------------------------------------------------------------------
## Define the smearing formulas for photon energy and mmg invariant mass
phoEResSmear = w.factory('phoEResSmear[-100,200]')
phoEResSmearFunc = w.factory('''expr::phoEResSmearFunc(
    "{m} + {s} * ({x} - {m0}) / {s0}",
    {{{x}, {m}, {s}, {m0}, {s0}}}
    )'''.format(x='phoERes', m=targets, s=targetr, m0=phoScaleRef,
                s0=phoResRef)
    )

## Renaming identity phoEResSmear -> phoERes
phoEResFunc = w.factory('expr::phoEResFunc("phoEResSmear", {phoEResSmear})')

## mmgMassSmear = w.factory('mmgMassPhoSmearE[40, 140]')
## phoEResSmear = w.factory('phoEResSmear[-80, 110]')

##------------------------------------------------------------------------------
## Get the smeared data
phoEResSmearFunc.SetName('phoEResSmear')
data.addColumn(phoEResSmearFunc)
phoEResSmearFunc.SetName('phoEResSmearFunc')
datasmeared = data.reduce(ROOT.RooArgSet(phoEResSmear))

phoEResFunc.SetName('phoERes')
datasmeared.addColumn(phoEResFunc)
phoEResFunc.SetName('phoEResFunc')

##------------------------------------------------------------------------------
## Plot the nominal MC data overlayed with the pdf shape and fit
def plot_training_phoeres_with_shape_and_fit():
    canvases.next('TrainingSampleWithShapeAndFit')
    phoERes.setUnit("%")
    plot = phoERes.frame(roo.Range(-7.5, 7.5))
    plot.SetTitle("MC overlayed with PDF shape (blue) and it's parametrized fit"
                  "(dashed red)")
    data.plotOn(plot)
    phoEResPdf.shape.plotOn(plot)
    phoEResPdf.plotOn(plot, roo.LineColor(ROOT.kRed), roo.LineStyle(ROOT.kDashed))
    plot.Draw()
    Latex([
        's_{shape}: %.3f %%' % phoEResPdf.shapemode,
        's_{fit}: %.3f #pm %.3f %%' % (phoScale.getVal(), phoScale.getError()),
        's_{fit} - s_{shape}: %.4f #pm %.4f' % (
            phoScale.getVal() - phoEResPdf.shapemode,
            phoScale.getError()
            ),
        'r_{shape}: %.3f %%' % phoEResPdf.shapewidth,
        'r_{fit}: %.3f #pm %.3f %%' % (phoRes.getVal(), phoRes.getError()),
        'r_{fit}/r_{shape}: %.4f #pm %.4f' % (
            phoRes.getVal() / phoEResPdf.shapewidth,
            phoRes.getError() / phoEResPdf.shapewidth),
        ], position=(0.2, 0.75)).draw()
## end of plot_training_phoeres_with_shape_and_fit
    
##------------------------------------------------------------------------------
## Plot the smeared data
def plot_smeared_phoeres_with_fit():
    phoEResPdf.fitTo(datasmeared, roo.PrintLevel(-1), roo.SumW2Error(False))
    canvases.next('SmearedSampleWithFit')
    plot = phoERes.frame(roo.Range(-30, 30))
    plot.SetTitle("Smeared MC with paremetrized fit")
    datasmeared.plotOn(plot)
    phoEResPdf.plotOn(plot)
    phoEResPdf.paramOn(plot)
    plot.Draw()
    Latex([
        'target s: %.3g %%' % targets,
        'target r: %.3g %%' % targetr,
        ], position=(0.2, 0.75)).draw()
## end of plot_smeared_phoeres_with_fit

##------------------------------------------------------------------------------
def main():
    plot_training_phoeres_with_shape_and_fit()
    plot_smeared_phoeres_with_fit()
    canvases.update()
## end of main

##------------------------------------------------------------------------------
## Footer stuff
canvases.update()
if __name__ == "__main__":
    main()
    import user

