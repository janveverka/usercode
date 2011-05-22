#include <string>
#include <iostream>

#include "DataFormats/Common/interface/Handle.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

#include "Misc/TreeMaker/interface/EventIdBranchManager.h"

namespace cit {

  EventIdBranchManager::EventIdBranchManager(const edm::ParameterSet& iConfig) :
      eventInfo_( iConfig.getUntrackedParameter<bool>( "eventInfo", true ) ),
      pileupInfo_( iConfig.existsAs<std::string>( "pileupInfoSrc", false ) ),
      pileupInfoSrc_( iConfig.getUntrackedParameter<std::string>( "pileupInfoSrc", "" ) ),
      id_()
  {} // end of ctor definition


  void
  EventIdBranchManager::init(TTree & tree)
  {
    /// Book the branches
    /// Do we want to safe the event ID data?
    if (eventInfo_ == true)
      tree.Branch("id", &id_, "run/i:luminosityBlock:event");

    /// Do we want to store the pile-up info?
    if (pileupInfo_ == true)
      tree.Branch("numPileup", &numPileup_, "numPileup/i");

    std::cout << "pileupInfo_: " << pileupInfo_ << std::endl;
    std::cout << "pileupInfoSrc: " << pileupInfoSrc_ << std::endl;

  } // end of EventIdBranchManager::init(TTree & tree) definition


  void
  EventIdBranchManager::getData( const edm::Event& iEvent,
                                 const edm::EventSetup& iSetup )
  {
    /// Do we want to safe the event ID data?
    if (eventInfo_ == true)
      /// Use the EventIdData ctor to get the event ID data.
      id_ = EventIdData( iEvent.id() );

    /// Do we want to store the pile-up info?
    if (pileupInfo_ == true) {
      edm::Handle<std::vector< PileupSummaryInfo > >  pileupInfo;
      iEvent.getByLabel(pileupInfoSrc_, pileupInfo);
      /// Loop over pileup bunch crossings.
      numPileup_ = 0;
      for(std::vector<PileupSummaryInfo>::const_iterator
          iPileup = pileupInfo->begin();
          iPileup != pileupInfo->end(); ++iPileup) {
  
        numPileup_ += iPileup->getPU_NumInteractions();
      } // end of loop over pileup bunch crossings
    } // end of pileup
  } // end of EventIdBranchManager::getData(...) definition

} // end of namespace cit