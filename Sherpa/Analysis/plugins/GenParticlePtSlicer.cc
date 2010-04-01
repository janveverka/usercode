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
// $Id$
//
//


// system include files
#include <memory>
#include <string>

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
  src_(iConfig.getParameter<edm::InputTag>("src") )
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

  // create the output collection
  std::auto_ptr<GenParticleCollection> outSlice(new GenParticleCollection);
  outSlice->reserve( srcCollection->size() );

  // loop over the source collection
  for (GenParticleCollection::const_iterator item = srcCollection->begin();
       item != srcCollection->end(); ++item) {
    // fill the output
    outSlice->push_back(*item);
  }
  
  // sort by pt
  GreaterByPt<reco::GenParticle> pTComparator_;
  std::sort(outSlice->begin(), outSlice->end(), pTComparator_);

  // save the output
  iEvent.put(outSlice);
}

// ------------ method called once each job just before starting event loop  ------------
void GenParticlePtSlicer::beginJob() {}

// ------------ method called once each job just after ending the event loop  ------------
void GenParticlePtSlicer::endJob() {}

//define this as a plug-in
DEFINE_FWK_MODULE(GenParticlePtSlicer);
