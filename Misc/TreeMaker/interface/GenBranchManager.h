#ifndef Misc_TreeMaker_GenBranchManager_h
#define Misc_TreeMaker_GenBranchManager_h

#include <string>
#include <vector>
#include <TTree.h>
#include <TBranch.h>
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"

class GenBranchManager {
public:
  GenBranchManager(const edm::ParameterSet&);
  ~GenBranchManager();
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
  TBranch * b_MomPdgId_;
  TBranch * b_MomStatus_;
  TBranch * b_GMomPdgId_;
  TBranch * b_GMomStatus_;

  /// leaf variables
  std::vector<Int_t> MomPdgId_;
  std::vector<Int_t> MomStatus_;
  std::vector<Int_t> GMomPdgId_;
  std::vector<Int_t> GMomStatus_;
}; // end of class GenBranchManager declaration

#endif
