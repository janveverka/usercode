#include "Misc/TreeMaker/interface/EventIdBranchManager.h"

namespace cit {

  EventIdBranchManager::EventIdBranchManager(const edm::ParameterSet& iConfig) :
      eventInfo_ ( iConfig.getUntrackedParameter<bool>("eventInfo", true) ),
      id_()
  {} // end of ctor definition


  void
  EventIdBranchManager::init(TTree & tree)
  {
    /// Do we want to safe the event ID data?
    if (!eventInfo_) return;

    /// Book the branch.
    tree.Branch("id", &id_, "run/i:luminosityBlock:event");
  } // end of EventIdBranchManager::init(TTree & tree) definition


  void
  EventIdBranchManager::getData( const edm::Event& iEvent,
                                 const edm::EventSetup& iSetup )
  {
    /// Do we want to safe the event ID data?
    if (!eventInfo_) return;

    /// Use the EventIdData ctor to get the event ID data.
    id_ = EventIdData( iEvent.id() );
  } // end of EventIdBranchManager::getData(...) definition

} // end of namespace cit