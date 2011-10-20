import copy
import ROOT

import JPsi.MuMu.common.r9Chains as r9Chains
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.common.cmsstyle as cmsstyle

from JPsi.MuMu.common.plotter import Plotter

canvases.wwidth = 700

chains = r9Chains.getChains('v1')
plots = []

ROOT.gStyle.SetTitleOffset(1.25, "Y")
# ROOT.gStyle.SetPadRightMargin(0.02)
# ROOT.gStyle.SetPadLeftMargin(0.15)
# ROOT.gStyle.SetPadTopMargin(0.02)

### Configuration
plot = Plotter(
    cuts = [
        '!isEBEtaGap',
        '!isEBPhiGap',
        '!isEBEEGap',
        ## Module +4
#         '1.16 < scEta & scEta < 1.44',
        ## Barrel
        'isEB',
    ],
    expression = 'r9',
    binning = '20,0.9,1',
    name = 'r9_EB',
    title = '',
    xtitle = 'photon R_{9}',
    ytitle = 'a.u.',
    labels = [
        'flat-p_{T} #gamma gun',
        'E_{T}^{#gamma} #in [10,100] GeV',
        '#eta/#phi/subdet-cracks removed',
        'barrel',
    ],
    trees = [chains[n] for n in 'g93p01 g94cms g94p02'.split()],
    colors = [ROOT.kRed, ROOT.kBlack, ROOT.kBlue,],
    ltitles = ['Spring11 MC', 'Summer11 MC', 'Winter11 MC'],
    drawopts = 'e0 e0hist e0'.split(),
    markerstyles = [20, 21, 22],
    normalize_to_unit_area = True,
    legendkwargs = dict(position = (0.675, 0.9, 0.95, 0.7)),
)

plots.append(plot)

#### Meat
c1 = canvases.next(plot.name)
plot.draw()
c1.SetGrid()
c1.RedrawAxis()
c1.Update()


## Plot Endcaps
plot = plot.clone(name = 'r9_EE')
plots.append(plot)
plot.cuts.remove('isEB')
plot.cuts.append('!isEB')
plot.labels.remove('barrel')
plot.labels.append('endcaps')
c1 = canvases.next(plot.name)
plot.draw()
c1.SetGrid()
c1.RedrawAxis()
c1.Update()


###############################################################################
## brem plots
brem_plots = copy.deepcopy(plots)
for p in brem_plots:
    p.expression = 'scPhiWidth/scEtaWidth'
    p.xtitle = '#sigma_{#phi}^{SC} / #sigma_{#eta}^{SC}'
    p.name = p.name.replace('r9', 'brem')
    p.binning = '30,0,15'
    p.cuts.append('r9 < 0.94')
    c1 = canvases.next(p.name)
    p.draw()
    c1.SetGrid()
    c1.RedrawAxis()
    c1.Update()

if __name__ == '__main__':
    import user
