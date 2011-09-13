'''
Facilitates the plotting of variables versus the the fit range iteration.
    Usage: python -i plotScaleVsFitRangeIter.py
'''
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.escale.fitRangeIterationPlotter as frip

canvases.next()
frip.filename = 'test.root'
frip.wsname = 'ws1'
frip.snapshot = 'EB_lowR9_mc_pt10-12_cbShape'
frip.main()

canvases.next()
frip.variable = '#sigma'
frip.ytitle = '#sigma (%)'
frip.main()

canvases.next()
frip.snapshot = 'chi2_EB_lowR9_mc_pt10-12_cbShape'
frip.variable = 'reducedChi2'
frip.ytitle = '#chi2/ndof'
frip.main()

canvases.next()
frip.snapshot = 'chi2_EB_lowR9_mc_pt10-12_cbShape'
frip.variable = 'fitProb'
frip.ytitle = 'P(#chi2)'
frip.main()

if __name__ == '__main__':
    import user
