'''
Facilitates the plotting of variables versus the the fit range iteration.
    Usage: python -i <filename>
'''

import JPsi.MuMu.common.canvases as canvases
from JPsi.MuMu.escale.fitResultPlotter import FitResultPlotter
from JPsi.MuMu.common.binedges import BinEdges
from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *
from JPsi.MuMu.escale.lyondata import data_2011_09_23_confID155805 as lyon

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

categories = 'EB_lowR9 EB_highR9 EE_lowR9 EE_highR9'.split()
lyonmc = lyon['mc']

class Config():
    """Holds fitResultPlotter configuration data."""
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
## end of Config

cfgs = [
    ###########################################################################
    ## EB, R9 < 0.94, mmMass < 80 GeV, mmgMass in [87.2, 95.2]
    Config(
        ## Used to pick the right Lyon data and in canvas name
        name = 'EB_lowR9',
        ## Used in canvas title
        title = 'Barrel, R_{9} < 0.94, Baseline Selection, POWHEG S4',
        filenames = ['mc_mmMass80_EB_lowR9_PhoEt_mmgMass87.2-95.2_'
                     'cbShape.root'] * n,
        wsnames = ('ws1',) * n,
        sreco_snapshots = ['sFit_sreco_mc_mmMass80_EB_lowR9_cbShape_'
                           'PhoEt%d-%d_iter0' % (lo, hi) for lo, hi in binedges],
        ## MC truth scale
        strue_snapshots = ['sFit_strue_mc_mmMass80_EB_lowR9_cbShape_'
                           'PhoEt%d-%d' % (lo, hi) for lo, hi in binedges],
    ),
    ###########################################################################
    ## EB, R9 > 0.94, mmMass < 80 GeV, mmgMass in [87.2, 95.2]
    Config(
        ## Used to pick the right Lyon data and in canvas name
        name = 'EB_highR9',
        ## Used in canvas title
        title = 'Barrel, R_{9} > 0.94, Baseline Selection, POWHEG S4',
        filenames = ['mc_mmMass80_EB_highR9_PhoEt_mmgMass87.2-95.2_'
                     'cbShape.root'] * n,
        wsnames = ('ws1',) * n,
        sreco_snapshots = ['sFit_sreco_mc_mmMass80_EB_highR9_cbShape_'
                           'PhoEt%d-%d_iter0' % (lo, hi) for lo, hi in binedges],
        ## MC truth scale
        strue_snapshots = ['sFit_strue_mc_mmMass80_EB_highR9_cbShape_'
                           'PhoEt%d-%d' % (lo, hi) for lo, hi in binedges],
    ),
    ###########################################################################
    ## EE, R9 < 0.95, mmMass < 80 GeV, mmgMass in [87.2, 95.2]
    Config(
        ## Used to pick the right Lyon data and in canvas name
        name = 'EE_lowR9',
        ## Used in canvas title
        title = 'Endcaps, R_{9} < 0.95, Baseline Selection, POWHEG S4',
        filenames = ['mc_mmMass80_EE_lowR9_PhoEt_mmgMass87.2-95.2_'
                     'cbShape.root'] * n,
        wsnames = ('ws1',) * n,
        sreco_snapshots = ['sFit_sreco_mc_mmMass80_EE_lowR9_cbShape_'
                           'PhoEt%d-%d_iter0' % (lo, hi) for lo, hi in binedges],
        ## MC truth scale
        strue_snapshots = ['sFit_strue_mc_mmMass80_EE_lowR9_cbShape_'
                           'PhoEt%d-%d' % (lo, hi) for lo, hi in binedges],
    ),
    ###########################################################################
    ## EE, R9 > 0.95, mmMass < 80 GeV, mmgMass in [87.2, 95.2]
    Config(
        ## Used to pick the right Lyon data and in canvas name
        name = 'EE_highR9',
        ## Used in canvas title
        title = 'Endcaps, R_{9} > 0.95, Baseline Selection, POWHEG S4',
        filenames = ['mc_mmMass80_EE_highR9_PhoEt_mmgMass87.2-95.2_'
                     'cbShape.root'] * n,
        wsnames = ('ws1',) * n,
        sreco_snapshots = ['sFit_sreco_mc_mmMass80_EE_highR9_cbShape_'
                           'PhoEt%d-%d_iter0' % (lo, hi) for lo, hi in binedges],
        ## MC truth scale
        strue_snapshots = ['sFit_strue_mc_mmMass80_EE_highR9_cbShape_'
                           'PhoEt%d-%d' % (lo, hi) for lo, hi in binedges],
    ),
]

for cfg in cfgs:
    #------------------------------------------------------------------------------
    ## Scale Comparison
    ## Lyon
    frp = FitResultPlotter(
        sources = zip(cfg.filenames, cfg.wsnames, cfg.sreco_snapshots),
        getters = (
            lambda ws, i = iter(bincenters): i.next(),    # x
            lambda ws, i = iter(lyonmc[cfg.name]['sreco']): i.next(), # y
            lambda ws, i = iter(binhalfwidths): i.next(), # ex
            lambda ws, i = iter(lyonmc[cfg.name]['esreco']): i.next(), # ey
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
    frp.sources = zip(cfg.filenames, cfg.wsnames, cfg.strue_snapshots)
    frp.getters = var_vs_pt('#Deltas')
    frp.title = 'MC Truth'
    frp.getdata()
    frp.makegraph()

    ## Compare Caltech, Lyon and MC truth scale
    canvases.next('s_' + cfg.name).SetGrid()
    frp.plotall(title = cfg.title,
                styles = [20, 25, 22],
                colors = [kBlue, kRed, kBlack])

    plotters.append(frp)

    #------------------------------------------------------------------------------
    ## S width Comparison
    ## Lyon
    frp = FitResultPlotter(
        sources = zip(cfg.filenames, cfg.wsnames, cfg.sreco_snapshots),
        getters = (
            lambda ws, i = iter(bincenters): i.next(),    # x
            lambda ws, i = iter(lyonmc[cfg.name]['sigma']): i.next(),    # y
            lambda ws, i = iter(binhalfwidths): i.next(), # ex
            lambda ws, i = iter(lyonmc[cfg.name]['esigma']): i.next(),   # ey
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

    ## Compare Caltech and Lyon s width
    canvases.next('sigma_' + cfg.name).SetGrid()
    frp.plotall(title = cfg.title,
                styles = [20, 25])

    plotters.append(frp)
## end of loop over cfgs

if __name__ == '__main__':
    import user
