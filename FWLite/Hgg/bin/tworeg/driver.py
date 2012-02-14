'''
Use the module modeandeffsigmafitter to carry out all the fits.

Jan Veverka, Caltech, 4 Feb 2012
Last update: 5 Feb 2012
'''
import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.canvases as canvases
from modeandeffsigmafitter import ModeAndEffSigmaFitter

output_filename = 'mode_and_sigma_fit.root'

## 1: Use limited statistics for testing
## 0: Use full stats for final results 
debuglevel = 0

## Mitigate numerical noise paying lower performance.
if debuglevel == 0:
    ROOT.RooAbsReal.defaultIntegratorConfig().setEpsAbs(1e-9)
    ROOT.RooAbsReal.defaultIntegratorConfig().setEpsRel(1e-9)

fitters = []
for em in 'pho ele'.split():
    for src in 'data mc'.split():
        for icat in range(4):
            cat = 'cat%d' % icat
            print '+++ ', em, src, cat
            fitter = ModeAndEffSigmaFitter(name = '_'.join([em, src, cat]),
                                           debuglevel = debuglevel)
            fitter.run()
            fitters.append(fitter)
        for icalcat in range(8):
            cat = 'calcat%d' % icalcat
            print '+++ ', em, src, cat
            fitter = ModeAndEffSigmaFitter(name = '_'.join([em, src, cat]),
                                           debuglevel = debuglevel)        
            fitter.run()
            fitters.append(fitter)

## Store RooFit objects in a rootfile
w = ROOT.RooWorkspace('w')
for f in fitters:
    for item in [f.data, f.data_half_odd, f.data_half_even, f.model]:
        w.Import(item)
    w.Import(f.fit_data, f.name + '_fit_data')
    w.Import(f.train_data, f.name + '_train_data')
    w.Import(f.fit_result, f.name + '_fit_result')

w.writeToFile(output_filename)
        
## Store canvases in a rootfile
outfile = ROOT.TFile.Open(output_filename, 'UPDATE')
outfile.mkdir('Canvases').cd()
for c in canvases.canvases:
    if c:
        c.Write(c.GetName())

canvases.make_plots('eps png C'.split())

if __name__ == '__main__':
        import user
