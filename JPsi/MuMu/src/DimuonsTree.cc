#include "JPsi/MuMu/interface/DimuonsTree.h"

DimuonsTree::DimuonsTree(TTree *tree):
  tree_(0x0)
{
  initLeafVariables();
  if (tree) init(tree);
}

DimuonsTree::~DimuonsTree() {}

void DimuonsTree::init(TTree *tree) {
  tree_ = tree;
  if (!tree_) return;
  tree_->Branch("run"       , &run       , "run/i"       );
  tree_->Branch("lumi"      , &lumi      , "lumi/i"      );
  tree_->Branch("event"     , &event     , "event/i"     );
  tree_->Branch("nDimuons", &nDimuons, "nDimuons/b");
  tree_->Branch("mass"      , mass      , "mass[nDimuons]/F"      );
  tree_->Branch("pt"        , &pt        , "pt/F"        );
  tree_->Branch("eta"       , &eta       , "eta/F"       );
  tree_->Branch("phi"       , &phi       , "phi/F"       );
  tree_->Branch("y"         , &y         , "y/F"         );
  tree_->Branch("p"         , &p         , "p/F"         );
  tree_->Branch("charge"    , &charge    , "charge/I"    );
  tree_->Branch("vProb"     , &vProb     , "vProb/F"     );
  tree_->Branch("vrho"      , &vrho      , "vrho/F"      );
  tree_->Branch("vrhoBS"    , &vrhoBS    , "vrhoBS/F"    );
  tree_->Branch("vrhoPV"    , &vrhoPV    , "vrhoPV/F"    );
  tree_->Branch("vx"        , &vx        , "vx/F"        );
  tree_->Branch("vxBS"      , &vxBS      , "vxBS/F"      );
  tree_->Branch("vxPV"      , &vxPV      , "vxPV/F"      );
  tree_->Branch("vy"        , &vy        , "vy/F"        );
  tree_->Branch("vyBS"      , &vyBS      , "vyBS/F"      );
  tree_->Branch("vyPV"      , &vyPV      , "vyPV/F"      );
  tree_->Branch("vz"        , &vz        , "vz/F"        );
  tree_->Branch("vzBS"      , &vzBS      , "vzBS/F"      );
  tree_->Branch("vzPV"      , &vzPV      , "vzPV/F"      );
  tree_->Branch("d0"        , &d0        , "d0/F"        );
  tree_->Branch("d0BS"      , &d0BS      , "d0BS/F"      );
  tree_->Branch("d0PV"      , &d0PV      , "d0PV/F"      );
  tree_->Branch("dz"        , &dz        , "dz/F"        );
  tree_->Branch("dzBS"      , &dzBS      , "dzBS/F"      );
  tree_->Branch("dzPV"      , &dzPV      , "dzPV/F"      );
  tree_->Branch("dsz"       , &dsz       , "dsz/F"       );
  tree_->Branch("dszBS"     , &dszBS     , "dszBS/F"     );
  tree_->Branch("dszPV"     , &dszPV     , "dszPV/F"     );
  tree_->Branch("pdgId"     , &pdgId     , "pdgId/I"     );
  tree_->Branch("backToBack", &backToBack, "backToBack/F");
  tree_->Branch("mu1Pt"                     , &mu1Pt                     , "mu1Pt/F"                     );
  tree_->Branch("mu2Pt"                     , &mu2Pt                     , "mu2Pt/F"                     );
  tree_->Branch("mu1Eta"                    , &mu1Eta                    , "mu1Eta/F"                    );
  tree_->Branch("mu2Eta"                    , &mu2Eta                    , "mu2Eta/F"                    );
  tree_->Branch("mu1Phi"                    , &mu1Phi                    , "mu1Phi/F"                    );
  tree_->Branch("mu2Phi"                    , &mu2Phi                    , "mu2Phi/F"                    );
  tree_->Branch("mu1P"                      , &mu1P                      , "mu1P/F"                      );
  tree_->Branch("mu2P"                      , &mu2P                      , "mu2P/F"                      );
  tree_->Branch("mu1Charge"                 , &mu1Charge                 , "mu1Charge/I"                 );
  tree_->Branch("mu2Charge"                 , &mu2Charge                 , "mu2Charge/I"                 );
  tree_->Branch("mu1SiNormalizedChi2"       , &mu1SiNormalizedChi2       , "mu1SiNormalizedChi2/F"       );
  tree_->Branch("mu2SiNormalizedChi2"       , &mu2SiNormalizedChi2       , "mu2SiNormalizedChi2/F"       );
  tree_->Branch("mu1SiD0"                   , &mu1SiD0                   , "mu1SiD0/F"                   );
  tree_->Branch("mu2SiD0"                   , &mu2SiD0                   , "mu2SiD0/F"                   );
  tree_->Branch("mu1SiD0BS"                 , &mu1SiD0BS                 , "mu1SiD0BS/F"                 );
  tree_->Branch("mu2SiD0BS"                 , &mu2SiD0BS                 , "mu2SiD0BS/F"                 );
  tree_->Branch("mu1SiD0PV"                 , &mu1SiD0PV                 , "mu1SiD0PV/F"                 );
  tree_->Branch("mu2SiD0PV"                 , &mu2SiD0PV                 , "mu2SiD0PV/F"                 );
  tree_->Branch("mu1SiDz"                   , &mu1SiDz                   , "mu1SiDz/F"                   );
  tree_->Branch("mu2SiDz"                   , &mu2SiDz                   , "mu2SiDz/F"                   );
  tree_->Branch("mu1SiDzBS"                 , &mu1SiDzBS                 , "mu1SiDzBS/F"                 );
  tree_->Branch("mu2SiDzBS"                 , &mu2SiDzBS                 , "mu2SiDzBS/F"                 );
  tree_->Branch("mu1SiDzPV"                 , &mu1SiDzPV                 , "mu1SiDzPV/F"                 );
  tree_->Branch("mu2SiDzPV"                 , &mu2SiDzPV                 , "mu2SiDzPV/F"                 );
  tree_->Branch("mu1SiDsz"                  , &mu1SiDsz                  , "mu1SiDsz/F"                  );
  tree_->Branch("mu2SiDsz"                  , &mu2SiDsz                  , "mu2SiDsz/F"                  );
  tree_->Branch("mu1SiDszBS"                , &mu1SiDszBS                , "mu1SiDszBS/F"                );
  tree_->Branch("mu2SiDszBS"                , &mu2SiDszBS                , "mu2SiDszBS/F"                );
  tree_->Branch("mu1SiDszPV"                , &mu1SiDszPV                , "mu1SiDszPV/F"                );
  tree_->Branch("mu2SiDszPV"                , &mu2SiDszPV                , "mu2SiDszPV/F"                );
  tree_->Branch("mu1SiHits"                 , &mu1SiHits                 , "mu1SiHits/I"                 );
  tree_->Branch("mu2SiHits"                 , &mu2SiHits                 , "mu2SiHits/I"                 );
  tree_->Branch("mu1PixelHits"              , &mu1PixelHits              , "mu1PixelHits/I"              );
  tree_->Branch("mu2PixelHits"              , &mu2PixelHits              , "mu2PixelHits/I"              );
  tree_->Branch("mu1IsGlobalMuon"           , &mu1IsGlobalMuon           , "mu1IsGlobalMuon/B"           );
  tree_->Branch("mu2IsGlobalMuon"           , &mu2IsGlobalMuon           , "mu2IsGlobalMuon/B"           );
  tree_->Branch("mu1IsTrackerMuon"          , &mu1IsTrackerMuon          , "mu1IsTrackerMuon/B"          );
  tree_->Branch("mu2IsTrackerMuon"          , &mu2IsTrackerMuon          , "mu2IsTrackerMuon/B"          );
  tree_->Branch("mu1IsTMLastStationAngTight", &mu1IsTMLastStationAngTight, "mu1IsTMLastStationAngTight/B");
  tree_->Branch("mu2IsTMLastStationAngTight", &mu2IsTMLastStationAngTight, "mu2IsTMLastStationAngTight/B");
  tree_->Branch("mu1IsTrackerMuonArbitrated", &mu1IsTrackerMuonArbitrated, "mu1IsTrackerMuonArbitrated/B");
  tree_->Branch("mu2IsTrackerMuonArbitrated", &mu2IsTrackerMuonArbitrated, "mu2IsTrackerMuonArbitrated/B");
  tree_->Branch("mu1TrackIso"               , &mu1TrackIso               , "mu1TrackIso/F"               );
  tree_->Branch("mu2TrackIso"               , &mu2TrackIso               , "mu2TrackIso/F"               );
  tree_->Branch("mu1EcalIso"                , &mu1EcalIso                , "mu1EcalIso/F"                );
  tree_->Branch("mu2EcalIso"                , &mu2EcalIso                , "mu2EcalIso/F"                );
  tree_->Branch("mu1HcalIso"                , &mu1HcalIso                , "mu1HcalIso/F"                );
  tree_->Branch("mu2HcalIso"                , &mu2HcalIso                , "mu2HcalIso/F"                );

}

void DimuonsTree::initLeafVariables()
{
  run        = 0;
  lumi       = 0;
  event      = 0;
  for (int i=0; i<maxDimuons; ++i) {
    mass[i]       = 0;
  }
  pt         = 0;
  eta        = 0;
  phi        = 0;
  y          = 0;
  p          = 0;
  charge     = 0;
  vProb      = 0;
  vrho       = 0;
  vrhoBS     = 0;
  vrhoPV     = 0;
  vx         = 0;
  vxBS       = 0;
  vxPV       = 0;
  vy         = 0;
  vyBS       = 0;
  vyPV       = 0;
  vz         = 0;
  vzBS       = 0;
  vzPV       = 0;
  d0         = 0;
  d0BS       = 0;
  d0PV       = 0;
  dz         = 0;
  dzBS       = 0;
  dzPV       = 0;
  dsz        = 0;
  dszBS      = 0;
  dszPV      = 0;
  pdgId      = 0;
  backToBack = 0;

  mu1Pt                      = 0;
  mu2Pt                      = 0;
  mu1Eta                     = 0;
  mu2Eta                     = 0;
  mu1Phi                     = 0;
  mu2Phi                     = 0;
  mu1P                       = 0;
  mu2P                       = 0;
  mu1Charge                  = 0;
  mu2Charge                  = 0;
  mu1SiNormalizedChi2        = 0;
  mu2SiNormalizedChi2        = 0;
  mu1SiD0                    = 0;
  mu2SiD0                    = 0;
  mu1SiD0BS                  = 0;
  mu2SiD0BS                  = 0;
  mu1SiD0PV                  = 0;
  mu2SiD0PV                  = 0;
  mu1SiDz                    = 0;
  mu2SiDz                    = 0;
  mu1SiDzBS                  = 0;
  mu2SiDzBS                  = 0;
  mu1SiDzPV                  = 0;
  mu2SiDzPV                  = 0;
  mu1SiDsz                   = 0;
  mu2SiDsz                   = 0;
  mu1SiDszBS                 = 0;
  mu2SiDszBS                 = 0;
  mu1SiDszPV                 = 0;
  mu2SiDszPV                 = 0;
  mu1SiHits                  = 0;
  mu2SiHits                  = 0;
  mu1PixelHits               = 0;
  mu2PixelHits               = 0;
  mu1IsGlobalMuon            = 0;
  mu2IsGlobalMuon            = 0;
  mu1IsTrackerMuon           = 0;
  mu2IsTrackerMuon           = 0;
  mu1IsTMLastStationAngTight = 0;
  mu2IsTMLastStationAngTight = 0;
  mu1IsTrackerMuonArbitrated = 0;
  mu2IsTrackerMuonArbitrated = 0;
  mu1TrackIso                = 0;
  mu2TrackIso                = 0;
  mu1EcalIso                 = 0;
  mu2EcalIso                 = 0;
  mu1HcalIso                 = 0;
  mu2HcalIso                 = 0;
}

int DimuonsTree::Fill() {
  return tree_->Fill();
}


