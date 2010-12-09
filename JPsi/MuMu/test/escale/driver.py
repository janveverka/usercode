import array
import yurii
from ROOT import *

selection = "abs(eta)<1.5"

scale = []
nll = []
for i in range(201):
    scale.append(-10. + 0.1 * i)
    nll.append( yurii.nll(scale[-1], selection) )

x = array.array("d", scale)
y = array.array("d", nll)
gr = TGraph(len(scale), x, y)
gr.Draw("ap")
gr.GetXaxis().SetTitle("scale [%]")
gr.GetYaxis().SetTitle("- log L")