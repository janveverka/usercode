// -*- C++ -*-
//
// Package:    GenParticleAnalyzer
// Class:      GenParticleAnalyzer
//
/**\class GenParticleAnalyzer GenParticleAnalyzer.cc Sherpa/GenParticleAnalyzer/src/GenParticleAnalyzer.cc

 Description: Analyzer GenParticles from Sherpa

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Jan Veverka,32 3-A13,+41227677936,
//         Created:  Mon Mar 22 05:44:30 CET 2010
// $Id$
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

class GenParticleAnalyzer : public edm::EDAnalyzer {
public:
  explicit GenParticleAnalyzer(const edm::ParameterSet&);
  ~GenParticleAnalyzer();


private:
  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;

  bool isPhoton(int) const;
  bool isLepton(int) const;

  // ----------member data ---------------------------
  // simple map to contain all histograms;
  // histograms are booked in the beginJob()
  // method
  std::map<std::string,TH1F*> histContainer_;
  TH2F* pdgIdAB_;
  // input tags
  edm::InputTag genSrc_;
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
GenParticleAnalyzer::GenParticleAnalyzer(const edm::ParameterSet& iConfig):
  histContainer_(),
  genSrc_(iConfig.getUntrackedParameter<edm::InputTag>("genSrc"))
{
}


GenParticleAnalyzer::~GenParticleAnalyzer()
{
}

//
// member functions
//

bool
GenParticleAnalyzer::isPhoton(int id) const {
  return abs(id) == 22;
}


bool
GenParticleAnalyzer::isLepton(int id) const {
  int absid = abs(id);
  return absid == 11 || absid == 13 || absid == 15;
}

// ------------ method called to for each event  ------------
#include "CommonTools/UtilAlgos/interface/DeltaR.h"
void
GenParticleAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   using namespace reco;
  // get gen. particle collection
  Handle<View<GenParticle> > genParticles;
  iEvent.getByLabel(genSrc_, genParticles);

  // loop over all pairs (a,b)
  for (View<GenParticle>::const_iterator a = genParticles->begin();
       a != genParticles->end()-1; ++a){
    if (a->status() != 3 || !( isPhoton(a->pdgId() ) || isLepton(a->pdgId() ) ) )
      continue;
    for (View<GenParticle>::const_iterator b = a+1;
         b != genParticles->end(); ++b){

      DeltaR<GenParticle> genPartDeltaR;
      histContainer_["deltaR"]->Fill( genPartDeltaR(*a, *b) );

      if (b->status() != 3 || !( isPhoton(b->pdgId() ) || isLepton(b->pdgId() ) ) )
        continue;
      if (a->pdgId() == b->pdgId()) continue;
      if (isLepton(a->pdgId()) && isLepton(b->pdgId())) continue;

      histContainer_["deltaRLeptonPhotonStatus3"]->Fill( genPartDeltaR(*a, *b) );
      histContainer_["deltaRLeptonPhotonStatus3Zoom"]->Fill( genPartDeltaR(*a, *b) );
      histContainer_["statusA"]->Fill(a->status() );
      histContainer_["pdgIdA"]->Fill(a->pdgId() );
      histContainer_["statusB"]->Fill(b->status() );
      histContainer_["pdgIdB"]->Fill(b->pdgId() );
      pdgIdAB_->Fill(a->pdgId(), b->pdgId() );
    }
  }

#ifdef THIS_IS_AN_EVENT_EXAMPLE
   Handle<ExampleData> pIn;
   iEvent.getByLabel("example",pIn);
#endif

#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
#endif
}


// ------------ method called once each job just before starting event loop  ------------
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
void
GenParticleAnalyzer::beginJob()
{
  // register to the TFileService
  edm::Service<TFileService> fs;

  // book histograms:
  histContainer_["deltaR"]=fs->make<TH1F>("deltaR", "deltaR",   100, 0,  20);
  histContainer_["deltaRLeptonPhotonStatus3"]=fs->make<TH1F>("deltaRLeptonPhotonStatus3", "deltaR lepton photon status 3",   100, 0,  10);
  histContainer_["deltaRLeptonPhotonStatus3Zoom"]=fs->make<TH1F>("deltaRLeptonPhotonStatus3Zoom", "deltaR lepton photon status 3",   100, 0,  1);
  histContainer_["statusA"]=fs->make<TH1F>("statusA", "statusA",   10, -.5,  9.5);
  histContainer_["statusB"]=fs->make<TH1F>("statusB", "statusB",   10, -.5,  9.5);
  histContainer_["pdgIdA"]=fs->make<TH1F>("pdgIdA", "pdgIdA",   51, -25.5, 25.5);
  histContainer_["pdgIdB"]=fs->make<TH1F>("pdgIdB", "pdgIdB",   51, -25.5, 25.5);
  pdgIdAB_=fs->make<TH2F>("pdgIdAB", "pdgIdAB",   51, -25.5, 25.5, 51, -25.5, 25.5);

}

// ------------ method called once each job just after ending the event loop  ------------
void
GenParticleAnalyzer::endJob() {
}

//define this as a plug-in
#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(GenParticleAnalyzer);
