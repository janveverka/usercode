#ifndef MISC_TREEMAKER_EVENTIDBRANCHMANAGER_H
#define MISC_TREEMAKER_EVENTIDBRANCHMANAGER_H

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "TTree.h"

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
      EventIdData id_;

  };  // end of class EventIdBranchManager declaration
} // end of namespace cit

#endif