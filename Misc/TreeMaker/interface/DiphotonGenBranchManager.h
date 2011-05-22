#ifndef Misc_TreeMaker_DiphotonGenBranchManager_h
#define Misc_TreeMaker_DiphotonGenBranchManager_h

#include <string>
#include <vector>
#include <TTree.h>
#include <TBranch.h>
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"

class DiphotonGenBranchManager {
public:
  DiphotonGenBranchManager(const edm::ParameterSet&);
  ~DiphotonGenBranchManager();
  void init(TTree &);
  void getData(const edm::Event&, const edm::EventSetup&);
private:
  /// input tags
  edm::InputTag src_;
  edm::InputTag genParticleSrc_;

  std::string sizeName_;
  bool isMC_;
  std::string prefix_;

  /// branches
  TBranch * b_Mom1PdgId_;
  TBranch * b_Mom1Status_;
  TBranch * b_GMom1PdgId_;
  TBranch * b_GMom1Status_;
  TBranch * b_pho1MinDEtaGenEle_;
  TBranch * b_pho1MinDPhiGenEle_;
  TBranch * b_pho1GenElePt_;
  TBranch * b_pho1GenEleCharge_;

  TBranch * b_Mom2PdgId_;
  TBranch * b_Mom2Status_;
  TBranch * b_GMom2PdgId_;
  TBranch * b_GMom2Status_;
  TBranch * b_pho2MinDEtaGenEle_;
  TBranch * b_pho2MinDPhiGenEle_;
  TBranch * b_pho2GenElePt_;
  TBranch * b_pho2GenEleCharge_;

  /// leaf variables
  std::vector<Int_t> Mom1PdgId_;
  std::vector<Int_t> Mom1Status_;
  std::vector<Int_t> GMom1PdgId_;
  std::vector<Int_t> GMom1Status_;
  std::vector<Float_t> pho1MinDEtaGenEle_;
  std::vector<Float_t> pho1MinDPhiGenEle_;
  std::vector<Float_t> pho1GenElePt_;
  std::vector<Int_t> pho1GenEleCharge_;

  std::vector<Int_t> Mom2PdgId_;
  std::vector<Int_t> Mom2Status_;
  std::vector<Int_t> GMom2PdgId_;
  std::vector<Int_t> GMom2Status_;
  std::vector<Float_t> pho2MinDEtaGenEle_;
  std::vector<Float_t> pho2MinDPhiGenEle_;
  std::vector<Float_t> pho2GenElePt_;
  std::vector<Int_t> pho2GenEleCharge_;
}; // end of class DiphotonGenBranchManager declaration

#endif
