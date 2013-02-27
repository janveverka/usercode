import os
import glob
import ROOT
#import JPsi.MuMu.common.roofit as roo
import JPsi.MuMu.common.canvases as canvases
import JPsi.MuMu.common.cmsstyle as cmsstyle

source_dir = '/mnt/hadoop/user/veverka/MC/DYToMuMu_M_20_FSRFilter_8_TuneZ2star_8TeV_pythia6_GEN_SIM_v2/veverka-Summer12-PU_S7_START52_V9_step3_RAW2DIGI_L1Reco_RECO_PU_v2-90a3c643a4855c1621ba3bfcbef2e742_VecBosV20-5_2_X/Selected'

cuts = [
    'massMuMuGamma + massMuMu < 180',
    'min(Muon1.pt, Muon2.pt) > 10',
    'max(Muon1.pt, Muon2.pt) > 20',
    'massMuMu > 30',
    'abs(massMuMuGamma-90) < 30', # Fit window
    ]

eb_cut = 'abs(Photon.SC.eta) < 1.5'

chain = ROOT.TChain('MuMuGamma')
for source_path in glob.glob(os.path.join(source_dir, '*.root')):
    chain.Add(source_path)
    
chain.Draw('Photon.energy>>hphoe(500,0,500)', '&'.join(cuts), '', 1000)