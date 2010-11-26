#ifndef JPsi_MuMu_MuMuGammaTree_h
#define JPsi_MuMu_MuMuGammaTree_h

#include <TTree.h>
#include "JPsi/MuMu/interface/DimuonsTree.h"

class MuMuGammaTree : public DimuonsTree {
public:
  MuMuGammaTree(TTree *tree=0);
  ~MuMuGammaTree();
  void initGamma(TTree*);
  void initGammaLeafVariables();

  const static unsigned char maxPhotons = -1;
  const static unsigned char maxMuMuGammas = -1;  // 255

  // event leafs
  Int_t nPhotons;
  Int_t nMuMuGammas;

  // MuMuGamma leafs
  float mmgMass[maxMuMuGammas];
  unsigned char mmgDimuon[maxMuMuGammas];
  unsigned char mmgPhoton[maxMuMuGammas];
  unsigned char mmgMuonNear[maxMuMuGammas];
  unsigned char mmgMuonFar[maxMuMuGammas];
  float mmgDeltaRNear[maxMuMuGammas];

  // photon leafs
  float phoPt[maxPhotons];
  float phoEta[maxPhotons];
  float phoScEta[maxPhotons];
  float phoPhi[maxPhotons];
  float phoEcalIso[maxPhotons];
  float phoHcalIso[maxPhotons];
  float phoTrackIso[maxPhotons];
  float phoSigmaIetaIeta[maxPhotons];
  float phoHadronicOverEm[maxPhotons];
  unsigned char phoHasPixelSeed[maxPhotons];
  int phoSeedRecoFlag[maxPhotons];
  int phoSeedSeverityLevel[maxPhotons];
  float phoMaxEnergyXtal[maxPhotons];
  float phoE3x3[maxPhotons];
  float phoSeedSwissCross[maxPhotons];
  float phoSeedE1OverE9[maxPhotons];
  int phoGenMatchPdgId[maxPhotons];      // 0 means no MC match found
  int phoGenMatchStatus[maxPhotons];     // 0 means no match found
  int phoGenMatchMomPdgId[maxPhotons];   // 0 means no MC match found
  int phoGenMatchMomStatus[maxPhotons];  // 0 means no match found
//   float phoGenPt[maxPhotons];  // 0 means no match found
//   float phoGenEta[maxPhotons];  // 0 means no match found
//   float phoGenPhi[maxPhotons];  // 0 means no match found



private:
  TTree *tree_;
};

#endif