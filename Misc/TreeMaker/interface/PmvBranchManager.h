#ifndef Misc_TreeMaker_PmvBranchManager_h
#define Misc_TreeMaker_PmvBranchManager_h

#include <string>
#include <vector>
#include <TTree.h>
#include <TBranch.h>
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

class PmvBranchManager {
public:
  PmvBranchManager(const edm::ParameterSet&);
  ~PmvBranchManager();
  void init(TTree &);
  void getData(const edm::Event&, const edm::EventSetup&);
private:
  /// input tags
  edm::InputTag src_;
  edm::InputTag genParticleSrc_;
  edm::InputTag primaryVertexSrc_;

  std::string sizeName_;
  bool isMC_;

  /// branches
  TBranch * b_phoMomPdgId_;
  TBranch * b_phoMomStatus_;
  TBranch * b_isFSR_;
  TBranch * b_isISR_;
  TBranch * b_phoIEtaX_;
  TBranch * b_phoIPhiY_;
  TBranch * b_muNearIEtaX_;
  TBranch * b_muNearIPhiY_;
  TBranch * b_muNearIsEB_;
  TBranch * b_muNearIndex_;

  /// leaf variables
  Int_t nVertices_;
  std::vector<Int_t> phoMomPdgId_;
  std::vector<Int_t> phoMomStatus_;
  std::vector<Int_t> isFSR_;
  std::vector<Int_t> isISR_;
  std::vector<Int_t> phoIEtaX_;
  std::vector<Int_t> phoIPhiY_;
  std::vector<Int_t> muNearIEtaX_;
  std::vector<Int_t> muNearIPhiY_;
  std::vector<Int_t> muNearIsEB_;
  std::vector<Int_t> muNearIndex_;

}; // end of class PmvBranchManager declaration

#endif
