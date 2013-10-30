# -*- coding: utf-8 -*-
'''
Implements the QQExtractor class.
Jan Veverka, MIT, jan.veverka@cern.ch
29 July 2019
'''
import os
import sys
import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.canvases as canvases
import FWLite.Tools.dataset as datasetly
import FWLite.Hgg.trees as trees

from FWLite.Tools.resampler import Resampler
from FWLite.Hgg.photonid.variables import config_map
from FWLite.Hgg.photonid.corrector import PhotonIdCorrector

#______________________________________________________________________________
class QQExtractor:
    '''
    Extracts the Q-Q corrections for photon ID variables.
    '''
    #__________________________________________________________________________
    def __init__(self, varname, raw_name, target_name, option='noskim',
                 max_entries=-1, prescale=1, prescale_phase=0, rho=0.7):
        #print 'DEBUG', self.__class__.__name__, '__init__' 
        common_args = [varname, option, max_entries, prescale, prescale_phase]
        self.raw    = DataSource(raw_name   , *common_args)
        self.target = DataSource(target_name, *common_args)
        self.corrector = PhotonIdCorrector(self.raw.data, 
                                           self.target.data, rho)
        self.postprocess_corrector()
    ## End of QQExtractor.__init__(..)
    
    #__________________________________________________________________________
    def postprocess_corrector(self):
        '''
        Customizes corrector name and title and updetes raw and target sources
        with corrector pdfs.
        '''
        name = '_'.join([self.raw.xvar.GetName(), 'qq'])
        title = ' '.join([self.raw.xvar.GetTitle(),
                          self.raw   .name.split('-')[0].capitalize(), 'to',
                          self.target.name.split('-')[0].capitalize(),
                          'Q-Q Corrector'])                 
        self.corrector.SetName(name)
        self.corrector.SetTitle(title)
        self.raw   .pdf = self.corrector.xpdf
        self.target.pdf = self.corrector.ypdf
    ## End of QQExtractor.postprocess_corrector()
    
    #__________________________________________________________________________
    def make_plots(self):
        '''
        Makes plots of the raw and target source, the corrector function,
        and the corrected data.
        '''
        for src in [self.raw, self.target]:
            plot = self.get_plot_of_source(src)
            canvases.next(src.varname + '_' + src.data.GetName()).SetGrid()
            self.draw_and_append(plot)
            ## Also with log scale on y-axis
            c = canvases.next(src.varname + '_' + src.data.GetName() + '_logy')
            c.SetGrid()
            c.SetLogy()
            plot.Draw()
        
        canvases.next(self.corrector.GetName()).SetGrid()
        self.draw_and_append(self.corrector.get_correction_plot())
        
        canvases.next(self.corrector.GetName() + '_adiff').SetGrid()
        self.draw_and_append(self.corrector.get_absolute_difference_plot())
        
        canvases.next(self.corrector.GetName() + '_rdiff').SetGrid()
        self.draw_and_append(self.corrector.get_relative_difference_plot())
        
        plot = self.corrector.get_validation_plot()
        cname = self.corrector.GetName() + '_validation'
        canvases.next(cname).SetGrid()
        self.draw_and_append(plot)
        ## Also y-axis log-scale
        canvases.next(cname + '_logy').SetGrid()
        canvases.canvases[-1].SetLogy()
        plot.Draw()
    ## End of QQExtractor.make_plots(..)
    
    #__________________________________________________________________________
    def get_plot_of_source(self, source):
        plot = source.xvar.frame(roo.Title(source.data.GetTitle()))
        source.data.plotOn(plot)
        source.pdf.plotOn(plot)        
        return plot
    ## End of QQExtractor.get_plot_of_source()
    
    #__________________________________________________________________________
    def draw_and_append(self, plot):
        if not hasattr(self, 'plots'):
            self.plots = []
        plot.Draw()
        self.plots.append(plot)
    ## End of QQExtractor.draw_and_append(plot)
    
    #__________________________________________________________________________
    def write_corrector_to_file(self, file_name):
        self.corrector.write_to_file(file_name, False)
        ## Also as an interpolation graph
        graph = self.corrector.get_interpolation_graph()
        out_file = ROOT.TFile.Open(file_name, "update")
        graph.Write()
        out_file.Write()
        out_file.Close()      
    ## End of QQExtractor.write_to_file(..)
    
## End of class QQExtractor


#______________________________________________________________________________
class DataSource:
    '''
    Holds data related to a given data source.
    '''
    #__________________________________________________________________________
    def __init__(self, name, varname, option, max_entries, prescale,
                 prescale_phase=0):
        print 'DEBUG', self.__class__.__name__, '__init__' 
        if prescale > 1:
            msg = ', '.join(['max_entries=%d' % max_entries,
                              'prescale=%d' % prescale])
            raise RuntimeError, 'Illegal arguments ' + msg
        self.name = name
        self.varname = varname
        #self.max_entries = max_entries
        #self.option = self.option
        tree = trees.get(name, option)
        cfg = config_map[varname]
        datasets = []
        ## Get a dataset for each expression-selection pair
        for expr, cuts in zip(cfg.expressions, cfg.selections):
            if hasattr(cfg, 'qqbinning') and len(cfg.qqbinning.split(',')) == 3:
                nbins, varmin, varmax = map(float, cfg.qqbinning.split(','))
                variable = ROOT.RooRealVar(cfg.name, expr, varmin, varmax)
                variable.setBins(int(nbins))
            else:
                variable = ROOT.RooRealVar(cfg.name, expr, 0.)
            cuts = [cuts]
                ## Adds an appropriate prescale
            if max_entries > 0:
                all_entries = float(tree.GetEntries())
                prescale = ROOT.TMath.CeilNint(all_entries / max_entries)
            if prescale > 1:
                cut = 'Entry$ %% %d == %d' % (prescale, prescale_phase)
                print 'Prescaling %s: %s' % (name, cut)
                cuts.append(cut)
            dataset = datasetly.get(tree=tree, variable=variable, cuts=cuts)
            variable = dataset.get().first()
            variable.SetTitle(cfg.title)
            variable.setUnit(cfg.unit)
            datasets.append(dataset)
        ## End of loop over expressions and selections
        dataset = datasets[0]
        for further_dataset in datasets[1:]:
            dataset.append(further_dataset)
        dataset.SetTitle('Raw ' + name.split('-')[0].capitalize())
        dataset.SetName('raw_' + name.split('-')[0])
        print 'max_entries, numEntries', max_entries, dataset.numEntries()
        #if max_entries > 0 and dataset.numEntries() > max_entries:
            ### Downsample to reduce the size of data
            #dataset.Print()
            #print 'QQ DEBUG: Downsampling to', max_entries
            #dataset = Resampler(dataset).downsample(max_entries)
            #dataset.Print()
        self.data = dataset
        self.xvar = dataset.get().first()
    ## End of DataSource.__init__(..)
## End of class DataSource
  

#______________________________________________________________________________
def main(varnames = 'r9b sieieb setab'.split()[:1],
         raw_name = 's12-zllm50-v7n',
         target_name = 'r12a-pho-j22-v1',
         option = 'skim10k',
         max_entries = 50000,
         prescale = 1,
         prescale_phase = 0,
         rho=0.8):
    '''
    Main entry point of execution.
    '''
    global extractors
    extractors = []
    name = '_'.join([raw_name.split('-')[0], 'to',
                     target_name.split('-')[0], 'qqcorrector'])
    out_file_name = '_'.join([raw_name.split('-')[0], 'to',
                              target_name.split('-')[0], 'qqcorrections.root'])
    if os.path.isfile(out_file_name):
        os.remove(out_file_name)
    for varname in varnames:
        print 'Q-Q Extractor: Processing', varname, '...'
        extractor = QQExtractor(varname, raw_name, target_name, option, 
                                max_entries, prescale, prescale_phase, rho)
        extractors.append(extractor)
        extractor.make_plots()
        canvases.update()
## End of main()


#______________________________________________________________________________
def save_and_cleanup(outdir = 'plots'):
    ## Save plots
    if not os.path.exists(outdir):
        print "Creating folder `%s'" % outdir
        os.mkdir(outdir)
    else:
        ## TODO: remove outdir
        pass
    canvases.make_plots(['png', 'root'], outdir)
    canvases.make_pdf_from_eps(outdir)
    ## Store corrections
    for extractor in extractors:
        raw    = extractor.raw   .name.split('-')[0]
        target = extractor.target.name.split('-')[0]
        out_file_name = '_'.join([raw, 'to', target, 'qqcorrections.root'])
        extractor.write_corrector_to_file(outdir + '/' + out_file_name)
    ## Cleanup
    trees.close_files()
## End of save_and_cleanup()


#______________________________________________________________________________
if __name__ == '__main__':
    roo.silence()
    main()
    import user
    ## Clean up to prevent horrible root crashes.
    if ROOT.gROOT.IsBatch():
        save_and_cleanup()
    
