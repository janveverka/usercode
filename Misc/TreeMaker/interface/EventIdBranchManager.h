#ifndef MISC_TREEMAKER_EVENTIDBRANCHMANAGER_H
#define MISC_TREEMAKER_EVENTIDBRANCHMANAGER_H

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"

#include "TTree.h"
#include "TBranch.h"

namespace cit {
  class EventIdBranchManager {
    public:
      /// ctor and dtor
      EventIdBranchManager(const edm::ParameterSet &);
      ~EventIdBranchManager(){}
      /// public methods
      void init(TTree &);
      void getData(const edm::Event&, const edm::EventSetup&);
    private:

      /// struct to hold the event ID data
      struct EventIdData {
        /// the data
        UInt_t run, luminosityBlock, event;
        /// default constructor
        EventIdData() : run(0), luminosityBlock(0), event(0) {}
        /// custom constructor
        EventIdData(const edm::EventID id) :
          run            ( id.run()             ),
          luminosityBlock( id.luminosityBlock() ),
          event          ( id.event()           )
        {}
      }; // end of struct EventIdData definition

      bool eventInfo_;
//       bool pileupInfo_;
//       bool doPileupWeight_;
 
      EventIdData id_;
//       edm::InputTag pileupInfoSrc_;
//       edm::ParameterSet pileupReweightingCfg_;
      /// Pile-up info branch
//       UInt_t numPileup_;
//       Float_t puWeight_;
//       Float_t puWeightOOT_;
//       edm::LumiReWeighting LumiWeights_;
  };  // end of class EventIdBranchManager declaration
} // end of namespace cit

#endif
