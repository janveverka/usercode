'''
Facilitates the plotting of variables versus the the fit range iteration.
    Usage: python -i plotScaleVsFitRangeIter.py
'''
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.escale.fitResultPlotter as frp
from JPsi.MuMu.common.binedges import BinEdges

canvases.wwidth = 400
canvases.wheight = 400
canvases.yperiod = 10

## Configuration for plots vs Pt
binedges = list(BinEdges([12, 15, 20, 25, 30, 100]))
bincenters = [0.5*(lo + hi) for lo, hi in binedges]
binhalfwidths = [0.5*(hi - lo) for lo, hi in binedges]
n = len(binedges)

frp.filenames = ['mc_mmMass85_EB_lowR9_PhoEt_cbShape.root'] * n
frp.wsnames = ('ws1',) * n

frp.xtitle = 'E_{T}^{#gamma} (GeV)'
frp.xdata = [0.5*(lo + hi) for lo, hi in binedges]
frp.exdata = [0.5*(hi - lo) for lo, hi in binedges]

## MC truth scale
frp.snapshots = ['sFit_strue_mc_mmMass85_EB_lowR9_cbShape_PhoEt%d-%d' % (lo, hi)
                 for lo, hi in binedges]
frp.yname = '#Deltas'
frp.ytitle = 's_{true} = E^{#gamma}_{reco}/E^{#gamma}_{gen} - 1 (%)'

sources = zip(frp.filenames, frp.wsnames, frp.snapshots)
data = frp.getData(
    sources, (
        lambda ws: ws.var('#Deltas').getVal(),
        lambda ws: ws.var('#Deltas').getError(),
        lambda ws, i = iter(bincenters): i.next(),
        lambda ws, i = iter(binhalfwidths): i.next(),
    )
)

y, ey, x, ex = zip(*data)
from array import array
y, ey, x, ex = [array('d', l) for l in (y, ey, x, ex)]
# canvases.next()
# frp.main()
# frp.dump(frp.graph)

## MC truth resolution
# canvases.next()
# frp.yname = '#sigma'
# frp.ytitle = '#sigma(E^{#gamma}_{reco}/E^{#gamma}_{gen})'
# frp.main()

## Scale from mmg
# frp.snapshots = ['sFit_sreco_mc_mmMass85_EB_lowR9_PhoEt%d-%d_cbShape' % (lo, hi)
#                  for lo, hi in binedges]
# frp.ytitle = 's_{reco} = E^{#gamma}_{reco}/E^{kin}_{reco} - 1 (%)'
# canvases.next()
# frp.main()
# frp.dump(frp.graph)
#
# ## Scale from mmg photon-only gen-level
# frp.snapshots = ['sFit_shyb_mc_mmMass85_EB_lowR9_PhoEt%d-%d_cbShape' % (lo, hi)
#                  for lo, hi in binedges]
# frp.ytitle = 's_{gen} = E^{#gamma}_{gen}/E^{kin}_{reco} - 1 (%)'
# canvases.next()
# frp.main()
# frp.dump(frp.graph)
#
# ## Scale from mmg gen-level
# frp.snapshots = ['sFit_sgen_mc_mmMass85_EB_lowR9_PhoEt%d-%d_cbShape' % (lo, hi)
#                  for lo, hi in binedges]
# frp.ytitle = 's_{gen} = E^{#gamma}_{gen}/E^{kin}_{gen} - 1 (%)'
# canvases.next()
# frp.main()
# frp.dump(frp.graph)

if __name__ == '__main__':
    import user
