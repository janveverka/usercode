'''Defines PDF's for the energy scale extraction from fit to s = E_reco/E_kin
using the Z->mumugamma FSR events.  Models are stored in a workspace together
with argument lists of observables (only s), parameters and snapshots of
their initial values. Supported models (instance names in brackets):
  * Crystal-Ball Line Shape (cbShape, model)
  * Cruijff (cruijff)
  * Bifurcated Gaussian (bifurGauss)
  * (Normal) Gaussian

The parameter argument set and inital snapshots are stored as
`parameters_<model name>' and `initial_<model name>' where <model name>
is the name used above.

Plan to implement, Log-Normal, Bifurcated Log-Normal and Gamma
distributions.
'''
from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *

## Load custom models
gSystem.Load('libJPsiMuMu')

## Define the workspace
ws1 = RooWorkspace( 'ws1', 'mmg energy scale' )

## Define the quantity to be fitted and the event weight
x = RooRealVar( 's', '100 * (1/kRatio - 1)', -100, 100, '%' )
w = RooRealVar( 'w', '1', 0, 99 )

xw = RooArgSet(x, w)
ws1.Import(xw)

dummy_params = ws1.factory('''{
    #Deltas[0, -50, 50],
    #sigma[20, 0.001, 100],
    #sigmaL[20, 0.001, 100],
    #sigmaR[20, 0.001, 100],
    #alpha[-1.5, -10, 0],
    #alphaL[10, 0.0, 100],
    #alphaR[10, 0.0, 100],
    n[1.5, 0.1, 10],
    k[1.2, 1.001, 3],
    FormulaVar::exp_x("s/100+1", {s}),
    FormulaVar::m0("(#Deltas/100+1)*pow(k,ln(k))", {#Deltas, k}),
}''')
models = [
    ## For backward compatibility
    ws1.factory('Gaussian::gauss(s, #Deltas, #sigma)'),
    ws1.factory('Lognormal::lognormal(exp_x, m0, k)'),
    ws1.factory('BifurGauss::model(s, #Deltas, #sigmaL, #sigmaR)'),
    ws1.factory('CBShape::cbShape(s, #Deltas, #sigma, #alpha, n)'),
    ws1.factory('''RooCruijff::cruijff(s, #Deltas, #sigmaL, #sigmaR, #alphaL,
                                       #alphaR)'''),
    ws1.factory('BifurGauss::bifurGauss(s, #Deltas, #sigmaL, #sigmaR)'),
] ## end of models definition

## Define observables
observables = RooArgSet(x)

## Define parameters for model
for m in models:
    parameters = m.getParameters(observables)
    ws1.defineSet("parameters_" + m.GetName(), parameters)
    ws1.saveSnapshot("initial_" + m.GetName(), parameters, True)

