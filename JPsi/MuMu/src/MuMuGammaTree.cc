#include "JPsi/MuMu/interface/MuMuGammaTree.h"

#include <algorithm>
#include <iostream>
#include <vector>

#include "TLorentzVector.h"

MuMuGammaTree::MuMuGammaTree(TTree *tree):
  DimuonsTree(tree),
  tree_(0x0)
{
  initGammaLeafVariables();
  if (tree) initGamma(tree);
}

MuMuGammaTree::~MuMuGammaTree() {}

void
MuMuGammaTree::initGamma(TTree *tree) {
  tree_ = tree;
  if (!tree_) return;
  std::cout << "MuMuGammaTree::initGamma: Making mmg and pho branches." << std::endl;
  tree_->Branch("nPhotons"           , &nPhotons           , "nPhotons/b"           );
  tree_->Branch("nMuMuGammas"         , &nMuMuGammas         , "nMuMuGammas/b"         );

  tree_->Branch("mmgMass"             , mmgMass             , "mmgMass[nMuMuGammas]/F"             );
  tree_->Branch("mmgDimuon"             , mmgDimuon, "mmgDimuon[nMuMuGammas]/b"             );
  tree_->Branch("mmgPhoton"             , mmgPhoton             , "mmgPhoton[nMuMuGammas]/b"             );
  tree_->Branch("mmgMuonNear"            , mmgMuonNear, "mmgMuonNear[nMuMuGammas]/b"             );
  tree_->Branch("mmgMuonFar"             , mmgMuonFar             , "mmgMuonFar[nMuMuGammas]/b"             );
  tree_->Branch("mmgDeltaRNear"             , mmgDeltaRNear, "mmgDeltaRNear[nMuMuGammas]/F"             );
//   tree_->Branch("mmgDeltaRFar"             , mmgDeltaRFar, "mmgDeltaRFar[nMuMuGammas]/F"             );
//   tree_->Branch("mmgDeltaEta"             , mmgDeltaEta             , "mmgDeltaEta[nMuMuGammas]/F"             );

  tree_->Branch("phoPt"             , phoPt, "phoPt[nPhotons]/F"             );
  tree_->Branch("phoEta"             , phoEta, "phoEta[nPhotons]/F"             );
  tree_->Branch("phoScEta"             , phoScEta, "phoScEta[nPhotons]/F"             );
  tree_->Branch("phoPhi"             , phoPhi, "phoPhi[nPhotons]/F"             );
  tree_->Branch("phoEcalIso"             , phoEcalIso, "phoEcalIso[nPhotons]/F"             );
  tree_->Branch("phoHcalIso"             , phoHcalIso, "phoHcalIso[nPhotons]/F"             );
  tree_->Branch("phoTrackIso"             , phoTrackIso, "phoTrackIso[nPhotons]/F"             );
  tree_->Branch("phoSigmaIetaIeta"             , phoSigmaIetaIeta, "phoSigmaIetaIeta[nPhotons]/F"             );
  tree_->Branch("phoHadronicOverEm"             , phoHadronicOverEm, "phoHadronicOverEm[nPhotons]/F"             );
  tree_->Branch("phoHasPixelSeed", phoHasPixelSeed, "phoHasPixelSeed[nPhotons]/b");
  tree_->Branch("phoSeedRecoFlag", phoSeedRecoFlag, "phoSeedRecoFlag[nPhotons]/I");
  tree_->Branch("phoSeedSeverityLevel", phoSeedSeverityLevel, "phoSeedSeverityLevel[nPhotons]/I");
  tree_->Branch("phoMaxEnergyXtal", phoMaxEnergyXtal, "phoMaxEnergyXtal[nPhotons]/F");
  tree_->Branch("phoE3x3", phoE3x3, "phoE3x3[nPhotons]/F");
  tree_->Branch("phoSeedSwissCross", phoSeedSwissCross, "phoSeedSwissCross[nPhotons]/F");
  tree_->Branch("phoSeedE1OverE9", phoSeedE1OverE9, "phoSeedE1OverE9[nPhotons]/F");
  tree_->Branch("phoGenMatchPdgId", phoGenMatchPdgId, "phoGenMatchPdgId[nPhotons]/I");
  tree_->Branch("phoGenMatchStatus", phoGenMatchPdgId, "phoGenMatchPdgId[nPhotons]/I");
  tree_->Branch("phoGenMatchMomPdgId", phoGenMatchMomPdgId, "phoGenMatchMomPdgId[nPhotons]/I");
  tree_->Branch("phoGenMatchMomStatus", phoGenMatchMomStatus, "phoGenMatchMomStatus[nPhotons]/I");
}

void
MuMuGammaTree::initGammaLeafVariables()
{
  nPhotons = 0;
  nMuMuGammas = 0;

  for (int i=0; i<nDimuons; ++i) {
    mmgMass[i]              = 0;
    mmgDimuon[i]                = 0;
    mmgPhoton[i]               = 0;
    mmgMuonNear[i]               = 0;
    mmgMuonFar[i]               = 0;
    mmgDeltaRNear[i]               = 0;
/*    mmgDeltaRFar[i]               = 0;
    mmgDeltaEta[i]                 = 0;*/
  }

  for (int i=0; i<maxPhotons; ++i) {
    phoPt[i]                      = 0;
    phoEta[i]                      = 0;
    phoScEta[i]                      = 0;
    phoPhi[i]                      = 0;
    phoEcalIso[i]                      = 0;
    phoHcalIso[i]                      = 0;
    phoTrackIso[i]                      = 0;
    phoSigmaIetaIeta[i]                      = 0;
    phoHadronicOverEm[i]                      = 0;
    phoHasPixelSeed[i]                      = 0;
    phoSeedRecoFlag[i]                      = 0;
    phoSeedSeverityLevel[i] = 0;
    phoMaxEnergyXtal[i] = 0;
    phoE3x3[i] = 0;
    phoSeedSwissCross[i] = 0;
    phoSeedE1OverE9[i] = 0;
    phoGenMatchPdgId[i]       = 0;
    phoGenMatchStatus[i]      = 0;
    phoGenMatchMomPdgId[i]    = 0;
    phoGenMatchMomStatus[i]   = 0;

  }
}

