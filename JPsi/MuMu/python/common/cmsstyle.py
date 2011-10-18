'''Provides function cmsstyle that sets the ROOT CMS Style.'''
import os
import ROOT
ROOT.gROOT.LoadMacro(os.path.join(os.environ['CMSSW_BASE'],
                                  'src/JPsi/MuMu/test/CMSStyle.C'))
cmsstyle = ROOT.CMSstyle
print "Setting ROOT's style to CMS Style..."
cmsstyle()
