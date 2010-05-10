// -*- C++ -*-
//
// Package:    GenParticlePtSlicer
// Class:      GenParticlePtSlicer
// 
/**\class GenParticlePtSlicer GenParticlePtSlicer.cc Sherpa/GenParticlePtSlicer/src/GenParticlePtSlicer.cc

 Description: Produces a pt ordered slice of shallow clones of the input collection

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Jan Veverka,32 3-A13,+41227677936,
//         Created:  Thu Mar 25 21:03:27 CET 2010
// $Id: GenParticlePtSlicer.cc,v 1.1 2010/03/31 23:23:46 veverka Exp $
//
//


// system include files
#include <memory>
#include <string>
#include <algorithm>

// user include files
#include "CommonTools/Utils/interface/PtComparator.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"


//
// class declaration
//

class GenParticlePtSlicer : public edm::EDProducer {
public:
  explicit GenParticlePtSlicer(const edm::ParameterSet&);
  ~GenParticlePtSlicer();

private:
  virtual void beginJob() ;
  virtual void produce(edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
  
  // ----------member data ---------------------------

  edm::InputTag src_;
  int first_;
  int last_;
  typedef std::vector<reco::GenParticle> GenParticleCollection;
};

//
// constants, enums and typedefs
//


//
// static data member definitions
//

//
// constructors and destructor
//
GenParticlePtSlicer::GenParticlePtSlicer(const edm::ParameterSet& iConfig) :
  src_(iConfig.getParameter<edm::InputTag>("src") ),
  // The slice has the same meaning as the python slice [first:last+1]
  // Note the `+1'!
  // That means that `last' is *included* in the slice.
  // This is to be able to use negative indices. If `last' weren't included
  // it would not be possible to describe the full list by [0:-1] since
  // -1 is the index of the last element.
  first_(iConfig.getUntrackedParameter<int>("first", 0) ),
  last_(iConfig.getUntrackedParameter<int>("last", -1) )
{
   //register products
   produces<GenParticleCollection>();
}


GenParticlePtSlicer::~GenParticlePtSlicer()
{
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
GenParticlePtSlicer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  // retreive the source collection
  Handle<GenParticleCollection> srcCollection;
  iEvent.getByLabel(src_, srcCollection);

  // Create the output collection.
  std::auto_ptr<GenParticleCollection> sortedCollection(new GenParticleCollection);
  sortedCollection->reserve( srcCollection->size() );

  // Loop over the source collection.
  for (GenParticleCollection::const_iterator item = srcCollection->begin();
       item != srcCollection->end(); ++item) {
    // fill the output
    sortedCollection->push_back(*item);
  }

  // Sort by pt.
  GreaterByPt<reco::GenParticle> pTComparator_;
  std::sort(sortedCollection->begin(), sortedCollection->end(), pTComparator_);

  // Do we need to slice it at all?
  if (first_ == 0 && last_ == -1) {
    // No, store the full sorted collection.
    iEvent.put(sortedCollection);
    return;
  }

  // Find the first and last slice element
  GenParticleCollection::const_iterator first, last;
  
  if (abs(first_) < (int) sortedCollection->size()) {
    if (first_ >= 0) {
      first = sortedCollection->begin() + first_;
    } else {
      first = sortedCollection->end() + first_;
    }
  } else {
    // slice will be empty
    first = sortedCollection->end();
  }
  if (abs(last_) < (int) sortedCollection->size()) {
    if (last_ >= 0) {
      last = sortedCollection->begin() + last_;
    } else {
      last = sortedCollection->end() + last_;
    }
  } else {
    // slice will be empty
    last = sortedCollection->begin() - 1;
  }
  ++last;
  
  std::auto_ptr<GenParticleCollection> slice(new GenParticleCollection(last-first) );

  copy(first, last, slice->begin());
  
  // save the output
  iEvent.put(slice);
}

// ------------ method called once each job just before starting event loop  ------------
void GenParticlePtSlicer::beginJob() {}

// ------------ method called once each job just after ending the event loop  ------------
void GenParticlePtSlicer::endJob() {}

//define this as a plug-in
DEFINE_FWK_MODULE(GenParticlePtSlicer);
