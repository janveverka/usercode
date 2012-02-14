'''Provides function cmsstyle that sets the ROOT CMS Style.'''
import os
import ROOT
ROOT.gROOT.LoadMacro(os.path.join(os.environ['CMSSW_BASE'],
                                  'src/FWLite/Tools/test/CMSStyle.C'))
setcmsstyle = ROOT.CMSstyle
print "Setting ROOT's style to CMS Style..."
setcmsstyle()
ROOT.gStyle.SetPalette(1)

