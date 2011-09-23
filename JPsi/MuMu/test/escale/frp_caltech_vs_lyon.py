'''
Facilitates the plotting of variables versus the the fit range iteration.
    Usage: python -i <filename>
'''

import JPsi.MuMu.common.canvases as canvases
from JPsi.MuMu.escale.fitResultPlotter import FitResultPlotter
from JPsi.MuMu.common.binedges import BinEdges
from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *

gStyle.SetPadTopMargin(0.1)
canvases.wwidth = 400
canvases.wheight = 400
canvases.yperiod = 10

plotters = []

## Configuration for plots vs Pt
binedges = list(BinEdges([10, 12, 15, 20, 25, 30, 100]))
bincenters = [0.5*(lo + hi)
              for lo, hi in BinEdges([10, 12, 15, 20, 25, 30, 50])]
binhalfwidths = [0.5*(hi - lo)
                 for lo, hi in BinEdges([10, 12, 15, 20, 25, 30, 50])]
n = len(binedges)
# binhalfwidths = [0] * n



###############################################################################
## EB, R9 < 0.94, mmMass < 80 GeV, mmgMass in [87.2, 95.2]
sreco_lyon_data = (
    ## s, es, sigma, esigma
    (-1.811, 0.170, 13.279, 0.120),
    ( 2.075, 0.130, 12.612, 0.092),
    ( 2.398, 0.101, 10.628, 0.071),
    ( 2.233, 0.104,  8.460, 0.073),
    ( 1.696, 0.116,  7.133, 0.082),
    ( 2.123, 0.111,  6.214, 0.079),
)

sreco_lyon, esreco_lyon, sigma_lyon, esigma_lyon = zip(*sreco_lyon_data)

filenames = ['mc_mmMass80_EB_lowR9_PhoEt_mmgMass87.2-95.2_cbShape.root'] * n
wsnames = ('ws1',) * n
## MC truth scale
sreco_snapshots = ['sFit_sreco_mc_mmMass80_EB_lowR9_cbShape_PhoEt%d-%d_iter0' % (lo, hi)
                   for lo, hi in binedges]

sgen_snapshots = ['sFit_sgen_mc_mmMass80_EB_lowR9_cbShape_PhoEt%d-%d_iter0' % (lo, hi)
                   for lo, hi in binedges]

strue_snapshots = ['sFit_strue_mc_mmMass80_EB_lowR9_cbShape_PhoEt%d-%d' % (lo, hi)
                   for lo, hi in binedges]

def var_vs_pt(name):
    """Returns functions that take a workspaces ws and return
    x, y, ex, ey where y and ey correspond to workspace
    variable of a given name and x and ex are pt bins."""
    return (
        lambda ws, i = iter(bincenters): i.next(),    # x
        lambda ws: ws.var(name).getVal(),             # y
        lambda ws, i = iter(binhalfwidths): i.next(), # ex
        lambda ws: ws.var(name).getError(),           # ey
    )

#------------------------------------------------------------------------------
## Scale Comparison
## Lyon
frp = FitResultPlotter(
    sources = zip(filenames, wsnames, sreco_snapshots),
    getters = (
        lambda ws, i = iter(bincenters): i.next(),    # x
        lambda ws, i = iter(sreco_lyon): i.next(),    # y
        lambda ws, i = iter(binhalfwidths): i.next(), # ex
        lambda ws, i = iter(esreco_lyon): i.next(),   # ey
        ),
    xtitle = 'E_{T}^{#gamma} (GeV)',
    ytitle = 's_{reco} = E^{#gamma}_{reco}/E^{kin}_{reco} - 1 (%)',
    title = 'Lyon',
    )
frp.getdata()
frp.makegraph()

## Caltech
frp.getters = var_vs_pt('#Deltas')
frp.title = 'Caltech'
frp.getdata()
frp.makegraph()

## True
frp.sources = zip(filenames, wsnames, strue_snapshots)
frp.getters = var_vs_pt('#Deltas')
frp.title = 'MC Truth E_{reco}/E_{gen}'
frp.getdata()
frp.makegraph()


## Compare Caltech, Lyon and MC truth scale
canvases.next().SetGrid()
frp.plotall(title = 'Barrel, R_{9} < 0.94, Baseline Selection, POWHEG S4',
            styles = [20, 25, 22],
            colors = [kBlue, kRed, kBlack])

plotters.append(frp)

#------------------------------------------------------------------------------
## S width Comparison
## Lyon
frp = FitResultPlotter(
    sources = zip(filenames, wsnames, sreco_snapshots),
    getters = (
        lambda ws, i = iter(bincenters): i.next(),    # x
        lambda ws, i = iter(sigma_lyon): i.next(),    # y
        lambda ws, i = iter(binhalfwidths): i.next(), # ex
        lambda ws, i = iter(esigma_lyon): i.next(),   # ey
        ),
    xtitle = 'E_{T}^{#gamma} (GeV)',
    ytitle = '#sigma(s_{reco}) (%)',
    title = 'Lyon',
    )
frp.getdata()
frp.makegraph()

## Caltech
frp.getters = var_vs_pt('#sigma')
frp.title = 'Caltech'
frp.getdata()
frp.makegraph()

## Compare Caltech and Lyon scale
canvases.next()
frp.plotall(title = 'Barrel, R_{9} < 0.94, Baseline Selection, POWHEG S4',
            styles = [20, 25])

plotters.append(frp)



###############################################################################
## EB, R9 > 0.94, mmMass < 80 GeV, mmgMass in [87.2, 95.2]
sreco_lyon_data = (
    ## s, es, sigma, esigma
    (-3.604, 0.185, 11.901,  0.131),
    ( 0.778, 0.145, 11.382,  0.102),
    ( 0.154, 0.108,  9.681,  0.076),
    ( 0.160, 0.106,  7.715,  0.075),
    ( 0.060, 0.113,  6.549,  0.081),
    ( 0.147, 0.109,  6.007,  0.078),
)

sreco_lyon, esreco_lyon, sigma_lyon, esigma_lyon = zip(*sreco_lyon_data)

filenames = ['mc_mmMass80_EB_highR9_PhoEt_mmgMass87.2-95.2_cbShape.root'] * n
wsnames = ('ws1',) * n
## MC truth scale
sreco_snapshots = ['sFit_sreco_mc_mmMass80_EB_highR9_cbShape_PhoEt%d-%d_iter0' % (lo, hi)
                   for lo, hi in binedges]
strue_snapshots = ['sFit_strue_mc_mmMass80_EB_highR9_cbShape_PhoEt%d-%d_iter0' % (lo, hi)
                   for lo, hi in binedges]

def var_vs_pt(name):
    """Returns functions that take a workspaces ws and return
    x, y, ex, ey where y and ey correspond to workspace
    variable of a given name and x and ex are pt bins."""
    return (
        lambda ws, i = iter(bincenters): i.next(),    # x
        lambda ws: ws.var(name).getVal(),             # y
        lambda ws, i = iter(binhalfwidths): i.next(), # ex
        lambda ws: ws.var(name).getError(),           # ey
    )

#------------------------------------------------------------------------------
## Scale Comparison
## Lyon
frp = FitResultPlotter(
    sources = zip(filenames, wsnames, sreco_snapshots),
    getters = (
        lambda ws, i = iter(bincenters): i.next(),    # x
        lambda ws, i = iter(sreco_lyon): i.next(),    # y
        lambda ws, i = iter(binhalfwidths): i.next(), # ex
        lambda ws, i = iter(esreco_lyon): i.next(),   # ey
        ),
    xtitle = 'E_{T}^{#gamma} (GeV)',
    ytitle = 's_{reco} = E^{#gamma}_{reco}/E^{kin}_{reco} - 1 (%)',
    title = 'Lyon',
    )
frp.getdata()
frp.makegraph()

## Caltech
frp.getters = var_vs_pt('#Deltas')
frp.title = 'Caltech'
frp.getdata()
frp.makegraph()

## Compare Caltech and Lyon scale
canvases.next()
frp.plotall(title = 'Barrel, R_{9} > 0.94, Baseline Selection, POWHEG S4',
            styles = [20, 25, 22],
            color = [kBlue, kRed, kBlack])

plotters.append(frp)

#------------------------------------------------------------------------------
## S width Comparison
## Lyon
frp = FitResultPlotter(
    sources = zip(filenames, wsnames, sreco_snapshots),
    getters = (
        lambda ws, i = iter(bincenters): i.next(),    # x
        lambda ws, i = iter(sigma_lyon): i.next(),    # y
        lambda ws, i = iter(binhalfwidths): i.next(), # ex
        lambda ws, i = iter(esigma_lyon): i.next(),   # ey
        ),
    xtitle = 'E_{T}^{#gamma} (GeV)',
    ytitle = '#sigma(s_{reco}) (%)',
    title = 'Lyon',
    )
frp.getdata()
frp.makegraph()

## Caltech
frp.getters = var_vs_pt('#sigma')
frp.title = 'Caltech'
frp.getdata()
frp.makegraph()

## Compare Caltech and Lyon scale
canvases.next()
frp.plotall(title = 'Barrel, R_{9} > 0.94, Baseline Selection, POWHEG S4',
            styles = [20, 25])

plotters.append(frp)



###############################################################################
## EE, R9 < 0.95, mmMass < 80 GeV, mmgMass in [87.2, 95.2]
sreco_lyon_data = (
    ## s, es, sigma, esigma
    (-1.907, 0.285, 14.025, 0.201),
    ( 2.201, 0.229, 13.808, 0.162),
    ( 3.425, 0.185, 12.007, 0.130),
    ( 2.698, 0.184,  9.310, 0.130),
    ( 2.092, 0.199,  7.699, 0.141),
    ( 2.310, 0.199,  6.825, 0.141),
)

sreco_lyon, esreco_lyon, sigma_lyon, esigma_lyon = zip(*sreco_lyon_data)

filenames = ['mc_mmMass80_EE_lowR9_PhoEt_mmgMass87.2-95.2_cbShape.root'] * n
wsnames = ('ws1',) * n
## MC truth scale
sreco_snapshots = ['sFit_sreco_mc_mmMass80_EE_lowR9_cbShape_PhoEt%d-%d_iter0' % (lo, hi)
                   for lo, hi in binedges]

def var_vs_pt(name):
    """Returns functions that take a workspaces ws and return
    x, y, ex, ey where y and ey correspond to workspace
    variable of a given name and x and ex are pt bins."""
    return (
        lambda ws, i = iter(bincenters): i.next(),    # x
        lambda ws: ws.var(name).getVal(),             # y
        lambda ws, i = iter(binhalfwidths): i.next(), # ex
        lambda ws: ws.var(name).getError(),           # ey
    )

#------------------------------------------------------------------------------
## Scale Comparison
## Lyon
frp = FitResultPlotter(
    sources = zip(filenames, wsnames, sreco_snapshots),
    getters = (
        lambda ws, i = iter(bincenters): i.next(),    # x
        lambda ws, i = iter(sreco_lyon): i.next(),    # y
        lambda ws, i = iter(binhalfwidths): i.next(), # ex
        lambda ws, i = iter(esreco_lyon): i.next(),   # ey
        ),
    xtitle = 'E_{T}^{#gamma} (GeV)',
    ytitle = 's_{reco} = E^{#gamma}_{reco}/E^{kin}_{reco} - 1 (%)',
    title = 'Lyon',
    )
frp.getdata()
frp.makegraph()

## Caltech
frp.getters = var_vs_pt('#Deltas')
frp.title = 'Caltech'
frp.getdata()
frp.makegraph()

## Compare Caltech and Lyon scale
canvases.next()
frp.plotall(title = 'Endcaps, R_{9} < 0.95, Baseline Selection, POWHEG S4',
            styles = [20, 25])

plotters.append(frp)

#------------------------------------------------------------------------------
## S width Comparison
## Lyon
frp = FitResultPlotter(
    sources = zip(filenames, wsnames, sreco_snapshots),
    getters = (
        lambda ws, i = iter(bincenters): i.next(),    # x
        lambda ws, i = iter(sigma_lyon): i.next(),    # y
        lambda ws, i = iter(binhalfwidths): i.next(), # ex
        lambda ws, i = iter(esigma_lyon): i.next(),   # ey
        ),
    xtitle = 'E_{T}^{#gamma} (GeV)',
    ytitle = '#sigma(s_{reco}) (%)',
    title = 'Lyon',
    )
frp.getdata()
frp.makegraph()

## Caltech
frp.getters = var_vs_pt('#sigma')
frp.title = 'Caltech'
frp.getdata()
frp.makegraph()

## Compare Caltech and Lyon scale
canvases.next().SetGrid()
frp.plotall(title = 'Endcap, R_{9} < 0.95, Baseline Selection, POWHEG S4',
            styles = [20, 25])

plotters.append(frp)


if __name__ == '__main__':
    import user
