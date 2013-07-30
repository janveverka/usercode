'''
Tests FWLite.Hgg.photonid.corrector.PhotonIdCorrector
Jan Veverka, MIT, jan.veverka@cern.ch
28 July 2013
'''
import sys
import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.canvases as canvases
import FWLite.Tools.dataset as datasetly
import FWLite.Hgg.trees as trees

from FWLite.Hgg.photonid.variables import config_map
from FWLite.Hgg.photonid.corrector import PhotonIdCorrector

plots = []

#______________________________________________________________________________
def test(max_entries = -1):
    '''
    Tests the PhotonIdCorrector class.
    '''
    global raw_data, target_data, corr, vplot
    varname = 'setab'
    option = 'skim10k'
    raw_name = 's12-zllm50-v7n'
    target_name = 'r12a-pho-j22-v1'
    raw_data    = get_dataset(raw_name, varname, max_entries, option)
    target_data = get_dataset(target_name, varname, max_entries, option)
    xvar = raw_data.get().first()

    raw_data.SetTitle('Raw ' + raw_name.split('-')[0].capitalize())
    target_data.SetTitle('Raw ' + target_name.split('-')[0].capitalize())
    
    corr = PhotonIdCorrector(raw_data, target_data, rho=0.7)
    corr.SetName('_'.join([raw_name.split('-')[0], 'to',
                           target_name.split('-')[0], varname, 'qqcorrector']))
    corr.SetTitle(' '.join([raw_name.split('-')[0].capitalize(), 'to',
                            target_name.split('-')[0].capitalize(),
                            xvar.GetTitle(), 'Q-Q Corrector']))
    
    plot = xvar.frame(roo.Title(raw_data.GetTitle()))
    raw_data.plotOn(plot)
    corr.xpdf.plotOn(plot)
    canvases.next(varname + '_' + raw_name.split('-')[0]).SetGrid()
    draw_and_append(plot)

    plot = xvar.frame(roo.Title(target_data.GetTitle()))
    target_data.plotOn(plot)
    corr.ypdf.plotOn(plot)
    canvases.next(varname + '_' + target_name.split('-')[0]).SetGrid()
    draw_and_append(plot)
    
    canvases.next(corr.GetName()).SetGrid()
    draw_and_append(corr.get_correction_plot())
    
    canvases.next(corr.GetName() + '_validation').SetGrid()
    draw_and_append(corr.get_validation_plot())
    
    canvases.update()

## End of test()


#______________________________________________________________________________
def get_dataset(data_name, varname, max_entries = -1, option = 'merged'):
    tree = trees.get(data_name, option)
    cfg = config_map[varname]
    datasets = []
    ## Get a dataset for each expression-selection pair
    for expr, cuts in zip(cfg.expressions, cfg.selections):
        if hasattr(cfg, 'binning') and len(cfg.binning.split(',')) == 3:
            nbins, varmin, varmax = map(float, cfg.binning.split(','))
            variable = ROOT.RooRealVar(cfg.name, expr, varmin, varmax)
            variable.setBins(int(nbins))
        else:
            variable = ROOT.RooRealVar(cfg.name, expr)
        cuts = [cuts]
        if max_entries > 0:
            cuts.append('Entry$ < %d' % max_entries)
        dataset = datasetly.get(tree=tree, variable=variable, cuts=cuts)
        variable = dataset.get().first()
        variable.SetTitle(cfg.title)
        variable.setUnit(cfg.unit)
        datasets.append(dataset)
    ## End of loop over expressions and selections
    dataset = datasets[0]
    for further_dataset in datasets[1:]:
        dataset.append(further_dataset)
    return dataset
## End of get_dataset()


#______________________________________________________________________________
def draw_and_append(plot):
    plot.Draw()
    plots.append(plot)
## End of draw_and_append(plot)


#______________________________________________________________________________
if __name__ == '__main__':
    import user
    test()
    ## Clean up to prevent horrible root crashes.
    if not '-i' in sys.argv:
        canvases.make_pdf_from_eps('plots')
        trees.close_files()
    
