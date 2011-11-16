import ROOT
import JPsi.MuMu.common.roofit as roofit
import JPsi.MuMu.common.dataset as dataset
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.common.cmsstyle as cmsstyle
import JPsi.MuMu.common.energyScaleChains as esChains

## Define the model
w = ROOT.RooWorkspace('w', 'w')

## Dimuon mass in terms of m(mmg) and m(mg)'s
mmMassFunc = w.factory('''FormulaVar::mmMassFunc(
    "sqrt(mmgMass^2 - m1gMass^2 - m2gMass^2)",
    {mmgMass[0,200], m1gMass[0,200], m2gMass[0,200]}
    )''')

## Breit-Wigner modelling Z-lineshape
zmmGenShape = w.factory('''BreitWigner::zmmGenShape(mmMass[20,200],
                                                    MZ[91.2], GZ[2.5])''')
## Dimuon mass resolution
mmMassRes = w.factory('''CBShape::mmMassRes(mmMass,
                                            mmScale[0,-10,10],
                                            mmRes[1.5,0.1,10],
                                            mmCut[1.5,0.5,5],
                                            mmPower[1.5,0.5,10])''')

## Model for the reconstructed dimuon invariant mass
mmMass = w.var('mmMass')
mmMass.setBins(1000, 'fft')
mmMassPdf = w.factory('FCONV::mmMassPdf(mmMass, zmmGenShape, mmMassRes)')

## Get data
chains = esChains.getChains('v11')
weight = w.factory('dummyWeight[1,0,55]')
weight.SetTitle('1')

mmgMass = w.var('mmgMass')
m1gMass = w.var('m1gMass')
m2gMass = w.var('m2gMass')

mmMassIsrData = dataset.get(tree=chains['z'], variable=mmMass, weight=weight,
                            cuts=['!isFSR', 'mmgMass < 200', 'mmMass < 200',
                                  'phoPt > 10', 'Entry$ < 10000'])
mmgMassIsrData = dataset.get(variable=mmgMass)
m1gMassIsrData = dataset.get(variable=m1gMass)
m2gMassIsrData = dataset.get(variable=m2gMass)


isrData = mmgMassIsrData
isrData.merge(mmMassIsrData, m1gMassIsrData, m2gMassIsrData)

## Fit the model to the data
mmMassPdf.fitTo(mmMassIsrData, roofit.Range(60,120))

## Plot the data and the fit
mmPlot = mmMass.frame(roofit.Range(60,120))
mmMassIsrData.plotOn(mmPlot)
mmMassPdf.plotOn(mmPlot)
canvases.next('mmMass')
mmPlot.Draw()

## Model for the reconstructed mmg mass of the ISR through transformation
mmgMassIsrPdf = ROOT.RooFFTConvPdf('mmgMassIsrPdf', 'mmgMassIsrPdf', mmMassFunc,
                                   mmMass, zmmGenShape, mmMassRes)

## Plot the mmg mass data and model overlaid without fitting (!)
mmgPlot = mmMass.frame(roofit.Range(60,120))
isrData.plotOn(mmgPlot)
isrData_m1gMass_m2gMass = isrData.reduce(ROOT.RooArgSet(m1gMass,m2gMass)).binnedClone()
mmgMassIsrPdf.plotOn(mmgPlot,roofit.ProjWData(isrData_m1gMass_m2gMass))
canvases.next('mmgMass')
mmgPlot.Draw()
