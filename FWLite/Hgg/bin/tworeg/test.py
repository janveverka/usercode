'''
Use the module modeandeffsigmafitter to carry out all the fits.

Jan Veverka, Caltech, 4 Feb 2012
Last update: 5 Feb 2012
'''
import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.canvases as canvases
from modeandeffsigmafitter import ModeAndEffSigmaFitter

## CONFIGURATION BEGIN ========================================================
output_filename = 'test_mode_and_sigma_fit.root'

## 1: Use limited statistics for testing
## 0: Use full stats for final results 
debuglevel = 1

## The EM object type: 'pho' for photons, 'ele' for electrons.
em = 'pho'

## The data source type: 'mc' for Monte Carlo, 'data' for real data.
src = 'mc'

## The category: 'cat0', 'cat1', .., 'cat3' for analysis categories,
## 'calcat0', 'calcat1', ... 'calcat7' for calibration categories with
## more eta bins
cat = 'cat0'

## CONFIGURATION END ==========================================================

#______________________________________________________________________________
def main():
    '''
    Main entry point of execution.
    '''
    ## Mitigate numerical noise paying lower performance.
    if debuglevel == 0:
        ROOT.RooAbsReal.defaultIntegratorConfig().setEpsAbs(1e-9)
        ROOT.RooAbsReal.defaultIntegratorConfig().setEpsRel(1e-9)

    ## Assemble the job name
    name = '_'.join([em, src, cat])

    f = ModeAndEffSigmaFitter(name, debuglevel)
    f.run()


    ## Store RooFit objects in a rootfile
    w = ROOT.RooWorkspace('w')
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

    ## Make the plots
    canvases.make_plots('eps png C'.split())
## End of main()
    
    
#______________________________________________________________________________
if __name__ == '__main__':
        import user
        main()
