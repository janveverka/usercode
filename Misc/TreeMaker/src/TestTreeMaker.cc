// -*- C++ -*-
//
// Package:   TreeMaker
// Class:    TestTreeMaker
//
/**\class TestTreeMaker TestTreeMaker.cc Misc/TreeMaker/src/TestTreeMaker.cc

 Description: Analyzer to produce a tree in the conventional way to test
          if the same result is obtained with the TreeMaker.

 Implementation:
    Create all branches and fill them by-hand.
*/
//
// Original Author:  Jan Veverka
//      Created:  Mon Apr  4 21:25:02 CEST 2011
// $EventIdData$
//
//


// system include files
#include <memory>

#include "TTree.h"

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Candidate/interface/Candidate.h"

const unsigned ncandsMax = 99;

// class declaration
class TestTreeMaker : public edm::EDAnalyzer {
  public:
    explicit TestTreeMaker(const edm::ParameterSet&);
    ~TestTreeMaker();


  private:
    virtual void beginJob() ;
    virtual void analyze(const edm::Event&, const edm::EventSetup&);
    virtual void endJob() ;

    // ----------member data ---------------------------
    /// configuration parameters
    edm::InputTag candSrc_;

    /// tree to be produced
    TTree *tree_;

    /// leaf variables
    struct EventIdData {
      UInt_t run, luminosityBlock, event;
      EventIdData() : run(0), luminosityBlock(0), event(0) {};
      EventIdData(const edm::EventID id) :
        run( id.run() ),
        luminosityBlock( id.luminosityBlock() ),
        event( id.event() )
      {};
    } id_;

    Int_t ncands_;
    Float_t candPt_ [ncandsMax];
    Float_t candEta_[ncandsMax];
    Float_t candPhi_[ncandsMax];
    Float_t candZSide_[ncandsMax];

}; // end of class declaration

/// constructors and destructor
TestTreeMaker::TestTreeMaker(const edm::ParameterSet& iConfig) :
  candSrc_( iConfig.getUntrackedParameter<edm::InputTag>("candSrc") ),
  tree_(0),
  id_()
{
  edm::Service<TFileService> fs;
  // book the tree:
  tree_ = fs->make<TTree>("testTree", "TestTreeMaker tree");
} // end of constructor


TestTreeMaker::~TestTreeMaker()
{

  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)

} // end of destructor


//
// member functions
//

// ------------ method called to for each event  ------------
void
TestTreeMaker::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  id_ = EventIdData( iEvent.id() );

  Handle<reco::CandidateView> cands;
  iEvent.getByLabel(candSrc_, cands);


  /// TODO: Fix neglecting part of the collection for cands->size() > ncandsMax
  for (ncands_ = 0; unsigned(ncands_) < cands->size() &&
                    unsigned(ncands_) < ncandsMax; ++ncands_)
  {
    candPt_ [ncands_] = cands->at(ncands_).pt ();
    candEta_[ncands_] = cands->at(ncands_).eta();
    candPhi_[ncands_] = cands->at(ncands_).phi();
    if ( cands->at(ncands_).eta() > 0 )
      candZSide_[ncands_] = 1;
    else
      candZSide_[ncands_] = -1;
  }

  tree_->Fill();
} // end analyze(...)


// ------------ method called once each job just before starting event loop  ------------
void
TestTreeMaker::beginJob()
{
  tree_->Branch("id", &id_, "run/i:luminosityBlock:event");
  tree_->Branch("ncands", &ncands_, "ncands/I");
  tree_->Branch("candPt" , &candPt_ , "candPt[ncands]/F");
  tree_->Branch("candEta", &candEta_, "candEta[ncands]/F");
  tree_->Branch("candPhi", &candPhi_, "candPhi[ncands]/F");
  tree_->Branch("candZSide" , &candZSide_ , "candZSide[ncands]/F");
}

// ------------ method called once each job just after ending the event loop  ------------
void
TestTreeMaker::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(TestTreeMaker);
