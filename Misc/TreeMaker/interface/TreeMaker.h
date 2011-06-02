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
// $Id: TreeMaker.h,v 1.2 2011/04/19 09:01:25 veverka Exp $
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
#include "Misc/TreeMaker/interface/PileupBranchManager.h"
#include "Misc/TreeMaker/interface/BranchManager.h"

namespace cit {

  // TreeMaker declaration
  template <typename Collection, typename T = Float_t>
  class TreeMaker : public edm::EDAnalyzer {
  public:
    explicit TreeMaker(const edm::ParameterSet&);
    ~TreeMaker();

  protected:
    virtual void beginJob();
    virtual void analyze(const edm::Event&, const edm::EventSetup&);
    virtual void endJob();

    // ----------member data ---------------------------
    TTree *tree_;
    std::string name_;
    std::string title_;

    /// branch managers
    EventIdBranchManager eventId_;
    PileupBranchManager pileup_;
    BranchManager<Collection, T> vars_;
  //   PmvBranchManager pmv_;
  }; // of TreeMaker class declaration

  // constructors and destructor
  template <typename Collection, typename T>
  TreeMaker<Collection, T>::TreeMaker(const edm::ParameterSet& iConfig) :
    tree_(0),
    name_ ( iConfig.getUntrackedParameter<std::string>( "name", "tree" ) ),
    title_( iConfig.getUntrackedParameter<std::string>( "title",
                                                        "TreeMaker tree" ) ),
    eventId_(iConfig),
    pileup_(iConfig),
    vars_(iConfig)
  //   pmv_( iConfig )
  {
    edm::Service<TFileService> fs;
    // book the tree:
    tree_ = fs->make<TTree>(name_.c_str(), title_.c_str() );

    // initialize branch managers
    eventId_.init( *tree_ );
    pileup_ .init( *tree_ );
    vars_   .init( *tree_ );
  } // end of constructor


  template <typename Collection, typename T>
  TreeMaker<Collection, T>::~TreeMaker()
  { }


  //
  // member functions
  //

  // ------------ method called to for each event  ------------

  template <typename Collection, typename T>
  void
  TreeMaker<Collection, T>::analyze( const edm::Event& iEvent,
                                  const edm::EventSetup& iSetup )
  {
    using namespace edm;

    eventId_.getData( iEvent, iSetup );
    pileup_ .getData( iEvent, iSetup );
    vars_   .getData( iEvent, iSetup );

    tree_->Fill();
  }


  // ------------ method called once each job just before starting event loop  ------------
  template <typename Collection, typename T>
  void
  TreeMaker<Collection, T>::beginJob()
  { }

  // ------------ method called once each job just after ending the event loop  ------------
  template <typename Collection, typename T>
  void
  TreeMaker<Collection, T>::endJob()
  { }


} // end of namespace cit


