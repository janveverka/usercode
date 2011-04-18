// -*- C++ -*-
//
// Package:   TreeMaker
// Class:    TreeMaker
//
/**\class TreeMaker TreeMaker.cc Misc/TreeMaker/src/TreeMaker.cc

 Description: [one line class summary]

 Implementation:
    [Notes on implementation]
*/
//
// Original Author:  Jan Veverka
//      Created:  Mon Apr  4 21:25:02 CEST 2011
// $Id: TreeMaker.cc,v 1.8 2011/04/17 22:14:12 veverka Exp $
//
//


// system include files
#include <memory>
#include <string>

#include "TTree.h"

// user include files
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/UtilAlgos/interface/StringCutObjectSelector.h"
#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "DataFormats/Candidate/interface/Candidate.h"
// #include "DataFormats/PatCandidates/interface/Photon.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "Misc/TreeMaker/interface/EventIdBranchManager.h"
#include "Misc/TreeMaker/interface/BranchManager.h"

namespace cit {

  // class declaration
  class TreeMaker : public edm::EDAnalyzer {
  public:
    explicit TreeMaker(const edm::ParameterSet&);
    ~TreeMaker();

  private:
    virtual void beginJob();
    virtual void analyze(const edm::Event&, const edm::EventSetup&);
    virtual void endJob();

    // ----------member data ---------------------------
    typedef reco::CandidateView C;
    typedef C typename_C;

    TTree *tree_;
    std::string name_;
    std::string title_;

    /// leaf variables
    EventIdBranchManager eventId_;
    BranchManager<reco::CandidateView> vars_;
  //   PmvBranchManager pmv_;
  }; // of TreeMaker class declaration

  // constructors and destructor
  TreeMaker::TreeMaker(const edm::ParameterSet& iConfig) :
    tree_(0),
    name_ ( iConfig.getUntrackedParameter<std::string>( "name", "tree" ) ),
    title_( iConfig.getUntrackedParameter<std::string>( "title",
                                                        "TreeMaker tree" ) ),
    eventId_(iConfig),
    vars_(iConfig)
  //   pmv_( iConfig )
  {
    edm::Service<TFileService> fs;
    // book the tree:
    tree_ = fs->make<TTree>(name_.c_str(), title_.c_str() );

    // initialize branch managers
    eventId_.init( *tree_ );
    vars_   .init( *tree_ );
  } // end of constructor


  TreeMaker::~TreeMaker() {
  }


  //
  // member functions
  //

  // ------------ method called to for each event  ------------
  void
  TreeMaker::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
  {
    using namespace edm;

    eventId_.getData(iEvent, iSetup);
    vars_   .getData(iEvent, iSetup);

    tree_->Fill();
  }


  // ------------ method called once each job just before starting event loop  ------------
  void
  TreeMaker::beginJob() {
  }

  // ------------ method called once each job just after ending the event loop  ------------
  void
  TreeMaker::endJob() {
  }


} // end of namespace cit


//define this as a plug-in
using cit::TreeMaker;
DEFINE_FWK_MODULE(TreeMaker);
