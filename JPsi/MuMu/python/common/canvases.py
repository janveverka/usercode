'''Facilitates the creation and use of multiple canvases.'''
import ROOT

canvases = []

def next():
    c1 = ROOT.TCanvas()
    i = len( ROOT.gROOT.GetListOfCanvases() )
    c1.SetWindowPosition( 20*i, 20*i )
    canvases.append(c1)

