#ifndef Zee_Analysis_ZeeTree_h
#define Zee_Analysis_ZeeTree_h

#include <TTree.h>

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"

class ZeeTree {
public:
  ZeeTree(TTree *tree=0);
  ~ZeeTree();

  const static unsigned char max_ = -1;  // 255

  struct PtEtaPhi {
    Float_t pt [max_];
    Float_t eta[max_];
    Float_t phi[max_];
    PtEtaPhi() {
      // init loop
      for (int i=0; i<max_; ++i) {
        pt [i] = 0;
        eta[i] = 0;
        phi[i] = 0;
      } // end init loop
    } // end constructor
  }; // end struct PtEtaPhi

  struct XYZ {
    Float_t x[max_];
    Float_t y[max_];
    Float_t z[max_];
    XYZ() {
      // init loop
      for (int i=0; i<max_; ++i) {
        x[i] = 0;
        y[i] = 0;
        z[i] = 0;
      } // end init loop
    } // end ctor
  }; // end struct XYZ

  struct Particle {
    PtEtaPhi momentum;
    XYZ      vertex;
    Int_t    charge[max_];
    Particle () : momentum(), vertex() {
      // init loop
      for (int i=0; i<max_; ++i) {
        charge[i] = 0;
      } // end init loop
    } // end ctor
    virtual void
    set (int i, reco::Candidate const& cand) {
      momentum.pt [i] = cand.pt();
      momentum.eta[i] = cand.eta();
      momentum.phi[i] = cand.phi();
      vertex.x[i] = cand.vertex().x();
      vertex.y[i] = cand.vertex().y();
      vertex.z[i] = cand.vertex().z();
      charge[i]   = cand.charge();
    }
    virtual void
    set (int i) {
      momentum.pt [i] = 0;
      momentum.eta[i] = 0;
      momentum.phi[i] = 0;
      vertex.x[i] = 0;
      vertex.y[i] = 0;
      vertex.z[i] = 0;
      charge[i]   = 0;
    }
  }; // end class Particle

  struct Electron : Particle {
    Particle gen;
    Int_t hasGenMatch[max_];
    Int_t   class_[max_];
    Float_t brem  [max_]; // sigmaEtaEta / sigmaPhiPhi
    Int_t   nbrem [max_]; // numberOfBrems
    Float_t scE   [max_];   // super cluster energy
    Float_t fbrem [max_];
    Float_t pinMinusEScOverPin[max_];
    Electron() : Particle(), gen() {
      // init loop
      for (int i=0; i<max_; ++i) {
        hasGenMatch[i] = 0;
        class_[i] = 0;
        brem  [i] = 0;
        nbrem [i] = 0;
        scE   [i] = 0;
        fbrem [i] = 0;
        pinMinusEScOverPin[i] = 0;
      } // end init loop
    } // end ctor
    virtual void
    fill (int i, pat::Electron const& ele) {
      Particle::set(i, ele);
      if ( ele.genParticle(0) ) {
        hasGenMatch[i] = 1;
        gen.set(i, *ele.genParticle(0) );
      } else {
        hasGenMatch[i] = 0;
        gen.set(i);
      }
      class_[i] = ele.classification();
      brem  [i] = ele.userFloat("electronUserData:covEtaEta") /
                  ele.userFloat("electronUserdata:covPhiPhi");
      nbrem [i] = ele.numberOfBrems();
      scE   [i] = ele.superCluster()->energy();
      fbrem [i] = ele.fbrem();
      pinMinusEScOverPin[i] = (ele.pt() - scE[i]) / ele.pt();
    }
  };

  void init(TTree*);
  void fill(reco::CompositeCandidateView const &,
            edm::View<pat::Photon> const &);


  // event leafs
  Int_t nZees_;

  // Zee leafs
  Float_t mass_[max_];
  Float_t massGen_[max_];
  Float_t massEfromGenPfromEle_[max_]; // E from SC, P from ele
  Float_t massEfromScPfromEle_[max_];  // E from SC, P from ele
  Float_t massEfromPhoPfromEle_[max_]; // E from pho, P from pho
  Float_t massEfromPhoPfromPho_[max_]; // E from pho, P from ph
  Float_t massEfromPhoPfromPhoVtxFromEle_[max_]; // E from pho, P from ph
  Float_t massEfromPhoPfromEleVtxFromPho_[max_]; // E from pho, P from ph
  Electron ele1_;
  Electron ele2_;

private:
  TTree *tree_;

  void initLeafs();

  void branch(const char *, Float_t *);
  void branch(const char *, Int_t   *);

  void branch(const char *, const char *, Float_t *);
  void branch(const char *, const char *, Int_t   *);

  void branch(const char *, Float_t *, const char *);
  void branch(const char *, Int_t   *, const char *);

  void branch(const char *, const char *, Float_t *, const char *);
  void branch(const char *, const char *, Int_t   *, const char *);

  void branch(const char *, PtEtaPhi &, const char *);
  void branch(const char *, XYZ      &, const char *);
  void branch(const char *, Particle &, const char *);
  void branch(const char *, Electron &, const char *);
};

#endif