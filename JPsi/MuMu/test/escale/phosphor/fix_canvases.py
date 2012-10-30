import os
import glob
import ROOT
import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.common.cmsstyle as cmsstyle

for path in glob.glob('/Users/veverka/Desktop/PHOSPHOR/v2/*/*'):
    
    for fname in glob.glob(os.path.join(path, '*_landscape.root')):
        print fname
        rootfile = ROOT.TFile.Open(fname)
        cname = os.path.splitext(os.path.basename(fname))[0]
        canvas = rootfile.Get(cname)
        canvas.Draw()
        canvas.SetWindowSize(1200, 600)
        canvases.canvases.append(canvas)

    for fname in glob.glob(os.path.join(path, '*_data.root')):
        print fname
        rootfile = ROOT.TFile.Open(fname)
        cname = os.path.splitext(os.path.basename(fname))[0]
        canvas = rootfile.Get(cname)
        canvas.Draw()
        canvas.SetWindowSize(600, 400)
        canvases.canvases.append(canvas)

    for fname in glob.glob(os.path.join(path, '*_combo.root')):
        print fname
        rootfile = ROOT.TFile.Open(fname)
        cname = os.path.splitext(os.path.basename(fname))[0]
        canvas = rootfile.Get(cname)
        canvas.Draw()
        canvas.SetWindowSize(500, 500)
        canvases.canvases.append(canvas)

    canvases.update()
    canvases.make_plots('png pdf'.split(), path=path)
    del canvases.canvases[:]
