'''
Toy demonstrating the difference in different ways of pileup (PU) reweighting,
the in-time (IT) and mean reweigthing.

The IT reweighting uses the number of IT PU interactions in MC to match
its spectrum in data.  This way, the reweighted IT PU spectrum in MC matches
data perfectly but the out-of-time (OOT) PU interactions are mismodeled.

The mean reweighting uses the Poisson mean of the IT PU in MC to calculate
the weights to match the Poisson mean of the PU in data.  This way, both
IT and OOT PU spectrum matches the one in data.

USAGE: python -i ootputoy.py

Jan Veverka, Caltech, 15 May 2012
'''
import ROOT
import FWLite.Tools.roofit as roo
import FWLite.Tools.cmsstyle as cmsstyle

import FWLite.Tools.canvases as canvases


#______________________________________________________________________________
def bookhistos():
    '''
    Books all the needed histograms as global variables.
    '''
    global hx, hy, hz, hmean, hxy, hxz, hyz
    hx = ROOT.TH1F('hx', 'IT PU', 101, -0.5, 100.5)
    hy = ROOT.TH1F('hy', 'Early OOT PU', 101, -0.5, 100.5)
    hz = ROOT.TH1F('hz', 'Late OOT PU', 101, -0.5, 100.5)
    hmean = ROOT.TH1F('hmean', 'PU mean', 100, 0, 100)
    hxy = ROOT.TH2F('hxy', 'IT v Early OOT PU', 101, -0.5, 100.5, 101, -0.5, 100.5)
    hxz = ROOT.TH2F('hxz', 'IT v Late OOT PU', 101, -0.5, 100.5, 101, -0.5, 100.5)
    hyz = ROOT.TH2F('hyz', 'Early v Late OOT PU', 101, -0.5, 100.5, 101, -0.5, 100.5)
    
    global hxd, hmeand
    hxd = ROOT.TH1F('hxd', 'PU in real data', 101, -0.5, 100.5)
    hmeand = ROOT.TH1F('hmeand', 'PU mean in real data', 100, 0, 100)
    
    global hxw, hyw, hzw
    hxw = ROOT.TH1F('hxw', 'IT Reweighted IT PU', 101, -0.5, 100.5)
    hyw = ROOT.TH1F('hyw', 'IT Reweighted Early OOT PU', 101, -0.5, 100.5)
    hzw = ROOT.TH1F('hzw', 'IT Reweighted Late OOT PU', 101, -0.5, 100.5)
   
    global hxwm, hywm, hzwm  
    hxwm = ROOT.TH1F('hxwm', 'Mean Reweighted IT PU', 101, -0.5, 100.5)
    hywm = ROOT.TH1F('hywm', 'Mean Reweighted Early OOT PU', 101, -0.5, 100.5)
    hzwm = ROOT.TH1F('hzwm', 'Mean Reweighted Late OOT PU', 101, -0.5, 100.5)
## End of bookhistos().


#______________________________________________________________________________
def generatetoys():
    global toy
    global hx, hy, hz, hmean, hxd, hmeand
    global hxy, hxz, hyz
    toy = []
    for i in range(100000):
        mean = ROOT.gRandom.Uniform(0., 50)
        x = ROOT.gRandom.Poisson(mean)
        y = ROOT.gRandom.Poisson(mean)
        z = ROOT.gRandom.Poisson(mean)
        meand = ROOT.gRandom.Gaus(30, 5)
        xd = ROOT.gRandom.Poisson(meand)
        
        for var, hist in zip([x, y, z, mean, xd, meand], 
                             [hx, hy, hz, hmean, hxd, hmeand]):
            hist.Fill(var)
        
        hxy.Fill(x, y)
        hxz.Fill(x, z)
        hyz.Fill(y, z)
    
        toy.append((mean, x, y, z, meand, xd))
## End of generatetoys()    


#______________________________________________________________________________
def calculateweights():    
    global hw, hwm

    hw = hxd.Clone('hw')
    hw.Divide(hx)
    hw.SetTitle('IT Weight')
    
    hwm = hmeand.Clone('hwm')
    hwm.Divide(hmean)
    hwm.SetTitle('Mean Weight')
## End calculateweights().


#______________________________________________________________________________
def reweighttoys():
    global hxw, hyw, hzw, hxwm, hywm, hzwm
    for (mean, x, y, z, meand, xd) in toy:
        w = hw.GetBinContent(hw.GetXaxis().FindBin(x))
        wm = hwm.GetBinContent(hwm.GetXaxis().FindBin(mean))
        hxw.Fill(x, w)
        hyw.Fill(y, w)
        hzw.Fill(z, w)
        hxwm.Fill(x, wm)
        hywm.Fill(y, wm)
        hzwm.Fill(z, wm)
## End of reweighttoys()


#______________________________________________________________________________
def decoratehistos():
    global hx, hxw, hxwm
    global hy, hyw, hywm
    global hz, hzw, hzwm
    for hists, color in zip([(hx, hxw, hxwm), (hy, hyw, hywm), (hz, hzw, hzwm)], 
                           'Red Blue Green'.split()):
        for hist in hists:
            hist.SetLineColor(getattr(ROOT, 'k' + color))
       
    for hist in [hxw, hxwm]:
        hist.SetLineWidth(2)
        hist.SetLineStyle(2)
## End of decoratehistos()


#______________________________________________________________________________
def drawhistos():
    global hx, hy, hz, hmean, hxd, hmeand, hw, hwm, hxw, hyw, hzw, hxwm 
    global hywm, hzwm, hxy, hxz, hyz

    for hist in [hx, hy, hz, hmean, hxd, hmeand, hw, hwm, hxw, hyw, hzw, hxwm, 
                 hywm, hzwm]:
        canvases.next(hist.GetName())
        hist.Draw()
    
    for hist in [hxy, hxz, hyz]:
        canvases.next(hist.GetName())
        hist.Draw('colz')
    
    canvases.next('ioverlay')
    hxd.Draw()
    hxw.Draw('same')
    hyw.Draw('same')
    hzw.Draw('same')
    
    canvases.next('moverlay')
    hxd.Draw()
    hxwm.Draw('same')
    hywm.Draw('same')
    hzwm.Draw('same')

    canvases.update()
## End of drawhistos()    
   

#______________________________________________________________________________
def main():
    bookhistos()
    generatetoys()
    calculateweights()    
    reweighttoys()
    decoratehistos()
    drawhistos()
## End of main()


#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user
 
