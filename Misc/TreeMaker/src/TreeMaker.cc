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
// $Id: TreeMaker.cc,v 1.6 2011/04/16 13:32:15 veverka Exp $
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

const unsigned VECTOR_SIZE = 99;

namespace jv {

// class declaration
class TreeMaker : public edm::EDAnalyzer {
public:
  explicit TreeMaker(const edm::ParameterSet&);
  ~TreeMaker();

private:
  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;

  // ----------member data ---------------------------
//   typedef pat::PhotonCollection C;
  typedef reco::CandidateView C;
  typedef C typename_C;

  struct SingleBranchManager {
    std::string tag;
    StringObjectFunction<typename_C::value_type> quantity;
    std::vector<Float_t> data;
    TBranch *branch;

    // default ctor
    SingleBranchManager(const std::string &iTag,
                        const StringObjectFunction<typename_C::value_type> &iQuantity,
                        size_t size = VECTOR_SIZE) :
      tag(iTag), quantity(iQuantity), data(size), branch(0) {data.clear();}

    // member methods
    void makeBranch(TTree &tree, const char *size) {
      branch = tree.Branch(tag.c_str(),
                           &(data[0]),
                           (tag + "[" + size + "]/F").c_str() );
    }

    virtual void getData(C const & collection) {
      LogDebug("genParticle") << tag << ": Entering SingleBranchManager::getData(...) ..." << std::flush;
      for (typename_C::const_iterator element = collection.begin();
            element != collection.end(); ++element) {
        data.push_back( quantity(*element) );
      } // end of loop over collection
    }

    void updateBranchAddress() {if (branch != 0) branch->SetAddress( &(data[0]) );}

  }; // end of struct SingleBranchManager definition

  struct ConditionalSingleBranchManager : public SingleBranchManager {
    // data members
    StringCutObjectSelector<typename_C::value_type, true> condition;
    StringObjectFunction<typename_C::value_type> elseQuantity;
    // ctor
    ConditionalSingleBranchManager(
      const std::string &iTag,
      StringCutObjectSelector<typename_C::value_type, true> &iCondition,
      const StringObjectFunction<typename_C::value_type> &iQuantity,
      const StringObjectFunction<typename_C::value_type> &iElseQuantity,
      size_t size = VECTOR_SIZE) :
      SingleBranchManager(iTag, iQuantity, size),
      condition(iCondition),
      elseQuantity(iElseQuantity)
    {} // end of ctor

    void getData(C const & collection) {
      LogDebug("genParticle") << tag << ": Entering ConditionalSingleBranchManager::getData(...) ..." << std::flush;
      for (typename_C::const_iterator element = collection.begin();
            element != collection.end(); ++element) {
        LogDebug("genParticle") << "before if" << std::flush;
        if ( condition(*element) ) {
          LogDebug("genParticle") << "before quantity" << std::flush;
          data.push_back( quantity(*element) );
        } else {
          LogDebug("genParticle") << "before elseQuantity" << std::flush;
          data.push_back( elseQuantity(*element) );
        }
      } // end of loop over collection
    } // end of getData(...) method
  }; // end of struct ConditionalSingleBranchManager

  struct BranchManager {
    // TODO: figure out how to store both SingleBranchManagers
    // and ConditionalSingleBranchManagers in one container.
    // Worth trying: use pure virtual base class BMBase with two specializations
    // SBM and CSBM
    std::vector<SingleBranchManager> variables_;
    std::vector<ConditionalSingleBranchManager> conditionalVariables_;
    std::string sizeTag_;
    Int_t size;

    // ctor
    BranchManager(std::string tag) : variables_(), sizeTag_(tag), size(0) {}

    void push_back(SingleBranchManager var) {variables_.push_back(var);}

    void push_back(ConditionalSingleBranchManager var) {
      conditionalVariables_.push_back(var);
    }

    void makeBranches(TTree &tree) {
      tree.Branch(sizeTag_.c_str(), &size, (sizeTag_ + "/I").c_str() );

      for (std::vector<SingleBranchManager>::iterator var = variables_.begin();
           var != variables_.end(); ++var) {
        var->makeBranch(tree, sizeTag_.c_str() );
      } // end of loop over variables_

      for (std::vector<ConditionalSingleBranchManager>::iterator
           var = conditionalVariables_.begin();
           var != conditionalVariables_.end(); ++var) {
        var->makeBranch(tree, sizeTag_.c_str() );
      } // end of loop over conditionalVariables_

    } // end of makeBranches

    void getData(const C &collection) {
      size = collection.size();

      for (std::vector<SingleBranchManager>::iterator
           var = variables_.begin(); var != variables_.end(); ++var) {
        var->data.clear();
        var->getData(collection);
        var->updateBranchAddress();
      } // end of loop over variables_

      for (std::vector<ConditionalSingleBranchManager>::iterator
           var = conditionalVariables_.begin();
           var != conditionalVariables_.end(); ++var) {
        var->data.clear();
        var->getData(collection);
        var->updateBranchAddress();
      } // end of loop over conditionalVariables_

    } // end of method getData(...)
  }; // end of struc BranchManager

  TTree *tree_;
  std::string name_;
  std::string title_;
  edm::InputTag src_;
  std::string prefix_;
  bool lazyParser_;

  /// leaf variables
  EventIdBranchManager eventId_;
  BranchManager vars_;
//   PmvBranchManager pmv_;
}; // of TreeMaker class declaration

// constructors and destructor
TreeMaker::TreeMaker(const edm::ParameterSet& iConfig) :
  tree_(0),
  name_ ( iConfig.getUntrackedParameter<std::string>("name", "tree") ),
  title_( iConfig.getUntrackedParameter<std::string>("title",
                                                     "TreeMaker tree") ),
  src_       ( iConfig.getParameter<edm::InputTag>("src") ),
  prefix_    ( iConfig.getUntrackedParameter<std::string>("prefix", "") ),
  lazyParser_( iConfig.getUntrackedParameter<bool>("lazyParser", true) ),
  eventId_(iConfig),
  vars_( iConfig.getUntrackedParameter<std::string>("sizeName",
                                                    "n" + prefix_ + "s") )
//   pmv_( iConfig )
{
  edm::Service<TFileService> fs;
  // book the tree:
  tree_ = fs->make<TTree>(name_.c_str(), title_.c_str() );

  eventId_.init( *tree_ );

  typedef std::vector<edm::ParameterSet> VPSet;
  VPSet variables = iConfig.getParameter<VPSet>("variables");
  for (VPSet::const_iterator q = variables.begin(); q != variables.end(); ++q){
    std::string tag = prefix_ + q->getUntrackedParameter<std::string>("tag");

    LogDebug("genParticle") << tag;
    if ( q->existsAs<std::string>("quantity", false) ) {
      LogDebug("genParticle") << "before quantity";
      StringObjectFunction<typename_C::value_type>
      quantity(q->getUntrackedParameter<std::string>("quantity"), lazyParser_);

      vars_.push_back(SingleBranchManager(tag, quantity) );
    } else {
      // expect a conditional quantity
      LogDebug("genParticle") << "before conditional quantity";
      edm::ParameterSet const &
      qConfig = q->getUntrackedParameter<edm::ParameterSet>("quantity");

      StringCutObjectSelector<typename_C::value_type, true>
      condition(
        qConfig.getUntrackedParameter<std::string>("ifCondition"),
        lazyParser_
      );

      StringObjectFunction<typename_C::value_type>
      quantity(
        qConfig.getUntrackedParameter<std::string>("thenQuantity"),
        lazyParser_
      );

      StringObjectFunction<typename_C::value_type>
      elseQuantity(
        qConfig.getUntrackedParameter<std::string>("elseQuantity"),
        lazyParser_
      );

      vars_.push_back(
        ConditionalSingleBranchManager(
          tag, condition, quantity, elseQuantity
        )
      );
    } // end if is a standard or conditional quantity
  } // end of loop over variables
  vars_.makeBranches(*tree_);
} // end of constructor


TreeMaker::~TreeMaker() {
//   LogDebug("Processing") << "Entering dtor ..." << std::endl;
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

  edm::Handle<C> collection;
  iEvent.getByLabel(src_, collection);

  vars_.getData(*collection);
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

//define this as a plug-in
DEFINE_FWK_MODULE(TreeMaker);

} // end of namespace jv
