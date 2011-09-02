#ifndef MISC_TREEMAKER_PILEUPBRANCHMANAGER_H
#define MISC_TREEMAKER_PILEUPBRANCHMANAGER_H

#include <vector>
#include "TTree.h"
#include "TBranch.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"


namespace cit {
  class PileupBranchManager {
    public:
      /// ctor and dtor
      PileupBranchManager(const edm::ParameterSet &);
      ~PileupBranchManager(){}
      /// public methods
      void init(TTree &);
      void getData(const edm::Event&, const edm::EventSetup&);
    private:
      void copy(const std::vector<double>&, std::vector<float>& );

      bool doPileupSummaryInfo_;
      bool doWeights_;
      bool doRho_;

      edm::InputTag pileupInfoSrc_;
      edm::InputTag rhoSrc_;
//       edm::ParameterSet pileupReweightingCfg_;

      /// branches
      TBranch * b_numInteractions_;
      TBranch * b_bunchCrossing_;

      /// leaf variables
      Int_t size_;
      std::vector<UInt_t> numInteractions_;
      std::vector<Int_t>  bunchCrossing_;
      Float_t weight_;
      Float_t weightOOT_;
      Float_t rho_;

      /// Tool used to calculate the weights
      edm::LumiReWeighting LumiWeights_;
  };  // end of class PileupBranchManager declaration
} // end of namespace cit

#endif
