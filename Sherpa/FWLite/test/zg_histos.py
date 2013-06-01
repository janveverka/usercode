'''
Produce histograms with photon pt after all kinematical cuts on llg and
its daughters. Do this separately for each combination of different
  * sqrt(s) = 7, 8, 13 TeV (name flags: 7, 8 and 13, respectively);
  * h3g = -0.02, 0, 0.02 (name flags m, z and p, respectively); and
  * h4g = -0.0002, 0, 0.0002 (name flags m, z, and p, respectively).
Scale each histogram to the correct XS, number of generated events
and lumi (5 fb-1 for 7TeV, 20 fb-1 for 8 TeV, and 20 fb-1 for 13 TeV).
store 
'''
import ROOT
import array


## Luminosity in inverse femtobarn
luminosity_in_ifb = {'7TeV' : 5,
                     '8TeV' : 5,
                     '13TeV' : 5}

#_______________________________________________________________________________
def main():
    '''
    Main entry point of exectution
    '''
    outfile = ROOT.TFile.Open('test.root', 'recreate')
    for job in getjobs()[:]:
        ifname = '/Users/veverka/Work/Data/sherpa/Trees/zgTree_%s.root' % job
        infile = ROOT.TFile.Open(ifname)
        tree = infile.Get('llgTree/llg')
        outfile.cd()
        histogram = makehistogram(job)
        fillhistogram(tree, histogram)
        histogram2 = histogram.Clone(histogram.GetName() + '2')
        makeLastBinOverflow(histogram)
        scale_bins_by_density(histogram2)
        eventweight = geteventweight(job)
        histogram.Scale(eventweight)
        histogram2.Scale(eventweight)
        infile.Close()
        outfile.Write()
## End of main()        


#_______________________________________________________________________________
def getjobs():
    suffix = {'7TeV': '_v2',
              '8TeV': '',
              '13TeV': '_v2',}
    jobs = []
    for sqrts in [num + 'TeV' for num in '7 8 13'.split()]:
        for h3 in ['h3' + f for f in 'm z p'.split()]:
            for h4 in ['h4' + f for f in 'm z p'.split()]:
                job = '_'.join([sqrts, 'Zgg', h3, h4])
                jobs.append(job + suffix[sqrts])
    return jobs
## End of getjobs()

#_______________________________________________________________________________
def makehistogram(job):
    shortname = getshortname(job)
    binning = array.array('d', [40, 50, 60, 80, 100, 150, 200, 300])
    numbins = len(binning) - 1
    htitle = ', '.join(job.split('_')[:4])
    xtitle = 'Photon E_{T} (GeV)'
    ytitle = 'Events / Bin'
    title = ';'.join([htitle, xtitle, ytitle])
    histogram = ROOT.TH1F(shortname, title, numbins, binning)
    histogram.Sumw2()
    return histogram
## End of makehistogram(...)


#_______________________________________________________________________________
def getshortname(job):
    sqrts, vertex, h3, h4 = job.split('_')[:4] 
    return 'h%s_%02d_%s%s' % (vertex[1], int(sqrts.replace('TeV', '')),
                              h3[2], h4[2])
## End of getshortname()


#_______________________________________________________________________________
def fillhistogram(tree, histogram):
    expression = 'gPt>>%s' % histogram.GetName()
    selection = ' & '.join(['(%s)' % cut for cut in getcuts()])
    tree.Draw(expression, selection, 'goff')
## End of fillhistogram(...)


#_______________________________________________________________________________
def getcuts():
    return [
        'abs(gEta) < 2.5',
        'abs(l1Eta) < 2.5',
        'abs(l2Eta) < 2.5',
        'l1Pt > 20',
        'l2Pt > 20',
        'llMass > 50',
        'minDeltaR > 0.7'
        ]
## End of getcuts


#_______________________________________________________________________________
def makeLastBinOverflow(h):
    '''
    adds the overflow bin to the last bin of a histogram
    '''
    nBins = h.GetNbinsX()
    lastBin = h.GetBinContent(nBins) + h.GetBinContent(nBins+1)
    h.SetBinContent(nBins,lastBin)
    h.SetBinContent(nBins+1,0)
## End of makeLastBinOverlow


#_______________________________________________________________________________
def scale_bins_by_density(histogram, scale = 1):
    histogram.GetYaxis().SetTitle('Events / {scale} GeV'.format(scale=scale))
    for bin in range(1, histogram.GetNbinsX() + 1):
        width = histogram.GetBinWidth(bin)
        content = histogram.GetBinContent(bin)
        error = histogram.GetBinError(bin)
        histogram.SetBinContent(bin, scale * content / width)
        histogram.SetBinError(bin, scale * error / width)
## End of scale_bins_by_density(...)


#_______________________________________________________________________________
def geteventweight(job):
    numevents = 10000.
    sqrts = job.split('_')[0]
    lumi = luminosity_in_ifb[sqrts] # fb-1
    xs = getxs(job) # pb
    return 1e3 * xs * lumi / numevents 
## End of geteventweight(...)


#_______________________________________________________________________________
def getxs(job):
    xsection_in_pb = {
        '7TeV_Zgg_h3m_h4m_v2': 2.84364,
        '7TeV_Zgg_h3m_h4p_v2': 2.63339,
        '7TeV_Zgg_h3m_h4z_v2': 2.52118,
        '7TeV_Zgg_h3p_h4m_v2': 2.6562,
        '7TeV_Zgg_h3p_h4p_v2': 2.82351,
        '7TeV_Zgg_h3p_h4z_v2': 2.52945,
        '7TeV_Zgg_h3z_h4m_v2': 2.65758,
        '7TeV_Zgg_h3z_h4p_v2': 2.71969,
        '7TeV_Zgg_h3z_h4z_v2': 2.53502,
        '8TeV_Zgg_h3m_h4m': 3.88737,
        '8TeV_Zgg_h3m_h4p': 3.47337,
        '8TeV_Zgg_h3m_h4z': 2.99907,
        '8TeV_Zgg_h3p_h4m': 3.42943,
        '8TeV_Zgg_h3p_h4p': 3.8958,
        '8TeV_Zgg_h3p_h4z': 3.05541,
        '8TeV_Zgg_h3z_h4m': 3.67015,
        '8TeV_Zgg_h3z_h4p': 3.63915,
        '8TeV_Zgg_h3z_h4z': 3.09673,
        '13TeV_Zgg_h3m_h4m_v2': 44.4815,
        '13TeV_Zgg_h3m_h4p_v2': 32.7948,
        '13TeV_Zgg_h3m_h4z_v2': 5.97,
        '13TeV_Zgg_h3p_h4m_v2': 32.1486,
        '13TeV_Zgg_h3p_h4p_v2': 41.4024,
        '13TeV_Zgg_h3p_h4z_v2': 6.02107,
        '13TeV_Zgg_h3z_h4m_v2': 38.755,
        '13TeV_Zgg_h3z_h4p_v2': 36.3988,
        '13TeV_Zgg_h3z_h4z_v2': 5.70355,
        }
    return xsection_in_pb[job]
## End of getxs(...)

#_______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user
    
