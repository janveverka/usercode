import commands
import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.canvases as canvases
import Zmmg.FWLite.showershape.r9_scaling_fitter as fitter

## CONFIGURATION BEGIN ========================================================
base_name = 'R9_EE_pt25up_v15reco'
base_cuts =  [
    '!phoIsEB',
    'phoPt > 25',
    'mmMass + mmgMass < 180',
    '!muNearIsEB',
    ]

fitter.name = base_name
fitter.title = 'Barrel'
fitter.tree_version = 'v15reco'
fitter.variable = ROOT.RooRealVar('R9', 'Photon R_{9}', 0.3, 1.1)
fitter.varexpression = 'phoR9'
fitter.weight = {
    'z'   : ROOT.RooRealVar('weight', 'pileup.weight', 0, 100),
    'data': ROOT.RooRealVar('weight', '1', 0, 100),
    }
fitter.cuts = base_cuts + [
    ## Require photons to be in squre of side N-1 = 0, 1, ..., centered
    ## on the central crystal.
    'TMath::Max(abs(muNearIEtaX - phoIEtaX), abs(muNearIPhiY - phoIPhiY)) == 0',
    ]
fitter.fit_range = (0.3, 1.1)
fitter.plot_range = (0.85, 1.0)
fitter.output_filename = 'r9fit.root'
## CONFIGURATION END ==========================================================

scalings = []
names = []


#______________________________________________________________________________
def fit_numerator():
    '''
    Fits the R9 scaling and make the plots for the situation when the nearest
    muon crosses the 3x3 crystals centered on the photon seed.
    '''
    fitter.name = base_name + '_muInNumerator'
    fitter.cuts = base_cuts + [
        ## Require photons to be in squre of side N-1 = 0, 1, ..., centered
        ## on the central crystal.
        ('TMath::Max(abs(muNearIEtaX - phoIEtaX), '
                    'abs(muNearIPhiY - phoIPhiY)) < 2'),
        ]
    fitter.labels =  [
        '#mu hits 3x3',
        '(R_{9} numer. and denom.)',
        '',
        'E_{T}^{#gamma} > 25 GeV',
        'Endcaps',
    ]
    scalings.append(fitter.main())
    names.append(fitter.name)
## End of fit_numerator()

    

#______________________________________________________________________________
def fit_denominator():
    '''
    Fits the R9 scaling and make the plots for the situation when the nearest
    muon crosses the photon supercluster outside of the 3x3 crystals
    centered on the photon seed.
    '''
    fitter.name = base_name + '_muInDenominator'
    fitter.cuts = base_cuts + [
        ## Require photons to be in squre of side N-1 = 0, 1, ..., centered
        ## on the central crystal.
        ('TMath::Max(abs(muNearIEtaX - phoIEtaX), '
                    'abs(muNearIPhiY - phoIPhiY)) == 2'),
        ]
    fitter.labels =  [
        '#mu hits SC outside 3x3',
        '(R_{9} denominator)',
        '',
        'E_{T}^{#gamma} > 25 GeV',
        'Endcaps',
    ]
    scalings.append(fitter.main())
    names.append(fitter.name)
## End of fit_numerator()

    
#______________________________________________________________________________
def fit_outside():
    '''
    Fits the R9 scaling for a number situation when the muon does not cross
    the SC and is further and further away from it.
    '''
    for index in range(2,10):
        side = 2 * index + 1
        fitter.name = base_name + '_muOutside%dx%d' % (side, side)
        fitter.cuts = base_cuts + [
            ## Require photons to be in squre of side N-1 = 0, 1, ..., centered
            ## on the central crystal.
            ('TMath::Max(abs(muNearIEtaX - phoIEtaX), '
                        'abs(muNearIPhiY - phoIPhiY)) > %d' % index),
            ]
        fitter.labels =  [
            '#mu outside %dx%d' % (side, side),
            '',
            '',
            'E_{T}^{#gamma} > 25 GeV',
            'Endcaps',
        ]

        scalings.append(fitter.main())
        names.append(fitter.name)
## End of fit_outside()

#______________________________________________________________________________
def print_report():
    '''
    Prints a list of the fitted scalings for the various classes.
    '''
    print '=== R9 Scalings ==='
    for name, (s, e) in zip(names, scalings):
        print name + ":",  "%.5f +/- %.5f" % (s, e)
## End of print_report()


#______________________________________________________________________________
def build_animation():
    '''
    Creates an animated gif out of the canvases.
    '''
    canvases.make_plots(['gif'])
    mc_files, data_files = [], []

    ## Create lists of files with the animation snapshots
    for c in canvases.canvases:
        if 'MC' in c.GetName():
            mc_files.append(c.GetName() + '.gif')
        else:
            data_files.append(c.GetName() + '.gif')

    ## Repeat the first snapshot 3xtimes and the 2nd 2xtimes.
    for files in [mc_files, data_files]:
        files = 3 * files[:1] +  2 * files[1:2] + mc_files[2:]
    
    options = ' --delay=100 --loop'
    command = 'gifsicle %s \\\n    %s > %s_Animation_MC.gif' % (
        options, '\\\n    '.join(mc_files), base_name
        )
    print command
    commands.getoutput(command)
        
    command = 'gifsicle %s \\\n    %s > %s_Animation_Data.gif' % (
        options, '\\\n    '.join(data_files), base_name
        )
    print command
    commands.getoutput(command)
## End of build_animation()


#______________________________________________________________________________
def make_pdf_plots():
    '''
    Creates pdf files out of the canvases.
    '''
    canvases.make_plots(['eps'])
    ## Create lists of files with the animation snapshots
    for c in canvases.canvases:
        command = "ps2pdf -dEPSCrop %s.eps" % c.GetName()
        print command
        commands.getoutput(command)
## End of make_pdf_plots()


#______________________________________________________________________________
def main():
    '''
    Main entry point for exectuion.
    '''
    fit_numerator()
    fit_denominator()
    fit_outside()
    # build_animation()
    make_pdf_plots()
    print_report()
## End of main()


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user
    
