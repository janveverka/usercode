'''Facilitates the creation and use of multiple canvases.'''
import ROOT

canvases = []

xperiod = 30
yperiod = 5
wheight = 500
wwidth = 700

#______________________________________________________________________________
def next(name=None, title=None):
    i = len(ROOT.gROOT.GetListOfCanvases())
    wtopx = 20 * (i % xperiod)
    wtopy = 20 * (i % yperiod)

    if name:
        if title:
            c1 = ROOT.TCanvas(name, title)
        else:
            c1 = ROOT.TCanvas(name, name)
    else:
        c1 = ROOT.TCanvas()

    c1.SetWindowPosition(wtopx, wtopy)
    c1.SetWindowSize(wheight, wwidth)

    canvases.append(c1)
    return c1
## end of next()
