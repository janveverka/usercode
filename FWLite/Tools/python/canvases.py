'''Facilitates the creation and use of multiple canvases.'''
import ROOT

canvases = []

xperiod = 30
yperiod = 5
wheight = 500
wwidth = 700

#______________________________________________________________________________
def next(name=None, title=None):
    update()
    i = len(ROOT.gROOT.GetListOfCanvases())
    wtopx = 20 * (i % xperiod)
    wtopy = 20 * (i % yperiod)

    if name:
        if ROOT.gROOT.GetListOfCanvases().FindObject(name):
            i = 0
            while ROOT.gROOT.GetListOfCanvases().FindObject(name + '_%d' % i):
                i += 1
            name = name + '_%d' % i
            if title:
                title = title + ' %d' % i
        if title:
            c1 = ROOT.TCanvas(name, title)
        else:
            c1 = ROOT.TCanvas(name, name)
    else:
        c1 = ROOT.TCanvas()

    c1.SetWindowPosition(wtopx, wtopy)
    c1.SetWindowSize(wwidth, wheight)

    canvases.append(c1)
    return c1
## end of next()

#______________________________________________________________________________
def make_plots(graphics_extensions = ['png']):
    for c in canvases:
        if not c:
            continue
        for ext in graphics_extensions:
            c.Print(''.join([c.GetName(), '.', ext]))
        ## end of loop over graphics_extensions
    ## end of loop over canvases
## end of make_plots()

#______________________________________________________________________________
def update():
    for c in canvases:
        if c:
            c.Update()
    ## end of loop over canvases
## end of update()

