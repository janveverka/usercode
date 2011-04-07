#include "Zee/Analysis/interface/ZeeTree.h"

#include <algorithm>
#include <iostream>
#include <vector>
#include <string>
// #include <stdio>

#include "TLorentzVector.h"

#include "CommonTools/UtilAlgos/interface/DeltaR.h"

#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/Math/interface/LorentzVector.h"


ZeeTree::ZeeTree(TTree *tree) :
  ele1_(),
  ele2_(),
  tree_(0x0)
{
  initLeafs();
  if (tree) init(tree);
}


ZeeTree::~ZeeTree() {}

void
ZeeTree::branch(const char *name, Int_t  *address) {
  const char * leafs = (std::string(name) + "/I").c_str();
  printf("tree_->Branch(\"%s\", address, \"%s\");\n", name, leafs);
  std::cout << std::flush;
  tree_->Branch(name, address, leafs);
}

void
ZeeTree::branch(const char *name, Float_t *address) {
  const char * leafs = (std::string(name) + "/F").c_str();
  printf("tree_->Branch(\"%s\", address, \"%s\");\n", name, leafs);
  std::cout << std::flush;
  tree_->Branch(name, address, leafs);
}



void
ZeeTree::branch(const char *name, const char *suffix, Int_t *address) {
  const char * bname = (std::string(name) + suffix).c_str();
  branch(bname, address);
}

void
ZeeTree::branch(const char *name, const char *suffix, Float_t *address) {
  const char * bname = (std::string(name) + suffix).c_str();
  branch(bname, address);
}



void
ZeeTree::branch(const char *name, Int_t *address, const char *size) {
  const char * leafs = (std::string(name) + "[" + size + "]/I").c_str();
  printf("tree_->Branch(\"%s\", address, \"%s\");\n", name, leafs);
  std::cout << std::flush;
  tree_->Branch(name, address, leafs);
}

void
ZeeTree::branch(const char *name, Float_t *address, const char *size) {
  const char * leafs = (std::string(name) + "[" + size + "]/F").c_str();
  printf("tree_->Branch(\"%s\", address, \"%s\");\n", name, leafs);
  std::cout << std::flush;
  tree_->Branch(name, address, leafs);
}



void
ZeeTree::branch(const char *name, const char *suffix, Int_t *address, const char *size) {
  const char * bname = (std::string(name) + suffix).c_str();
  branch(bname, address, size);
}

void
ZeeTree::branch(const char *name, const char *suffix, Float_t * address, const char *size) {
  const char * bname = (std::string(name) + suffix).c_str();
  branch(bname, address, size);
}

void
ZeeTree::branch(const char *name, PtEtaPhi & momentum, const char *size) {
  branch(name, "Pt" , momentum.pt , size);
  branch(name, "Eta", momentum.eta, size);
  branch(name, "Phi", momentum.phi, size);
}


void
ZeeTree::branch(const char *name, XYZ & point, const char *size) {
  branch(name, "X" , point.x, size);
  branch(name, "Y" , point.y, size);
  branch(name, "Z" , point.z, size);
}

void
ZeeTree::branch(const char *name, Particle & particle, const char *size) {
  branch(name, particle.momentum, size);
  branch(name, particle.vertex, size);
  branch(name, "Charge", particle.charge, size);
}

void
ZeeTree::branch(const char *name, Electron & ele, const char *size) {
  branch(name, (Particle &) ele, size);
  branch( (std::string(name) + "Gen").c_str(), ele.gen, size);
  branch(name, "Class", ele.class_, size);
  branch(name, "Brem" , ele.brem  , size);
  branch(name, "Nbrem", ele.nbrem , size);
  branch(name, "ScE"  , ele.scE   , size);
  branch(name, "Fbrem", ele.fbrem , size);
  branch(name, "PinMinusEScOverPin", ele.pinMinusEScOverPin , size);
}

void
ZeeTree::init(TTree *tree) {
  tree_ = tree;
  if (!tree_) return;
  std::cout << "ZeeTree::init: Making branches." << std::endl;
  tree_->Branch("nZees", &nZees_, "nZees/I");
  tree_->Branch("mass", &mass_, "mass[nZees]/F");
  tree_->Branch("massGen", massGen_, "massGen[nZees]/F");
//   branch("nZees", &nZees_);
//   branch("mass" , mass_ , "nZees");
//   branch("massGen", massGen_, "nZees");
  branch("massEfromGenPfromEle", &massEfromGenPfromEle_, "nZees");
  branch("massEfromScPfromEle", massEfromScPfromEle_, "nZees");
  branch("massEfromPhoPfromEle", massEfromPhoPfromEle_, "nZees");
  branch("massEfromPhoPfromPho", massEfromPhoPfromPho_, "nZees");
  branch("massEfromPhoPfromPhoVtxFromEle", massEfromPhoPfromPhoVtxFromEle_, "nZees");
  branch("massEfromPhoPfromEleVtxFromPho", massEfromPhoPfromEleVtxFromPho_, "nZees");
  branch("ele1", ele1_, "nZees");
  branch("ele2", ele2_, "nZees");
} // end ZeeTree::init(..)


void
ZeeTree::initLeafs()
{
  nZees_ = 0;

  // Loop over Zee's
  for (int i=0; i < max_; ++i) {
    mass_[i] = 0;
    massGen_[i] = 0;
    massEfromGenPfromEle_[i] = 0;
    massEfromScPfromEle_[i] = 0;
    massEfromPhoPfromEle_[i] = 0;
    massEfromPhoPfromPho_[i] = 0;
    massEfromPhoPfromPhoVtxFromEle_[i] = 0;
    massEfromPhoPfromEleVtxFromPho_[i] = 0;
  } // End loop over Zee's

} // end ZeeTree::initLeafs()

void
ZeeTree::fill(const reco::CompositeCandidateView &ees,
              const edm::View<pat::Photon> &photons)
{
  // Loop over dielectrons
  for (nZees_ = 0; nZees_ < (int) ees.size(); ++nZees_) {
    const reco::CompositeCandidate ee = ees[nZees_];
    mass_[nZees_] = ee.mass();

    // get the daughters
    pat::Electron const &e1 =
      * ( (const pat::Electron*) ee.daughter(0)->masterClonePtr().get() );
    pat::Electron const &e2 =
      * ( (const pat::Electron*) ee.daughter(1)->masterClonePtr().get() );

    ele1_.set(nZees_, e1);
    ele2_.set(nZees_, e2);

    // energy from SC, momentum from ele
    math::XYZVector
      p3_1 = e1.momentum().unit() * e1.superCluster()->energy(),
      p3_2 = e2.momentum().unit() * e2.superCluster()->energy();
    math::XYZTLorentzVector
      p4_1 ( p3_1.x(), p3_1.y(), p3_1.z(), e1.superCluster()->energy() ),
      p4_2 ( p3_2.x(), p3_2.y(), p3_2.z(), e2.superCluster()->energy() );
    massEfromScPfromEle_[nZees_] = (p4_1 + p4_2).mass();

    // energy from gen, momentum from ele
    if ( e1.genParticle(0) && e2.genParticle(0) ) {
      math::XYZVector
        p3_1 = e1.momentum().unit() * e1.genParticle(0)->energy(),
        p3_2 = e2.momentum().unit() * e2.genParticle(0)->energy();
  
      math::XYZTLorentzVector
        p4_1 ( p3_1.x(), p3_1.y(), p3_1.z(), e1.genParticle(0)->energy() ),
        p4_2 ( p3_2.x(), p3_2.y(), p3_2.z(), e2.genParticle(0)->energy() );
  
      massEfromGenPfromEle_[nZees_] = (p4_1 + p4_2).mass();
    } // end if have gen matches

  } // End loop over dielectrons

  tree_->Fill();
}

