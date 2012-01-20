'''
Phton Energy Scale and Photon Energy Resolution (PHOESPHOER) Fit model 1.
Strategy to build a 2D model for the mmMass and mmgMass as functions
of PhoES and PhoER.

Key formula:
mmgMass^2 = mmMass^2 + (mmgMassPhoEGen^2 - mmMass^2) * phoE/phoEGen (1)

Assumption:
phoE/phoEGen is uncorrelated with both mmMass and mmgMass

Strategy:
1. Build a 2D KEYS PDF of X = mmMass and
   T1 = log(mmgMassPhoEGen^2 - mmMass^2) fXT1(x, t1).

2. Build a 1D KEYS PDF of T2 = log(phoE/phoEGen) depending on
   s = phoScale and r = phoRes fT2(t2|s,r). Note that
   phoERes = 100 * (phoE/phoEGen - 1).
   Thus a substitution
   phoERes = 100 * (1 + exp(t2))
   in the phoEResPdf(phoERes|s,r) can be used.

3. Use FFT to convolve fXT1 and fT2 in T1 and T2 to get a 2D PDF
   of X and T = T1 + T2 fXT(x,t|s,r):
   fXT(x,t|s,r) = fXT1(x,t) * fT2(t|s,r)
   Note that X is an additional observable while s and t are parameters.
   It is important to cache the convolution in t *and* x for efficient
   likelihood calculation.

4. Substitute for T using the key formula T -> T3 = log(mmgMass^2 - mmMass^2)
   to obtain a density in X and Y = mmgMass fXY(x,y|s,r).
   fXY(x,y|s,r) = fXT(x,t3(x,y)|s,r).

Culprit:
T3 is only well defined for y > x.  Need to make the range of x depend on y.
Is this possible in RooFit?

Jan Veverka, Caltech, 18 January 2012.
'''
   
##- Boilerplate imports --------------------------------------------------------
import math
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.canvases as canvases

from JPsi.MuMu.common.cmsstyle import cmsstyle
from JPsi.MuMu.common.energyScaleChains import getChains
from JPsi.MuMu.common.latex import Latex
from JPsi.MuMu.common.parametrizedkeyspdf import ParametrizedKeysPdf
from JPsi.MuMu.escale.logphoereskeyspdf import LogPhoeresKeysPdf
from JPsi.MuMu.escale.montecarlocalibrator import MonteCarloCalibrator

##-- Configuration -------------------------------------------------------------
## Selection
name = 'EB_highR9_pt20-25'
cuts = ['mmMass + mmgMass < 190',
        'isFSR',
        'phoGenE > 0',
        #'60 < mmMass & mmMass < 70', 
        ]

##------------------------------------------------------------------------------
def parse_name_to_cuts():
    'Parse the name and apply the relevant cuts.'
    if 'EB' in name:
        cuts.append('phoIsEB')
        if 'highR9' in name:
            cuts.append('phoR9 > 0.94')
        elif 'lowR9' in name:
            cuts.append('phoR9 < 0.94')
    elif 'EE' in name:
        cuts.append('!phoIsEB')
        if 'highR9' in name:
            cuts.append('phoR9 > 0.95')
        elif 'lowR9' in name:
            cuts.append('phoR9 < 0.95')

    if 'pt' in name:
        ## Split the name into tokens.
        for tok in name.split('_'):
            ## Get the token with the pt
            if 'pt' in tok:
                lo, hi = tok.replace('pt', '').split('-')
                cuts.append('%s <= phoPt & phoPt < %s' % (lo, hi))
## End of parse_name_to_cuts().

##------------------------------------------------------------------------------
def init():
    'Initialize workspace and common variables and functions.'
    parse_name_to_cuts()
    ## Create the default workspace
    global w
    w = ROOT.RooWorkspace('w')

    ## Define data observables. 
    global mmgMass, mmMass, phoERes, mmgMassPhoGenE, weight
    mmgMass = w.factory('mmgMass[40, 140]')
    mmgMassPhoGenE = w.factory('mmgMassPhoGenE[0, 200]')
    mmMass = w.factory('mmMass[10, 140]')
    phoERes = w.factory('phoERes[-70, 100]')
    weight = w.factory('weight[1]')

    ## Define model parameters.
    global phoScale, phoRes, t
    phoScale = w.factory('phoScale[0,-50,50]')
    phoRes = w.factory('phoRes[1.5,0.01,50]')
    t = w.factory('t[7,1,20]')

    ## Set units.
    for x, u in zip([phoScale, phoRes],
                    '% %'.split()):
        x.setUnit(u)

    ## Prep for storing fit results in the workspace.
    global phoScaleTarget, phoResTarget, params
    phoScaleTarget = w.factory('phoScaleTarget[0,-50,50]')
    phoResTarget = w.factory('phoResTarget[5,0.01,50]')
    params = ROOT.RooArgSet(phoScaleTarget, phoResTarget)
    w.defineSet('params', params)
## End of init().


##------------------------------------------------------------------------------
def get_data(zchain = getChains('v11')['z']):
    'Get the nominal data that is used for smearing.'
    ## The TFormula expression defining the data is given in the titles.
    weight.SetTitle('pileup.weight')
    phoERes.SetTitle('100 * phoERes')
    mmgMassPhoGenE.SetTitle('threeBodyMass(mu1Pt, mu1Eta, mu1Phi, 0.106, '
                            '              mu2Pt, mu2Eta, mu2Phi, 0.106, '
                            '              phoGenE * phoPt / phoE, '
                            '                     phoEta, phoPhi, 0)')
    ## Create a preselected tree
    tree = zchain.CopyTree('&'.join(cuts))
    ## Have to copy aliases by hand
    for a in zchain.GetListOfAliases():
        tree.SetAlias(a.GetName(), a.GetTitle())

    ## Get the nominal dataset
    global data
    data = dataset.get(tree=tree, weight=weight, cuts=cuts,
                       variables=[mmgMass, mmMass, phoERes, mmgMassPhoGenE])

    ## Set units and nice titles
    for x, t, u in zip([mmgMass, mmgMassPhoGenE, mmMass, phoERes],
                       ['m_{#mu#mu#gamma}',
                        'm_{#mu#mu#gamma} with E_{gen}^{#gamma}',
                        'm_{#mu^{+}#mu^{-}}',
                        'E_{reco}^{#gamma}/E_{gen}^{#gamma} - 1', ],
                       'GeV GeV GeV %'.split()):
        x.SetTitle(t)
        x.setUnit(u)
    ##-- Get Smeared Data ------------------------------------------------------
    ## Enlarge the range of the observable to get vanishing tails.
    range_save = (phoERes.getMin(), phoERes.getMax())
    phoERes.setRange(-90, 150)
    global calibrator
    calibrator = MonteCarloCalibrator(data)
    phoERes.setRange(*range_save)
## End of get_data.

##------------------------------------------------------------------------------
def get_derived_data():
    ## Get x, t1 data
    global data
    global xt1data
    t1func = w.factory(
        '''expr::t1func("log(mmgMassPhoGenE^2 - mmMass^2)",
                        {mmgMassPhoGenE, mmMass})'''
        )
    t1func.SetName('t')
    data.addColumn(t1func)
    xt1data = data.reduce(ROOT.RooArgSet(mmMass, t))
    t1func.SetName('t1func')
    data = data.reduce(ROOT.RooArgSet(mmgMass, mmMass, phoERes, mmgMassPhoGenE))
    xmin = ROOT.Double(0)
    xmax = ROOT.Double(0)
    xt1data.getRange(mmMass, xmin, xmax, 0.05)
    global mmMass_range
    mmMass_range = (float(xmin), float(xmax))
    xt1data.getRange(t, xmin, xmax, 0.05)
    global t1range
    t1range = (float(xmin), float(xmax))

    ## Get t2 data
    global t2data
    t.setRange(-2, 2)
    t2func = w.factory(
        'expr::t2func("log(0.01 * phoERes + 1)", {phoERes})'
        )
    t2func.SetName('t')
    data.addColumn(t2func)
    t2func.SetName('t2func')
    t2data = data.reduce(ROOT.RooArgSet(t))
    data = data.reduce(ROOT.RooArgSet(mmgMass, mmMass, phoERes, mmgMassPhoGenE))
    t2data.getRange(t, xmin, xmax, 0.05)
    global t2range
    t2range = (float(xmin), float(xmax))

    ## Get x, t data
    global xtdata
    t.setRange(*t1range)
    tfunc = w.factory('''expr::tfunc("log(mmgMass^2 - mmMass^2)",
                                     {mmgMass, mmMass})''')
    tfunc.SetName('t')
    data.addColumn(tfunc)
    tfunc.SetName('tfunc')
    xtdata = data.reduce(ROOT.RooArgSet(mmMass, t))
    data = data.reduce(ROOT.RooArgSet(mmgMass, mmMass, phoERes, mmgMassPhoGenE))
## End of get_derived_data().

##------------------------------------------------------------------------------
def plot_xt1_proj_x():
    ## Plot fXT1(x, t1) projected on x axis
    canvases.next('xt1_proj_x')
    plot = mmMass.frame()
    xt1data.plotOn(plot)
    xt1pdf.plotOn(plot)
    plot.Draw()
## End of plot_xt1_proj_x().

##------------------------------------------------------------------------------
def plot_xt1_proj_t1():
    ## Plot fXT1(x, t1) projected on t1 axis
    canvases.next('xt1_proj_t1')
    t.setRange(*t1range)
    t.SetTitle('log(m_{#mu#mu#gamma,E_{gen}^{#gamma}}^{2} - m_{#mu#mu}^{2})')
    plot = t.frame()
    xt1data.plotOn(plot)
    xt1pdf.plotOn(plot)
    plot.Draw()
## End of plot_xt1_proj_t1().

##------------------------------------------------------------------------------
def plot_xt1():
    ## Plot fXT1(x, t1) with training data.
    c1 = canvases.next('xt1')
    c1.SetWindowSize(800, 400)
    c1.Divide(2,1)
    c1.cd(1).SetGrid()
    t.setRange(*t1range)
    t.SetTitle('log(m_{#mu#mu#gamma,E_{gen}^{#gamma}}^{2} - m_{#mu#mu}^{2})')
    hxt1d = xt1data.createHistogram(mmMass, t, 100, 100, '', 'hxt1')
    hxt1d.SetTitle('Data')
    hxt1d.GetXaxis().SetTitle(mmMass.GetTitle() + ' (GeV)')
    hxt1d.GetYaxis().SetTitle(t.GetTitle())
    hxt1d.GetXaxis().SetTitleOffset(1.3)
    hxt1d.GetXaxis().SetRangeUser(*mmMass_range)
    hxt1d.GetYaxis().SetRangeUser(*t1range)
    hxt1d.Draw('cont0')

    c1.cd(2).SetGrid()
    hxt1f = xt1pdf.createHistogram('hxt1f', mmMass, roo.YVar(t))
    hxt1f.SetTitle('PDF')
    hxt1f.GetXaxis().SetTitleOffset(1.3)
    hxt1f.Draw("cont0")
## End of plot_xt1().

##------------------------------------------------------------------------------
def plot_t2():
    ## Plot fT2(t2|s,r) fitted to training data.
    canvases.next('t2pdf').SetGrid()
    t.setRange(*t2range)
    t.setVal(0)
    t.SetTitle('log(E_{reco}^{#gamma}/E_{gen}^{#gamma})')
    phoScale.setVal(t2pdf.s0val)
    phoRes.setVal(t2pdf.r0val)
    t2pdf.fitTo(t2data, roo.Range(ROOT.TMath.Log(0.5), ROOT.TMath.Log(1.5)),
                roo.NumCPU(8), roo.SumW2Error(True))
    plot = t.frame(roo.Range(-0.3, 0.3))
    t2data.plotOn(plot)
    t2pdf.plotOn(plot)
    plot.Draw()
    Latex([
        's_{shape}: %.3f %%' % t2pdf.s0val,
        's_{fit}: %.3f #pm %.3f %%' % (phoScale.getVal(), phoScale.getError()),
        's_{fit} - s_{shape}: %.4f #pm %.4f %%' % (
            phoScale.getVal() - t2pdf.s0val,
            phoScale.getError()
            ),
        'r_{shape}: %.3f %%' % t2pdf.r0val,
        'r_{fit}: %.3f #pm %.3f %%' % (phoRes.getVal(), phoRes.getError()),
        'r_{fit}/r_{shape}: %.4f #pm %.4f' % (
            phoRes.getVal() / t2pdf.r0val,
            phoRes.getError() / t2pdf.r0val),
        ], position=(0.2, 0.75)).draw()
## End of plot_t2()

##------------------------------------------------------------------------------
def check_timer(label = ''):
    sw.Stop()
    print label, 'CPU time:', sw.CpuTime(), 's, real time:', sw.RealTime(), 's'
    sw.Reset()
    sw.Start()

##------------------------------------------------------------------------------
def build_models():
    ## Build the model fXT1(x, t1) for mmMass vs
    ## log(mmgMassPhoGenE^2 - mmMass^2)
    global xt1pdf
    t.setRange(*t1range)
    xt1pdf = ROOT.RooNDKeysPdf('xt1pdf', 'xt1pdf', ROOT.RooArgList(mmMass, t),
                               xt1data, "a", 1.5)
    xt1pdf.setNormValueCaching(2)
    ## Trigger filling the normalization cache.
    xt1pdf.getVal(ROOT.RooArgSet(mmMass, t))

    ## Build the model fT2(t2|s,r) for log(Ereco/Egen) ft2(t2|r,s)
    global t2pdf
    t.setRange(*t2range)
    t.setVal(0)
    t2pdf = LogPhoeresKeysPdf('t2pdf', 't2pdf', phoERes, t, phoScale,
                              phoRes, data, rho=1.5)

    ## Build the model for fXY(x,y|s,r) = fXT1(t) * fT2(t|s,r), t = t(x,y)
    global eptbound, tcfunc, xypdf
    trange = (4, 10)
    buffrac = 0.2
    exptbound = w.factory(
        '''expr::exptbound(
            "({M}*{M} - {m}*{m} <= {exptmin}) * {exptmin} +
             ({exptmin} < {M}*{M} - {m}*{m}) * ({M}*{M} - {m}*{m})",
             {{{M}, {m}}})'''.format(
            ## exptmin = math.exp(t1range[0] + t2range[0]),
            exptmin = math.exp(trange[0] - buffrac * (trange[1] - trange[0])),
            m='mmMass', M='mmgMass'
            )
        )
    tcfunc = w.factory('''expr::tcfunc("log(exptbound)", {exptbound})''')
    t.setRange(*trange)
    mmMass.setRange(*mmMass_range)
    t.setBins(100, "cache")
    mmMass.setBins(10, "cache")
    xypdf = ROOT.RooFFTConvPdf('xypdf', 'xypdf', tcfunc, t, xt1pdf, t2pdf)
    xypdf.setBufferFraction(0.2)
    xypdf.setCacheObservables(ROOT.RooArgSet(mmMass, t))
    xypdf.setNormValueCaching(2)
## End of build_models().
    
##------------------------------------------------------------------------------
sw = ROOT.TStopwatch()
sw.Start()

## (a) xt1pdf norm val chaching
## (b) cache=1000*40, rho=3, 296s
## (c) cache=100*10, rho=1.5, 2.2s
## (d) cache=100*100, rho=1.5, 2.3s

## 1. real time (s): 0.0 s
init()
check_timer(1)

## 2. real time (s): 5.2 s
get_data()
check_timer(2)

## 3. real time (s): 0.1 s
get_derived_data()
check_timer(3)

## 4. real time (s): 20.4, 21.2 (a), 34.3 (b)
build_models()
check_timer(4)

## ## 5. real time (s): 44.6, 44.2 (a)
## plot_xt1_proj_x()
## check_timer(5)

## ## 6. real time (s): 32.6, 32.6 (a)
## plot_xt1_proj_t1()
## check_timer(6)

## ## 7. real time (s): 6.1, 6.0(a)
## plot_xt1()
## check_timer(7)

## 8. real time (s): 0.4
plot_t2()
check_timer(8)

canvases.update()

t.setRange(*t1range)
t.setVal(0.5 * (t1range[0] + t1range[1]))

## Plot fXY(x,y|s,r) projected on mmgMass
c1 = canvases.next('xy_proj_y')
plot = mmgMass.frame(roo.Range(75, 105))
data.plotOn(plot)
xypdf.plotOn(plot)
plot.Draw()

## Plot fXY(x,y|s,r) projected on mmMass
c1 = canvases.next('xy_proj_x')
plot = mmMass.frame(roo.Range(40, 90))
data.plotOn(plot)
xypdf.plotOn(plot)
plot.Draw()

## Plot fXY(x,y|s,r) 2D plot with data
c1 = canvases.next('xy')
c1.SetWindowSize(800, 400)
c1.Divide(2,1)
c1.cd(1).SetGrid()
hd = data.createHistogram(mmMass, mmgMass, 50, 50, '', 'hxyd')
hd.SetTitle('Data')
hd.GetXaxis().SetTitle(mmMass.GetTitle() + ' (GeV)')
hd.GetYaxis().SetTitle(mmgMass.GetTitle() + ' (GeV)')
# hd.GetXaxis().SetTitleOffset(1.3)
hd.GetXaxis().SetRangeUser(40, 80)
hd.GetYaxis().SetRangeUser(75, 105)
hd.Draw('cont0')

c1.cd(2).SetGrid()
hf = xypdf.createHistogram('hxyf', mmMass, roo.Binning(100, 40, 80),
                           roo.YVar(mmgMass, roo.Binning(100, 75, 105)))
hf.SetTitle('PDF')
# hf.GetXaxis().SetTitleOffset(1.3)
hf.Draw("cont0")

## Plot fXY(x,y|s,r) slice at mmMass = [55, 60, 65, 70, 75] GeV
c1 = canvases.next('xy_slice_y')
plot = mmgMass.frame()
for mval, color in zip(
    [45, 50, 55, 60, 65, 70, 75, 80],
    'Red Yellow Orange Spring Green Magenta Blue Black'.split()
    ):
    mmMass.setVal(mval)
    xypdf.plotOn(plot, roo.LineColor(getattr(ROOT, 'k' + color)))

plot.Draw()

## Plot fXY(x,y|s,r) slice at mmgMass values
c1 = canvases.next('xy_slice_x')
plot = mmMass.frame()
for mval, color in zip(
    [70, 75, 80, 85, 90, 95, 100, 105],
    'Red Yellow Orange Spring Green Magenta Blue Black'.split()
    ):
    mmgMass.setVal(mval)
    xypdf.plotOn(plot, roo.LineColor(getattr(ROOT, 'k' + color)))

plot.Draw()

canvases.update()

## Plot fXT(t|s,r) fitted to data
data_small = data.reduce(roo.EventRange(0, data.numEntries()/10))
## xypdf.fitTo(data_small, roo.NumCPU(8), roo.Verbose(True), roo.Timer(True),
##             roo.SumW2Error(True),
##             #roo.Minos(ROOT.RooArgSet(phoRes))
##             )

## canvases.next('tpdf').SetGrid()
## t.setRange(5, 10)
## t.SetTitle('log(m_{#mu#mu#gamma}^{2} - m_{#mu#mu}^{2})')
## xypdf.fitTo(tdata, roo.Range(5.5, 9.5))
## plot = t.frame(roo.Range(6, 9))
## tdata.plotOn(plot)
## tpdf.plotOn(plot)
## tpdf.paramOn(plot)
## plot.Draw()

## real time (s): 267.3, 296.5(b), 2.2(c)

canvases.update()
sw.Stop()
print 'CPU time:', sw.CpuTime(), 's, real time:', sw.RealTime(), 's'
 

if __name__ == '__main__':
    # main()
    import user
