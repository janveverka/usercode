'''
Fit the mode and effective sigma for the electron-by-electron difference
in energy from the Caltech and the hggv2 regressions.

Jan Veverka, Caltech, 4 February 2012
Last update: 5 February 2012
'''

import os
import ROOT
import FWLite.Tools.canvases as canvases
import FWLite.Tools.cmsstyle as cmsstyle
import FWLite.Tools.dataset as dataset
import FWLite.Tools.roofit as roo

from FWLite.Tools.modalinterval import ModalInterval
from FWLite.Tools.parameterizedkeyspdf import ParameterizedKeysPdf

class ModeAndEffSigmaFitter:
    def __init__(self, name='data_cat0', debuglevel=0, numentries=-1,
                 fitmode='odd-even'):
        ## Cofniguration data
        self.name = name

        ## 0: production, 1: debugging
        self.debuglevel = debuglevel
        self.numentries = numentries
        self.fitmode = fitmode

        self.numentries_train_max = 100000
        
        for tok in self.name.split('_'):
            if 'pho' in tok:
                self.emtype = 'pho'
            if 'ele' in tok:
                self.emtype = 'ele'
            if 'cat' in tok:
                self.cat = tok
            if 'data' in tok:
                self.src = 'data'
            elif 'mc' in tok:
                self.src = 'mc'
        
        ## Decoration
        self.labels = [{'mc': 'Simulation', 'data': 'Data'}[self.src]]
        self.labels.extend({
            'cat0': ['Barrel' , 'R_{9} > 0.94'],
            'cat1': ['Barrel' , 'R_{9} < 0.94'],
            'cat2': ['Endcaps', 'R_{9} > 0.94'],
            'cat3': ['Endcaps', 'R_{9} < 0.94'],
            'calcat0': ['Central Barrel' , 'R_{9} > 0.94'],
            'calcat1': ['Central Barrel' , 'R_{9} < 0.94'],
            'calcat2': ['Forward Barrel' , 'R_{9} > 0.94'],
            'calcat3': ['Forward Barrel' , 'R_{9} < 0.94'],
            'calcat4': ['Outer Endcaps', 'R_{9} > 0.94'],
            'calcat5': ['Outer Endcaps', 'R_{9} < 0.94'],
            'calcat6': ['Inner Endcaps', 'R_{9} > 0.94'],
            'calcat7': ['Inner Endcaps', 'R_{9} < 0.94'],
            }[self.cat])
        ## self.color = {
        ##     'cat0': ROOT.kRed,
        ##     'cat1': ROOT.kGreen,
        ##     'cat2': ROOT.kBlue,
        ##     'cat3': ROOT.kBlack,
        ##     'calcat0': ROOT.kRed,
        ##     'calcat1': ROOT.kRed - 3,
        ##     'calcat2': ROOT.kOrange - 2,
        ##     'calcat3': ROOT.kSpring + 5,
        ##     'calcat4': ROOT.kGreen,
        ##     'calcat5': ROOT.kAzure - 9,
        ##     'calcat6': ROOT.kBlue,
        ##     'calcat7': ROOT.kBlack
        ##     }[self.cat]
        self.color = ROOT.kBlack
        self.color_model = ROOT.kBlue
        self.color_data = ROOT.kBlack
        ## self.marker_style = {'data': 20, 'mc': 21}[self.src]
        self.marker_style = 20
        self.plots = []
        self.canvases = []
        self.fixed_range_zoom = (-8, 8)
        self.fixed_range_log = (-25, 25)
        self.init_workspace()
        self.get_data()
        
        
    ## End of __init__(self, ..).

    ##--------------------------------------------------------------------------
    def init_workspace(self):
        self.w = w = ROOT.RooWorkspace('w')

        ## Define the observable.
        self.deltaE = w.factory('deltaE[0, -50, 50]')

        # Define the model parameters.
        self.mode = w.factory('m[0, -50, 50]')
        self.effsigma = w.factory('effsigma[1, 0.1, 25]')
        self.effsigma.SetName('#sigma_{eff}')

        for x in [self.deltaE, self.mode, self.effsigma]:
            x.setUnit('%')
    ## End of init_workspace().
    

    ##--------------------------------------------------------------------------
    def get_data(self):
        'Gets the RooDataSet with deltaE data.'
        chain = ROOT.TChain('Analysis')
        datapath = '/raid2/veverka/yyTrees/tworeg'

        if self.emtype == 'pho':
            self.filenames = '''
testSelection.v3.PhotonRun2011AandB30Nov2011v1AOD.preselcut3.sel0.n1cut0.smear0.phtcorr219.phtid1.merged.root

testSelection.v3.GluGluToHToGG_M-140_7TeV-powheg-pythia6Fall11-PU_S6_START42_V14B-v1AODSIM.preselcut3.sel0.n1cut0.smear3.phtcorr219.phtid1.r1.root

testSelection.v3.TTH_HToGG_M-140_7TeV-pythia6Fall11-PU_S6_START42_V14B-v1AODSIM.preselcut3.sel0.n1cut0.smear3.phtcorr219.phtid1.r1.root

testSelection.v3.VBF_HToGG_M-140_7TeV-powheg-pythia6Fall11-PU_S6_START42_V14B-v1AODSIM.preselcut3.sel0.n1cut0.smear3.phtcorr219.phtid1.r1.root

testSelection.v3.WH_ZH_HToGG_M-140_7TeV-pythia6Fall11-PU_S6_START42_V14B-v1AODSIM.preselcut3.sel0.n1cut0.smear3.phtcorr219.phtid1.r1.root
'''.split()
        elif self.emtype == 'ele':
            self.filenames = '''
testSelectionZeev1.v3.DoubleElectronRun2011A30Nov2011v1AOD.etcut25.corr216.eleid1.datapu0.mcpu0.r*.scale1.root

testSelectionZeev1.v3.DoubleElectronRun2011B30Nov2011v1AOD.etcut25.corr216.eleid1.datapu0.mcpu0.r*.scale1.root
  
testSelectionZeev1.v3.DYJetsToLL_TuneZ2_M50_7TeVmadgraphtauolaFall11PU_S6_START42_V14Bv1AODSIM.etcut25.corr216.eleid1.datapu6.mcpu1.r*.scale0.root
'''.split()            
        else:
            raise RuntimeError, "Illegal emtype: `%s'!" % str(self.emtype)

        for f in self.filenames:
            chain.Add(os.path.join(datapath, f))

        ## Selection
        if self.emtype == 'pho':
            cuts = ['100 <= mpair & mpair <= 180']
        elif self.emtype == 'ele':
            cuts = ['80 <= mpair & mpair <= 100']
        else:
            raise RuntimeError, "Illegal emtype: `%s'!" % str(self.emtype)
            
        cuts.append({'mc'  : 'runNumber == 1',
                     'data': 'runNumber >  1'}[self.src])
        cuts.extend({
            'cat0': ['scr9 >  0.94', 'fabs(sceta) <  1.48'],
            'cat1': ['scr9 <= 0.94', 'fabs(sceta) <  1.48'],
            'cat2': ['scr9 >  0.94', 'fabs(sceta) >= 1.48'],
            'cat3': ['scr9 <= 0.94', 'fabs(sceta) >= 1.48'],
            'calcat0': ['scr9 >  0.94', 'fabs(sceta) <  1'],
            'calcat1': ['scr9 <  0.94', 'fabs(sceta) <  1'],
            'calcat2': ['scr9 >  0.94', '1 < fabs(sceta) & fabs(sceta) <  1.48'],
            'calcat3': ['scr9 <  0.94', '1 < fabs(sceta) & fabs(sceta) <  1.48'],
            'calcat4': ['scr9 >  0.94', '1.48 < fabs(sceta) & fabs(sceta) <  2'],
            'calcat5': ['scr9 <  0.94', '1.48 < fabs(sceta) & fabs(sceta) <  2'],
            'calcat6': ['scr9 >  0.94', '2 < fabs(sceta) & fabs(sceta) < 2.5'],
            'calcat7': ['scr9 <  0.94', '2 < fabs(sceta) & fabs(sceta) < 2.5'],
            }[self.cat])

        if self.numentries > 0:
            cuts.append('Entry$ < %d' % self.numentries)

        self.deltaE.SetTitle('200*(scen_bendavid - scen_yangyong)/'
                             '    (scen_bendavid + scen_yangyong)')
        self.data = dataset.get(tree=chain, variable=self.deltaE, cuts=cuts[:],
                                name=self.name + '_data')
        self.data_half_odd = dataset.get(tree=chain, variable=self.deltaE,
                                         cuts=cuts[:] + ['Entry$ % 2 == 0'],
                                         name=self.name + '_data_half_odd')
        self.data_half_even = dataset.get(tree=chain, variable=self.deltaE,
                                          cuts=cuts[:] + ['Entry$ % 2 == 1'],
                                          name=self.name + '_data_half_even')
        if self.debuglevel > 0:
            reduced_range = roo.EventRange(0, 5000)
            self.data = self.data.reduce(reduced_range)
            self.data_half_odd = self.data_half_odd.reduce(reduced_range)
            self.data_half_even = self.data_half_even.reduce(reduced_range)

        nentries = self.data.tree().Draw('deltaE', '', 'goff')
        self.modal_interval = ModalInterval(nentries,
                                            self.data.tree().GetV1(), 1.)
        if self.fitmode == 'odd-even':
            self.train_data = self.data_half_odd
            self.fit_data = self.data_half_even
        elif self.fitmode == 'event-odd':
            self.train_data = self.data_half_even
            self.fit_data = self.data_half_odd
        elif self.fitmode == 'full-full':
            self.train_data = self.data
            self.fit_data = self.data
        else:
            raise RuntimeError, "Fit mode `%s' not supported!" % self.fitmode

        ## Make sure that the trainining dataset isn't too large
        if self.train_data.numEntries() > self.numentries_train_max:
            prescale = (self.train_data.numEntries() /
                        self.numentries_train_max + 1)
            self.deltaE.SetTitle('deltaE')
            self.train_data = dataset.get(tree=self.train_data.tree(),
                                          variable=self.deltaE,
                                          cuts=['Entry$ %% %d == 0' % prescale],
                                          name=self.name + '_train_data')
        nentries = self.train_data.tree().Draw('deltaE', '', 'goff')
        self.modal_interval_training = ModalInterval(
            nentries, self.train_data.tree().GetV1(), 0.99
            )
                                                     
        ## Set a nice title for the x-axis of plots
        if self.emtype == 'pho':
            self.deltaE.SetTitle('Photon #DeltaE_{two regr.}/E')
        elif self.emtype == 'ele':
            self.deltaE.SetTitle('Electron #DeltaE_{two regr.}/E')
        else:
            raise RuntimeError, "Unsupported emtype `%s'!" % self.emtype        
    ## End of get_data().


    ##--------------------------------------------------------------------------
    def get_fit_based_range(self, nsigma = 5):
        return (self.mode.getVal() - nsigma * self.effsigma.getVal(),
                self.mode.getVal() + nsigma * self.effsigma.getVal())
    ## End of get_fit_based_range().

    ##--------------------------------------------------------------------------
    def make_log_plot(self):
        c1 = canvases.next(self.name + '_log_autorange')
        c1.SetGrid()
        c1.SetLogy()
        self.canvases.append(c1)

        ## Use the ModalInterval class to display the shortest range containing
        ## 100% of all the entries.
        mi = self.modal_interval
        mi.setFraction(1)

        fullrange = (mi.lowerBound(), mi.upperBound())
        plot = self.deltaE.frame(roo.Range(*fullrange))
        plot.SetTitle(', '.join(self.labels))
        self.data.plotOn(plot, roo.MarkerColor(self.color_data),
                         roo.MarkerStyle(self.marker_style),
                         roo.LineColor(self.color_data))
        self.model.plotOn(plot, roo.LineColor(self.color_model))
        if fullrange[0] + fullrange[1] > 0:
            layout = (0.6, 0.9, 0.87)
        else:
            layout = (0.2, 0.5, 0.87)
        self.model.paramOn(plot, roo.Format("NEU", roo.AutoPrecision(2)),
                           roo.Layout(*layout))
        ## Fine tune the y-axis range so that we see all the events.
        plot.SetMinimum(0.5)
        ## Add a larger top margin to the y-axis range
        plot.SetMaximum(pow(plot.GetMaximum(), 1.1))
        plot.Draw()
        self.plots.append(plot)
    ## End of make_log_plot().
    

    ##--------------------------------------------------------------------------
    def make_fixed_range_log_plot(self):
        c1 = canvases.next(self.name + '_log_fixedrange')
        c1.SetGrid()
        c1.SetLogy()
        self.canvases.append(c1)

        ## Use the ModalInterval class to display the shortest range containing
        ## 100% of all the entries.
        mi = self.modal_interval
        mi.setFraction(1)

        fullrange = (mi.lowerBound(), mi.upperBound())
        plot = self.deltaE.frame(roo.Range(*self.fixed_range_log))
        plot.SetTitle(', '.join(self.labels))
        self.fit_data.plotOn(plot, roo.MarkerColor(self.color_data),
                             roo.MarkerStyle(self.marker_style),
                             roo.LineColor(self.color_data))
        self.model.plotOn(plot, roo.LineColor(self.color_model))
        if fullrange[0] + fullrange[1] > 0:
            layout = (0.6, 0.9, 0.87)
        else:
            layout = (0.2, 0.5, 0.87)
        self.model.paramOn(plot, roo.Format("NEU", roo.AutoPrecision(2)),
                           roo.Layout(*layout))
        ## Fine tune the y-axis range so that we see all the events.
        plot.SetMinimum(0.5)
        ## Add a larger top margin to the y-axis range
        plot.SetMaximum(pow(plot.GetMaximum(), 1.1))
        plot.Draw()
        self.plots.append(plot)
    ## End of make_fixed_range_log_plot().
    

    ##--------------------------------------------------------------------------
    def make_zoom_plot(self):
        c1 = canvases.next(self.name + '_lin_autorange')
        c1.SetGrid()
        self.canvases.append(c1)
        plot = self.deltaE.frame(roo.Range(*self.get_fit_based_range()))
        plot.SetTitle(', '.join(self.labels))
        self.fit_data.plotOn(plot, roo.MarkerColor(self.color_data),
                             roo.MarkerStyle(self.marker_style),
                             roo.LineColor(self.color_data))
        self.model.plotOn(plot, roo.LineColor(self.color_model))
        self.model.paramOn(plot, roo.Format("NEU", roo.AutoPrecision(2)),
                           roo.Layout(0.2, 0.52, 0.87))
        plot.Draw()
        self.plots.append(plot)
    ## End of make_zoom_plot().

    ##--------------------------------------------------------------------------
    def make_fixed_range_zoom_plot(self):
        c1 = canvases.next(self.name + '_lin_fixedrange')
        c1.SetGrid()
        self.canvases.append(c1)
        plot = self.deltaE.frame(roo.Range(*self.fixed_range_zoom))
        plot.SetTitle(', '.join(self.labels))
        self.fit_data.plotOn(plot, roo.MarkerColor(self.color_data),
                             roo.MarkerStyle(self.marker_style),
                             roo.LineColor(self.color_data))
        self.model.plotOn(plot, roo.LineColor(self.color_model))
        self.model.paramOn(plot, roo.Format("NEU", roo.AutoPrecision(2)),
                           roo.Layout(0.2, 0.52, 0.87))
        plot.Draw()
        self.plots.append(plot)
    ## End of make_zoom_plot().

    ##--------------------------------------------------------------------------
    def run(self):
        ## Set the range of deltaE to cover all the date plus a small margin.
        mi = self.modal_interval
        mi.setFraction(1.)
        self.deltaE.setRange(mi.lowerBound() - 1, mi.upperBound() + 1)
        self.model = ParameterizedKeysPdf(self.name + '_model',
                                          self.name + '_model', self.deltaE,
                                          self.mode, self.effsigma,
                                          self.train_data, rho=2)
        mit = self.modal_interval_training
        mit.setFraction(0.99)
        fitrange = roo.Range(mit.lowerBound(), mit.upperBound())
        self.fit_result = self.model.fitTo(self.fit_data, roo.NumCPU(8),
                                           roo.Save(), fitrange)
        self.fit_result.SetName(self.name + '_fit_result')
        self.make_log_plot()
        self.make_zoom_plot()
        self.make_fixed_range_log_plot()
        self.make_fixed_range_zoom_plot()
        canvases.update()
    ## End of main()
## End of ModeAndEffSigmaFitter.

if __name__ == '__main__':
    import user
    ## ROOT.RooAbsReal.defaultIntegratorConfig().setEpsAbs(1e-9)
    ## ROOT.RooAbsReal.defaultIntegratorConfig().setEpsRel(1e-9)
    fitter = ModeAndEffSigmaFitter(name='ele_data_cat1', debuglevel = 1)
    fitter.run()
