'''
Given a selection and photon scale and resolution,
fetch a RooDataSet of mmgMass MC data smeared such that the photon detector
responce Ereco/Etrue has the same shape as the nominal MC but has the given
scale and resolution.
'''
import ROOT
import JPsi.MuMu.common.roofit as roofit
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.tools as tools
from JPsi.MuMu.common.energyScaleChains import getChains
from JPsi.MuMu.common.latex import Latex

scale = 0.0
resolution = 5
# refScale = 3.49234e-2
# refResolution = 5.30486e-2
refScale = 3.46466
refResolution = 5.22628

nogarbage = []

##------------------------------------------------------------------------------
def geteffsigma(pdf, obs):
    'Returns the effective sigma of pdf of observable obs.'
    ## TODO: use the pdf itself instead of sampling it into a histogram?
    hist = pdf.createHistogram(obs.GetName(), 10000)
    hist.Scale(10000)
    return tools.effSigma(hist)
## End of geteffsigma

##------------------------------------------------------------------------------
def getmode(pdf, obs,
            ## Trick to have static variables zero and minusone
            zero = ROOT.RooConstVar('zero', 'zero', 0),
            minusone = ROOT.RooConstVar('minusone', 'minusone', -1)):
    'Returns the mode of a given pdf in observable RooAbsArg obs.'
    ## Set all parameters constant, remembering their constantness
    saveconst = []
    params = pdf.getParameters(ROOT.RooArgSet(obs))
    itpar = params.createIterator()
    for i in range(params.getSize()):
        p = itpar()
        saveconst.append(p.isConstant())
        p.setConstant(True)
    ## Create the function to be minimized: -pdf
    minuspdf = ROOT.RooPolyVar('minus_' + pdf.GetName(),
                               'Minus ' + pdf.GetTitle(),
                               pdf, ROOT.RooArgList(zero, minusone))
    ## Find the minimum with minuit
    minuit = ROOT.RooMinuit(minuspdf)
    minuit.migrad()
    ## Reset the constantness of the parameters of the pdf and
    itpar.Reset()
    for i in range(params.getSize()):
        itpar().setConstant(saveconst[i])
    return obs.getVal()
## End of getmode

##------------------------------------------------------------------------------
class ParametrizedKeysPdf(ROOT.RooKeysPdf):
    'Introduce location and scale parameters.'

    def __init__(self, name, title, x, mode, width, data,
                 mirror=ROOT.RooKeysPdf.NoMirror, rho=1., forcerange=True):

        self.shape = ROOT.RooKeysPdf(name + '_shape', title + ' shape', x, data,
                                     mirror, rho)
        self.shapewidth = geteffsigma(self.shape, x)
        self.shapemode = getmode(self.shape, x)
        if self.shapewidth <= 0.:
            raise RuntimeError, 'Illegal value of pdf width: %f.' % self.shapewidth
        ## Define the transformation of x that introduces the dependence on the
        ## mode and width
        self.xtransform = ROOT.RooFormulaVar(
            x.GetName() + '_linearTransform_' + name,
            x.GetTitle() + ' Linear Transform for Substitution in ' + title,
            "{shapemode} + ({x} - {mode}) * {shapewidth} / {width}".format(
                x=x.GetName(), shapemode=self.shapemode, mode=mode.GetName(),
                width=width.GetName(), shapewidth=self.shapewidth
                ),
            ROOT.RooArgList(x, mode, width)
            )
        if forcerange:
            ## Restrict the allowed tranformed values to the range where the
            ## PDF was trained.
            self.xtransform_ranged = ROOT.RooFormulaVar(
                x.GetName() + '_rangedLinearTransform_',
                x.GetTitle() + ' Lin. Transform constrained to a Range',
                ('{lo} * ({x} <= {lo}) + '
                 '{x} * ({lo} < {x} & {x} < {hi}) + '
                 '{hi} * ({hi} <= {x})').format(x=self.xtransform.GetName(),
                                                lo=x.getMin(),
                                                hi=x.getMax()),
                ROOT.RooArgList(self.xtransform)
                )
        self.customizer = ROOT.RooCustomizer(self.shape, 'transform')
        if forcerange:
            self.customizer.replaceArg(x, self.xtransform_ranged)
        else:
            self.customizer.replaceArg(x, self.xtransform)

        ROOT.RooKeysPdf.__init__(self, self.customizer.build())
        #self.pdf = self.customizer.build()
    ## end of __init__
## end of ParameterizedKeysPdf

##------------------------------------------------------------------------------
def get_parametrized_keyspdf(name, title, x, mode, width, data,
                             mirror=ROOT.RooKeysPdf.NoMirror, rho=1.,
                             forceRange=True):
    """Build a KEYS PDF that depends on the location and scale parameters
    mode and width. Mode is the mode of the PDF and width is it's effictive
    sigma - the shortest interval covering 68% of the distribution.
    """
    pdfshape = ROOT.RooKeysPdf(name + '_shape', title + ' shape', x, data,
                               mirror, rho)
    nominalwidth = geteffsigma(pdfshape, x)
    nominalmode = getmode(pdfshape, x)
    if nominalwidth <= 0.:
        raise RuntimeError, 'Illegal value of pdf width: %f.' % nominalwidth
    ## Define the transformation of x that introduces the dependence on the
    ## mode and width
    xtransform = ROOT.RooFormulaVar(
        x.GetName() + '_linearTransform_' + name,
        x.GetTitle() + ' Linear Transform for Substitution in ' + title,
        "{nominalmode} + ({x} + {mode}) * {nominalwidth} / {width}".format(
            x=x.GetName(), nominalmode=nominalmode, mode=mode.GetName(),
            width=width.GetName(), nominalwidth=nominalwidth
            ),
        ROOT.RooArgList(x, mode, width)
        )
    if forceRange:
        ## Restrict the allowed tranformed values to the range where the
        ## PDF was trained.
        xtransform_ranged = ROOT.RooFormulaVar(
            x.GetName() + '_rangedLinearTransform_',
            x.GetTitle() + ' Lin. Transform constrained to a Range',
            ('{lo} * ({x} <= {lo}) + '
             '{x} * ({lo} < {x} & {x} < {hi}) + '
             '{hi} * ({hi} <= {x})').format(x=xtransform.GetName(),
                                            lo=x.getMin(),
                                            hi=x.getMax()),
            ROOT.RooArgList(xtransform)
            )
    ## Replace the observable with it's ranged transform
    customizer = ROOT.RooCustomizer(pdfshape, 'transform')
    if forceRange:
        customizer.replaceArg(x, xtransform_ranged)
    else:
        customizer.replaceArg(x, xtransform)
    ## TODO: Do we need to keep the customizer if it owns the new PDF?
    nogarbage.append(customizer)
    return customizer.build()
## end of get_parametrized_keyspdf
                      
##------------------------------------------------------------------------------
## Here starts the meat.
w = ROOT.RooWorkspace('w')

## Define data variables 
mmgMass = w.factory('mmgMass[40, 140]')
mmMass = w.factory('mmMass[10, 140]')
phoERes = w.factory('phoERes[-70, 100]')
## mmgMassPhoSmearE = w.factory('mmgMassPhoSmearE[40, 140]')
## phoEResSmear = w.factory('phoEResSmear[-80, 110]')


weight = w.factory('weight[1]')
## phoScale = w.factory('phoScale[0,-50,50]')
weight.SetTitle('pileup.weight')

phoERes.SetTitle('100 * phoERes')
## mmgMassPhoSmearE.SetTitle('mmgMassPhoSmearE('
##     '{s}, {r}, {sref}, {rref}, phoE, phoGenE, mmgMass, mmMass'
##     ')'.format(s=scale, r=resolution, sref=refScale, rref=refResolution))

## phoEResSmear.SetTitle('100 * phoSmearE({s}, {r}, {sref}, {rref}, phoE, phoGenE) / '
##                            'phoGenE - 1'.format(s=scale/100., r=resolution/100.,
##                                                 sref=refScale/100.,
##                                                 rref=refResolution/100.))


cuts = ['phoIsEB',
        'phoR9 < 0.94',
        '15 < phoPt & phoPt < 20',
        'mmMass + mmgMass < 190',
        'isFSR',
        'phoGenE > 0',
        ]

## Create a preselected tree
zchain = getChains('v11')['z']
tree = zchain.CopyTree('&'.join(cuts))

## Have to copy aliases by hand
for a in zchain.GetListOfAliases():
    tree.SetAlias(a.GetName(), a.GetTitle())

## Get the nominal dataset
data = dataset.get(tree=tree, weight=weight, cuts=cuts,
                   variables=[mmgMass, mmMass, phoERes,
                              #mmgMassPhoSmearE,
                              #phoEResSmear
                              ])

# mmgMassPhoSmearE.SetTitle('mmgMassPhoSmearE')
phoERes.SetTitle('phoERes')
# phoEResSmear.SetTitle('phoEResSmear')


##------------------------------------------------------------------------------
## Test if it worked
data.SetName('data')
data.SetTitle('data')
w.Import(data)

## Build models
range_save = (phoERes.getMin(), phoERes.getMax())
phoERes.setRange(-90, 150)
phoEResPdf = w.factory('KeysPdf::phoEResPdf(phoERes, data, NoMirror, 1.5)')
phoERes.setRange(*range_save)

## range_save = (phoEResSmear.getMin(), phoEResSmear.getMax())
## phoEResSmear.setRange(-90, 150)
## phoEResSmearPdf = w.factory(
##     'KeysPdf::phoEResSmearPdf(phoEResSmear, data, NoMirror, 1.5)'
##     )
## phoEResSmear.setRange(*range_save)

## Extract the mode and effective sigma of the models
phoEResPdfEffSigma = geteffsigma(phoEResPdf, phoERes)
phoEResPdfMode = getmode(phoEResPdf, phoERes)
## phoEResSmearPdfEffSigma = geteffsigma(phoEResSmearPdf, phoEResSmear)
## phoEResSmearPdfMode = getmode(phoEResSmearPdf, phoEResSmear)

## Build models with floated scale and resolution
phoScaleNominal = w.factory('phoScaleNominal[%f]' % phoEResPdfMode)
phoResNominal = w.factory('phoResNominal[%f]' % phoEResPdfEffSigma)

phoEResFunc = w.factory('''expr::phoEResFunc(
    "phoScaleNominal + (phoERes - phoScale) *  phoResNominal / phoRes",
    {{phoERes, phoScale[{s}, -100, 100], phoRes[{r}, 0.5, 50], phoScaleNominal,
    phoResNominal}}
    )'''.format(s=phoEResPdfMode, r=phoEResPdfEffSigma))
phoEResFuncRanged = w.factory('''expr::phoEResFuncRanged(
    "(phoEResFunc <= {min}) * ({min}) +
     ({min} < phoEResFunc && phoEResFunc < {max}) * phoEResFunc +
     ({max} <= phoEResFunc) * ({max})",
    {{phoEResFunc}}
    )'''.format(min=phoERes.getMin(), max=phoERes.getMax()))
cust = ROOT.RooCustomizer(phoEResPdf, 'transfrom')
cust.replaceArg(phoERes, phoEResFuncRanged)
phoEResPdf_transform = cust.build()

## phoEResSmearFunc = w.factory('''expr::phoEResSmearFunc(
##     "phoScaleNominal + (phoResNominal - phoScale) * phoResNominal / phoRes",
##     {{phoEResSmear, phoScale, phoRes, phoScaleNominal, phoResNominal}}
##     )'''.format(s=phoEResPdfMode, r=phoEResPdfEffSigma))
## phoEResSmearFuncRanged = w.factory('''expr::phoEResSmearFuncRanged(
##     "(phoEResSmearFunc <= {min}) * ({min}) +
##      ({min} < phoEResSmearFunc && phoEResSmearFunc < {max}) * phoEResSmearFunc +
##      ({max} <= phoEResSmearFunc) * ({max})",
##     {{phoEResSmearFunc}}
##     )'''.format(min=phoERes.getMin(), max=phoERes.getMax()))
## cust = ROOT.RooCustomizer(phoEResPdf, 'transformSmear')
## cust.replaceArg(phoERes, phoEResSmearFuncRanged)
## phoEResPdf_transformSmear = cust.build()

plots = []
## Make plots
canvases.next()
plot = phoERes.frame(roofit.Range(-50, 50))
data.plotOn(plot)
phoEResPdf.plotOn(plot)
phoEResPdf_transform.fitTo(data)
phoEResPdf_transform.plotOn(plot, roofit.LineColor(ROOT.kRed),
                            roofit.LineStyle(ROOT.kDashed))
phoScale, phoRes = w.var('phoScale'), w.var('phoRes')
plot.Draw()
plots.append(plot)
latexlabels = Latex(['s_{keys}: %.3f %%' % phoEResPdfMode,
                     's_{fit}: %.3f #pm %.3f %%' % (phoScale.getVal(),
                                                    phoScale.getError()),
                     's_{fit} - s_{keys}: %.4f #pm %.4f' %
                     (phoScale.getVal() - phoEResPdfMode,
                      phoScale.getError()),
                     'r_{keys}: %.3f %%' % phoEResPdfEffSigma,
                     'r_{fit}: %.3f #pm %.3f %%' % (phoRes.getVal(),
                                                    phoRes.getError()),
                     'r_{fit}/r_{keys}: %.4f #pm %.4f' %
                     (phoRes.getVal() / phoEResPdfEffSigma,
                      phoRes.getError() / phoEResPdfEffSigma),])
latexlabels.draw()

## ## Plot the smeared photon energy
## canvases.next()
## plot = phoEResSmear.frame(roofit.Range(-50, 50))
## data.plotOn(plot)
## phoEResSmearPdf.plotOn(plot)
## phoEResPdf_transformSmear.fitTo(data)
## phoEResPdf_transformSmear.plotOn(plot, roofit.LineColor(ROOT.kRed),
##                                  roofit.LineStyle(ROOT.kDashed))
## plot.Draw()
## plots.append(plot)
## Latex(['s_{keys}: %.3f %%' % phoEResSmearPdfMode,
##        's_{fit}: %.3f #pm %.3f %%' % (phoScale.getVal(),
##                                       phoScale.getError()),
##        's_{fit} - s_{keys}: %.4f #pm %.4f %%' %
##        (phoScale.getVal() - phoEResSmearPdfMode,
##         phoScale.getError()),
##        'r_{keys}: %.3f %%' % phoEResSmearPdfEffSigma,
##        'r_{fit}: %.3f #pm %.3f %%' % (phoRes.getVal(), phoRes.getError()),
##        'r_{fit}/r_{keys}: %.4f #pm %.4f' %
##        (phoRes.getVal() / phoEResSmearPdfEffSigma,
##         phoRes.getError() / phoEResSmearPdfEffSigma),]).draw()

canvases.update()

print 'Nominal scale: %.3g%%' % phoEResPdfMode
print 'Nominal resolution: %.3g%%' % phoEResPdfEffSigma
## print 'Smeared scale: %.3g%%' % phoEResSmearPdfMode
## print 'Smeared resolution: %.3g%%' % phoEResSmearPdfEffSigma

phoScale2 = w.factory('phoScale2[0, -100, 100]')
phoRes2 = w.factory('phoRes2[5, 0.05, 50]')

phoEResPdf2 = ParametrizedKeysPdf('phoEResPdf2', 'phoEResPdf2',
                                  phoERes, phoScale2, phoRes2, data)


## if __name__ == "__main__":
##     import user

