#ifndef JPsi_MuMu_DimuonsTree_h
#define JPsi_MuMu_DimuonsTree_h

#include <TTree.h>

class DimuonsTree {
public:
  DimuonsTree(TTree *tree=0);
  ~DimuonsTree();
  int Fill();
  void init(TTree*);
  void initLeafVariables();

private:
  const static unsigned char maxMuons = 10;
  const static unsigned char maxDimuons = 45;

public:
  // Leaf variables
  unsigned run;
  unsigned lumi;
  unsigned event;
  unsigned char nDimuons;
  float    mass[maxDimuons];
  float    pt;
  float    eta;
  float    phi;
  float    y;
  float    p;
  int      charge;
  float    vProb;
  float    vrho;
  float    vrhoBS;
  float    vrhoPV;
  float    vx;
  float    vxBS;
  float    vxPV;
  float    vy;
  float    vyBS;
  float    vyPV;
  float    vz;
  float    vzBS;
  float    vzPV;
  float    d0;
  float    d0BS;
  float    d0PV;
  float    dz;
  float    dzBS;
  float    dzPV;
  float    dsz;
  float    dszBS;
  float    dszPV;
  int      pdgId;
  float    backToBack;
  unsigned char dau1[maxDimuons];
  unsigned char dau2[maxDimuons];
  unsigned char nMuons;
  float muPt[maxMuons];
  float    mu1Pt     ;
  float    mu2Pt     ;
  float    mu1Eta    ;
  float    mu2Eta    ;
  float    mu1Phi    ;
  float    mu2Phi    ;
  float    mu1P      ;
  float    mu2P      ;
  int      mu1Charge ;
  int      mu2Charge ;
  float    mu1SiNormalizedChi2;
  float    mu2SiNormalizedChi2;
  float    mu1SiD0   ;
  float    mu2SiD0   ;
  float    mu1SiD0BS ;
  float    mu2SiD0BS ;
  float    mu1SiD0PV ;
  float    mu2SiD0PV ;
  float    mu1SiDz   ;
  float    mu2SiDz   ;
  float    mu1SiDzBS ;
  float    mu2SiDzBS ;
  float    mu1SiDzPV ;
  float    mu2SiDzPV ;
  float    mu1SiDsz  ;
  float    mu2SiDsz  ;
  float    mu1SiDszBS;
  float    mu2SiDszBS;
  float    mu1SiDszPV;
  float    mu2SiDszPV;
  int      mu1SiHits ;
  int      mu2SiHits ;
  int      mu1PixelHits;
  int      mu2PixelHits;
  char     mu1IsGlobalMuon;
  char     mu2IsGlobalMuon;
  char     mu1IsTrackerMuon;
  char     mu2IsTrackerMuon;
  char     mu1IsTMLastStationAngTight;
  char     mu2IsTMLastStationAngTight;
  char     mu1IsTrackerMuonArbitrated;
  char     mu2IsTrackerMuonArbitrated;
  float    mu1TrackIso;
  float    mu2TrackIso;
  float    mu1EcalIso;
  float    mu2EcalIso;
  float    mu1HcalIso;
  float    mu2HcalIso;

private:
  TTree *tree_;
};

#endif