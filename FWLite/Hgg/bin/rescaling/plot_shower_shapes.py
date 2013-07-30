import os
import ROOT
import FWLite.Tools.canvases as canvases
import FWLite.Hgg.trees as trees

from FWLite.Hgg.photonid.variables import config_map

dataset = 'r12a-pho-j22-v1'
option = 'skim10k'

variables_to_plot = [
    'mass',
    'pt', 'pt1', 'pt2',
    'eta', 'eta1', 'eta2',
    'r9b', 'r9e',
    'setab', 'setae',
    'sphib', 'sphie',
    'sieieb', 'sieiee',
    'cieipb', 'cieipe',
    's4ratiob', 's4ratioe',
]


output_filename = trees.analysis + '_' + dataset + '_id-histos.root'
destination = os.path.join(trees.base_dir, trees.analysis, 'histos',
                           output_filename)
                           
tree = trees.get(dataset, option)
outfile = ROOT.TFile(destination, 'recreate')

hist = {}

for variable in variables_to_plot:
    cfg = config_map[variable]
    canvases.next(cfg.name).SetGrid()
    option = ''
    for expression, selection in zip(cfg.expressions, cfg.selections):
        if not ROOT.gDirectory.Get(cfg.name):
            varexp = expression + '>>' + cfg.name 
            if hasattr(cfg, 'binning'):
                varexp += '(' + cfg.binning + ')'
        else:
            varexp = expression + '>>+' + cfg.name
        tree.Draw(varexp, selection, option)
    hist[cfg.name] = ihist = ROOT.gDirectory.Get(cfg.name)
    binwidth = ihist.GetBinWidth(1)
    title_item = lambda e, c: c and '%s {%s}' % (e,c) or e
    title = ', '.join([title_item(e,c) for e,c in zip(cfg.expressions, 
                                                      cfg.selections)])
    xtitle = cfg.title
    ytitle = 'Events / %g' % binwidth
    if hasattr(cfg, 'unit') and cfg.unit:
        xtitle += ' (' + cfg.unit + ')'
        ytitle += ' ' + cfg.unit
    ihist.SetTitle(title)
    ihist.GetXaxis().SetTitle(xtitle)
    ihist.GetYaxis().SetTitle(ytitle)
    ihist.Draw()
    canvases.update()

    
#canvases.make_pdf_from_eps()
#outfile.Write()
#outfile.Close()

#formula = ROOT.TTreeFormula('mass', 'mass', tree)

#for i in range(10):
    #tree.GetEntry(i)
    #print i, formula.EvalInstance()

    