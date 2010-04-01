// -*- C++ -*-
//
// Package:    GenParticleAnalyzer
// Class:      GenParticleAnalyzer
//
/**\class DeltaRAnalyzer DeltaRAnalyzer.cc Sherpa/DeltaRAnalyzer/src/DeltaRAnalyzer.cc

 Description: Analyzer GenParticles from Sherpa

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Jan Veverka,32 3-A13,+41227677936,
//         Created:  Mon Mar 22 05:44:30 CET 2010
// $Id: DeltaRAnalyzer.cc,v 1.1 2010/03/22 21:53:54 veverka Exp $
//
//


// system include files
#include <memory>
#include <map>
#include <string>

#include "TH1.h"
#include "TH2.h"

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
//
// class declaration
//

class DeltaRAnalyzer : public edm::EDAnalyzer {
public:
  explicit DeltaRAnalyzer(const edm::ParameterSet&);
  ~DeltaRAnalyzer();


private:
  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;

  // ----------member data ---------------------------
  // simple map to contain all histograms;
  // histograms are booked in the beginJob()
  // method
  std::map<std::string,TH1F*> histContainer_;
  // input tags
  edm::InputTag srcA_;
  edm::InputTag srcB_;
  unsigned histoCount_;
  double min_;
  double max_;
  int nbins_;
  // TODO: add configurable histo min, max, nbins
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
DeltaRAnalyzer::DeltaRAnalyzer(const edm::ParameterSet& iConfig):
  histContainer_(),
  srcA_(iConfig.getUntrackedParameter<edm::InputTag>("srcA")),
  srcB_(iConfig.getUntrackedParameter<edm::InputTag>("srcB")),
  histoCount_(iConfig.getUntrackedParameter<unsigned>("histoCount")),
  min_(iConfig.getUntrackedParameter<double>("min", 0.)),
  max_(iConfig.getUntrackedParameter<double>("max", 10.)),
  nbins_(iConfig.getUntrackedParameter<int>("nbins", 100))
{
}


DeltaRAnalyzer::~DeltaRAnalyzer()
{
}

//
// member functions
//


// ------------ method called to for each event  ------------
#include "CommonTools/UtilAlgos/interface/DeltaR.h"
void
DeltaRAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   using namespace reco;
  // get gen. particle collection
  Handle<View<Candidate> > particlesA;
  iEvent.getByLabel(srcA_, particlesA);

  Handle<View<Candidate> > particlesB;
  iEvent.getByLabel(srcB_, particlesB);

  DeltaR<Candidate> candidateDeltaR;
  std::vector<float> deltaRCollection;
  deltaRCollection.reserve( particlesA->size() * particlesB->size() );

  // loop over all pairs (a,b)
  for (View<Candidate>::const_iterator a = particlesA->begin();
       a != particlesA->end(); ++a){
    for (View<Candidate>::const_iterator b = particlesB->begin();
         b != particlesB->end(); ++b){
      // protect against double counting if you have two identical collections
      if (particlesA.id().id() == particlesB.id().id() && a >= b) continue;
      histContainer_["deltaRAllPairs"]->Fill( candidateDeltaR(*a, *b) );
      deltaRCollection.push_back( candidateDeltaR(*a, *b) );
    }
  }
  sort( deltaRCollection.begin(), deltaRCollection.end() );
  for (unsigned i=0; i < histoCount_ && i < deltaRCollection.size(); ++i) {
    char name[128];
    sprintf(name, "deltaRMin%d", i);
    histContainer_[name]->Fill( deltaRCollection[i] );
  }

}

// ------------ method called once each job just before starting event loop  ------------
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
void
DeltaRAnalyzer::beginJob()
{
  // register to the TFileService
  edm::Service<TFileService> fs;

  // book histograms:
  histContainer_["deltaRAllPairs"]=fs->make<TH1F>("deltaR", "#DeltaR for all pairs", nbins_, min_, max_);
  for (unsigned i=0; i < histoCount_; ++i) {
    char name[128], title[128];
    sprintf(name, "deltaRMin%d", i);
    sprintf(title, "%d. #DeltaR", i+1);
    histContainer_[name]=fs->make<TH1F>(name, title, nbins_, min_, max_);
  }
}

// ------------ method called once each job just after ending the event loop  ------------
void
DeltaRAnalyzer::endJob() {
}

//define this as a plug-in
#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(DeltaRAnalyzer);
