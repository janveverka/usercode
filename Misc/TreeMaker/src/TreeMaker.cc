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
// $Id$
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include <string>
#include "TTree.h"
#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include <iostream>
#include <sstream>

const unsigned VECTOR_SIZE = 99;

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
  typedef reco::CandidateView C;
  typedef C typename_C;

  /// data formats
  struct EventIdData {
    UInt_t run, luminosityBlock, event;
    // default constructor
    EventIdData() : run(0), luminosityBlock(0), event(0) {}
    // custom constructor
    EventIdData(const edm::EventID id) :
      run( id.run() ),
      luminosityBlock( id.luminosityBlock() ),
      event( id.event() )
    {}
  }; // end of struct EventIdData definition

  struct Variable {
    std::string tag;
    StringObjectFunction<typename_C::value_type> quantity;
    std::vector<Float_t> data;
    TBranch *branch;
    // default ctor
    Variable(const std::string &iTag,
             const StringObjectFunction<typename_C::value_type> &iQuantity,
             size_t size = VECTOR_SIZE) :
      tag(iTag), quantity(iQuantity), data(size), branch(0) {data.clear();}
    // member methods
    Float_t *address() {return &(data[0]);}
    const char *name() {return tag.c_str();}
    const char *leaflist(const char *size) {
      return (tag + "[" + size + "]/F").c_str();
    }
    void makeBranch(TTree &tree, const char *size) {
      branch = tree.Branch(tag.c_str(),
                           &(data[0]),
                           (tag + "[" + size + "]/F").c_str() );
    }
    void setBranch(TBranch *iBranch) {branch = iBranch;}
    void setBranchAddress() {if (branch != 0) branch->SetAddress( &(data[0]) );}

  }; // end of struct Variable definition

  struct VarCollection {
    std::vector<Variable> variables;
    std::string sizeTag;
    Int_t size;
    // ctor
    VarCollection(std::string tag) : variables(), sizeTag(tag), size(0) {}
    void push_back(Variable var) {variables.push_back(var);}
    void makeBranches(TTree &tree) {
      tree.Branch(sizeTag.c_str(), &size, (sizeTag + "/I").c_str() );
      for (std::vector<Variable>::iterator var = variables.begin();
           var != variables.end(); ++var) {
        var->makeBranch(tree, sizeTag.c_str() );
      } // end of loop over variables
    }
    void fill(const C &collection) {
      size = collection.size();
      for (std::vector<Variable>::iterator
           var = variables.begin(); var != variables.end(); ++var) {
        /// Begin debug
        std::ostringstream dataAddress1(std::ostringstream::out);
        if (var->data.size() > 0)
          dataAddress1 << (Float_t*) &(var->data[0]);
        else
          dataAddress1 << "n/a";
        LogDebug("Fill") << "Before: "
                         << var->branch->GetName() << "["
                         << var->data.size() << "] ->"
                         << (Float_t*) var->branch->GetAddress() << "<- ->"
                         << dataAddress1.str() << "<-"
                         << std::endl;
        /// End debug
        var->data.clear();
        for (typename_C::const_iterator element = collection.begin();
             element != collection.end(); ++element) {
          var->data.push_back( var->quantity(*element) );
        } // end of loop over collection

        /// Begin debug
        std::ostringstream dataAddress2(std::ostringstream::out);
        if (var->data.size() > 0)
          dataAddress2 << (Float_t*) &(var->data[0]);
        else
          dataAddress2 << "n/a";
        LogDebug("Fill") << "After: "
                         << var->branch->GetName() << "["
                         << var->data.size() << "] ->"
                         << (Float_t*) var->branch->GetAddress() << "<- ->"
                         << dataAddress2.str() << "<-"
                         << std::endl;
        /// End debug

        // update the branch addresses
        var->setBranchAddress();

        /// Begin debug
        std::ostringstream dataAddress3(std::ostringstream::out);
        if (var->data.size() > 0)
          dataAddress3 << (Float_t*) &(var->data[0]);
        else
          dataAddress3 << "n/a";
        LogDebug("Fill") << "After setBranchAddress: "
                         << var->branch->GetName() << "["
                         << var->data.size() << "] ->"
                         << (Float_t*) var->branch->GetAddress() << "<- ->"
                         << dataAddress3.str() << "<-"
                         << std::endl;
        /// End debug

      } // end of loop over variables
    } // end of method fill(...)
  };

  TTree *tree_;
  std::string name_;
  std::string title_;
  edm::InputTag src_;
  std::string prefix_;
  bool eventInfo_;
  bool lazyParser_;

  /// leaf variables
  EventIdData id_;
  VarCollection vars_;
}; // of TreeMaker class declaration

// constructors and destructor
TreeMaker::TreeMaker(const edm::ParameterSet& iConfig) :
  tree_(0),
  name_ ( iConfig.getUntrackedParameter<std::string>("name", "tree") ),
  title_( iConfig.getUntrackedParameter<std::string>("title",
                                                     "TreeMaker tree") ),
  src_       ( iConfig.getParameter<edm::InputTag>("src") ),
  prefix_    ( iConfig.getUntrackedParameter<std::string>("prefix", "") ),
  eventInfo_ ( iConfig.getUntrackedParameter<bool>("eventInfo", true) ),
  lazyParser_( iConfig.getUntrackedParameter<bool>("lazyParser", true) ),
  id_(),
  vars_( iConfig.getUntrackedParameter<std::string>("sizeName",
                                                    "n" + prefix_ + "s") )
{
  edm::Service<TFileService> fs;
  // book the tree:
  tree_ = fs->make<TTree>(name_.c_str(), title_.c_str() );

  if (eventInfo_) {
    tree_->Branch("id", &id_, "run/i:luminosityBlock:event");
  }

  typedef std::vector<edm::ParameterSet> VPSet;
  VPSet variables = iConfig.getParameter<VPSet>("variables");
  for (VPSet::const_iterator q = variables.begin(); q != variables.end(); ++q){
    std::string tag = prefix_ + q->getUntrackedParameter<std::string>("tag");

    StringObjectFunction<typename_C::value_type>
    quantity(q->getUntrackedParameter<std::string>("quantity"), lazyParser_);

    vars_.push_back(Variable(tag, quantity) );
  } // end of loop over variables
  vars_.makeBranches(*tree_);
} // end of constructor


TreeMaker::~TreeMaker()
{
//   LogDebug("Processing") << "Entering dtor ..." << std::endl;

  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to for each event  ------------
void
TreeMaker::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;

  id_ = EventIdData( iEvent.id() );

  edm::Handle<C> collection;
  iEvent.getByLabel(src_, collection);

  vars_.fill(*collection);
  tree_->Fill();

  /// Dump the last entry from data
  tree_->Scan("", "", "", 1, tree_->GetEntries()-1);
  for (int i=0; i < vars_.size; ++i) {
    printf("%3d  ", i);
    for (std::vector<Variable>::const_iterator var = vars_.variables.begin();
         var != vars_.variables.end(); ++var) {
      printf("%10f  ", var->data[i]);
    }
    std::cout << std::endl << std::flush;
  }
}


// ------------ method called once each job just before starting event loop  ------------
void
TreeMaker::beginJob() {
  LogDebug("Processing") << "Entering beginJob() ..." << std::endl;
}

// ------------ method called once each job just after ending the event loop  ------------
void
TreeMaker::endJob() {
  LogDebug("Processing") << "Entering endJob() ..." << std::endl;
}

//define this as a plug-in
DEFINE_FWK_MODULE(TreeMaker);
