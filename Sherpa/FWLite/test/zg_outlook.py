import ROOT
import JPsi.MuMu.common.canvases as canvases

ifname = 'test.root'
infile = ROOT.TFile.Open(ifname)


#_______________________________________________________________________________
def main():
    print 'Sensitivity with respect to 7 TeV is greater by a factor of (4x lumi):'
    doh3()
    doh4()

#_______________________________________________________________________________
def doh3():
    h07 = infile.Get('hg_07_pz')
    h07.Add(infile.Get('hg_07_mz'))
    h07.Scale(0.5)

    h08 = infile.Get('hg_08_pz')
    h08.Add(infile.Get('hg_08_mz'))
    h08.Scale(0.5)
    h08.SetLineColor(ROOT.kBlue)

    h13 = infile.Get('hg_13_pz')
    h13.Add(infile.Get('hg_13_mz'))
    h13.Scale(0.5)
    h13.SetLineColor(ROOT.kRed)

    h13o07 = h13.Clone('h3_sqrts13o7')
    h13o07.Divide(h07)
    h08o07 = h08.Clone('h3_sqrts08o7')
    h08o07.Divide(h07)

    canvases.next('h3')
    h13.Draw()
    h08.Draw('same')
    h07.Draw('same')

    canvases.next('h3_13o7')
    h13o07.Draw()

    canvases.next('h3_08o7')
    h08o07.Draw()

    canvases.update()

    print '%.2g for h3g @  8 TeV' % getsensitivity(h08o07)
    print '%.2g for h3g @ 13 TeV' % getsensitivity(h13o07)

#_______________________________________________________________________________
def doh4():
    h07 = infile.Get('hg_07_zp')
    h07.Add(infile.Get('hg_07_zm'))
    h07.Scale(0.5)

    h08 = infile.Get('hg_08_zp')
    h08.Add(infile.Get('hg_08_zm'))
    h08.Scale(0.5)
    h08.SetLineColor(ROOT.kBlue)

    h13 = infile.Get('hg_13_zp')
    h13.Add(infile.Get('hg_13_zm'))
    h13.Scale(0.5)
    h13.SetLineColor(ROOT.kRed)

    h13o07 = h13.Clone('h4_sqrts13o7')
    h13o07.Divide(h07)
    h08o07 = h08.Clone('h4_sqrts08o7')
    h08o07.Divide(h07)

    canvases.next('h4')
    h13.Draw()
    h08.Draw('same')
    h07.Draw('same')

    canvases.next('h4_13o7')
    h13o07.Draw()

    canvases.next('h4_08o7')
    h08o07.Draw()

    canvases.update()

    print '%.2g for h4g @  8 TeV' % getsensitivity(h08o07)
    print '%.2g for h4g @ 13 TeV' % getsensitivity(h13o07)


#_______________________________________________________________________________
def getsensitivity(h):
    '''
    Assume all sensitivity comes from the last bin.
    It scale as a sqrt of the ratio of xs at different energies because
    of the quadratic dependence of xs on h3 and h4.
    Sensitivity scales with root 4 of the luminosity ratios.
    '''
    return ROOT.TMath.Sqrt(h.GetBinContent(h.GetNbinsX())) * pow(4., 0.25)


#_______________________________________________________________________________
if __name__ == '__main__':
    main()
