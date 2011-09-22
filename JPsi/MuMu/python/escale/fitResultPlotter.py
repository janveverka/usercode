'''
Facilitates the plotting of ynames versus the the fit range iteration.
    Usage: python -i plotScaleVsFitRangeIter.py
'''
from JPsi.MuMu.common.basicRoot import *
from JPsi.MuMu.common.roofit import *

gSystem.Load('libJPsiMuMu')
from ROOT import RooCruijff
import math

## Initialize data
filenames = []
wsnames = []
snapshots = []

xname, xtitle, xdata, exdata = None, None, None, None
yname, ytitle, ydata, eydata = None, None, None, None

labels = []
graphs = []
graph = None

logy = False

_filename = None
_file = None
_wsname = None
_workspace = None
_xvar = None
_yvar = None

#------------------------------------------------------------------------------
def init():
    '''Initialize private data members.'''
    global _file, _filename, _workspace, _wsname, xname, _xvar, yname, _yvar

    ## Check if we need to update the file
    if not _file or _file.GetName() != _filename:
        _file = ROOT.TFile(_filename)
        _workspace = _file.Get(_wsname)
        if xname:
            _xvar = _workspace.var(xname)
        if yname:
            _yvar = _workspace.var(yname)
    ## Do we need to update the workspace?
    elif not _workspace or _workspace.GetName() != _wsname:
        _workspace = _file.Get(_wsname)
        if xname:
            _xvar = _workspace.var(xname)
        if yname:
            _yvar = _workspace.var(yname)
    ## Do we need to update the x and y variables?
    else:
        if xname and (not _xvar or _xvar.GetName() != xname):
            _xvar = _workspace.var(xname)
        if yname and (not _yvar or _yvar.GetName() != yname):
            _yvar = _workspace.var(yname)
## end of init()

#------------------------------------------------------------------------------
def getData(sources, getters):
    data = []
    for fname, wsname, snapshot in sources:
        if 'file' in vars() and file.GetName() == fname:
            pass
        else:
            file = ROOT.TFile(fname)
            wspace = None

        if 'wspace' in vars() and wspace and wspace.GetName() == wsname:
            pass
        else:
            wspace = file.Get(wsname)

        wspace.loadSnapshot(snapshot)

        x = []
        for f in getters:
            x.append(f(wspace))

        data.append(x)
    return data
## end of getData


#------------------------------------------------------------------------------
def makeGraph():
    '''Makes a graph using the current workspace and yname.'''
    global _file, _filename, _workspace, _wsname
    global _xvar, xdata, exdata, _yvar, ydata, eydata, graph
    x, ex = array('d', []), array('d', [])
    y, ey = array('d', []), array('d', [])

    for i, (_filename,
            _wsname,
            snapshot) in enumerate(zip(filenames,
                                       wsnames,
                                       snapshots)):
        init()
        _workspace.loadSnapshot(snapshot)

        if xdata:
            x.append(xdata[i])
            ex.append(exdata[i])
        else:
            x.append(_xvar.getVal())
            ex.append(_xvar.getError())

        if ydata:
            y.append(ydata[i])
            ey.append(eydata[i])
        else:
            y.append(_yvar.getVal())
            ey.append(_yvar.getError())
    ## end of loop over graph points

    graph = TGraphErrors(len(x), x, y, ex, ey)
## end of makeGraph()

#------------------------------------------------------------------------------
def plot():
    '''Plots the current graph with appropriate ranges and labels.'''
    n = graph.GetN()

    xmin = min([graph.GetX()[i] - graph.GetEX()[i] for i in range(n)])
    xmax = max([graph.GetX()[i] + graph.GetEX()[i] for i in range(n)])
    dx = xmax - xmin

    ymin = min([graph.GetY()[i] - graph.GetEY()[i] for i in range(n)])
    ymax = max([graph.GetY()[i] + graph.GetEY()[i] for i in range(n)])
    dy = ymax - ymin

    graph.SetTitle(';%s;%s' % (xtitle, ytitle))
    graph.GetXaxis().SetLimits(xmin - 0.1 * dx, xmax + 0.1 * dx)
    graph.GetHistogram().SetMinimum(ymin - 0.1 * dy)
    graph.GetHistogram().SetMaximum(ymax + 0.1 * dy)
    graph.Draw("ap")

    graphs.append(graph)
## end of plot()

#------------------------------------------------------------------------------
def plotlogy():
    '''Plots the current graph with appropriate ranges and labels.'''
    n = graph.GetN()
    ymin = min([graph.GetY()[i] - graph.GetEY()[i] for i in range(n)])
    ymax = max([graph.GetY()[i] + graph.GetEY()[i] for i in range(n)])
    dlogy = math.log(ymax) - math.log(ymin)

    graph.SetTitle(';%s;%s' % (xtitle, ytitle))
    graph.GetXaxis().SetLimits(-0.5, n + 0.5)
    graph.GetHistogram().SetMinimum(ymin / math.exp(0.1 * dlogy))
    graph.GetHistogram().SetMaximum(ymax * math.exp(0.1 * dlogy))
    graph.Draw("ap")

    graphs.append(graph)
## end of plot()

def dump(graph):
    print '         x         ex          y         ey'
    for i in range(graph.GetN()):
        print '%10.3g' % graph.GetX()[i],
        print '%10.3g' % graph.GetEX()[i],
        print '%10.3g' % graph.GetY()[i],
        print '%10.3g' % graph.GetEY()[i]

#------------------------------------------------------------------------------
def main():
    '''Initializes private members and makes and plots the graph.
    Takes configuration from the current values of the customizeable data
    members.'''
    makeGraph()

    if logy:
        plotlogy()
    else:
        plot()

    gPad.Update()
## end of main()


if __name__ == '__main__':

    ## Defaults for customizeable data
    filenames = ('/home/veverka/cmssw/CMSSW_4_2_3/src/JPsi/MuMu/test/escale/'
                 'mc_mmMass85_EB_lowR9_PhoEt12-15.root',) * 8
    wsnames = ('ws1',) * 8

    snapshots = ['sFit_strue_mc_mmMass85_EB_lowR9_PhoEt12-15_gamma_iter%d' % i
                 for i in range(8)]

    xname = None
    xtitle = 'Fit Range Iteration'
    xdata = range(8)
    exdata = [0] * 8

    yname = '#Deltas'
    ytitle = '#Deltas (%)'
    ydata = None
    eydata = None

    labels = ['Barrel', 'R_{9}^{#gamma} < 0.94',
              'E_{T}^{#gamma} #in [10,12] GeV', 'Powheg S4', 'CB']

    main()
    import user
