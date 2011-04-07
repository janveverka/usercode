// -*- C++ -*-
//
// Package:    ZeeTreeMaker
// Class:      ZeeTreeMaker
//
/**\class ZeeTreeMaker ZeeTreeMaker.cc Zee/ZeeTreeMaker/src/ZeeTreeMaker.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Jan Veverka
//         Created:  Thu Mar 17 03:19:52 PDT 2011
// $Id$
//
//

// system include files
#include <memory>
#include <iostream>

// root include files
#include "TH1.h"
#include "TMath.h"
#include "TTree.h"

// user include files
#include "CommonTools/CandUtils/interface/AddFourMomenta.h"
#include "CommonTools/UtilAlgos/interface/DeltaR.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CondFormats/DataRecord/interface/EcalChannelStatusRcd.h"
#include "CondFormats/EcalObjects/interface/EcalChannelStatus.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/CaloRecHit/interface/CaloCluster.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"
#include "DataFormats/Candidate/interface/VertexCompositeCandidate.h"
#include "DataFormats/DetId/interface/DetId.h"
#include "DataFormats/EcalDetId/interface/EBDetId.h"
#include "DataFormats/EcalDetId/interface/EEDetId.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/Math/interface/Vector3D.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/EDMException.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalClusterLazyTools.h"
#include "RecoLocalCalo/EcalRecAlgos/interface/EcalSeverityLevelAlgo.h"

#include "Zee/Analysis/interface/ZeeTree.h"

//
// class declaration
//

class ZeeTreeMaker : public edm::EDAnalyzer {
public:
  explicit ZeeTreeMaker(const edm::ParameterSet&);
  ~ZeeTreeMaker();


private:
  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;

  // ----------member data ---------------------------
  ZeeTree eeTree_;
//   ZeeTree ggTree_;

  // input tags
  edm::InputTag photonSrc_;
  edm::InputTag eeSrc_;
  bool isMC_;
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
ZeeTreeMaker::ZeeTreeMaker(const edm::ParameterSet& iConfig) :
  photonSrc_(iConfig.getParameter<edm::InputTag>("photonSrc")),
  eeSrc_(iConfig.getParameter<edm::InputTag>("eeSrc"))
{
   //now do what ever initialization is needed

}


ZeeTreeMaker::~ZeeTreeMaker()
{

   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to for each event  ------------
void
ZeeTreeMaker::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  AddFourMomenta addP4;

  // get collections
  edm::Handle<edm::View<pat::Photon> > photons;
  edm::Handle<reco::CompositeCandidateView> ees;

  iEvent.getByLabel(photonSrc_, photons);
  iEvent.getByLabel(eeSrc_, ees);

  eeTree_.fill(*ees, *photons);

  // TODO: get ggs
//   ggTree_.fill(*ggs);

}


// ------------ method called once each job just before starting event loop  ------------
void
ZeeTreeMaker::beginJob()
{
  // register to the TFileService
  edm::Service<TFileService> fs;

  // book the tree:
  TTree * eeTree = fs->make<TTree>("zee", "Z->ee tree");
//   TTree * ggTree = fs->make<TTree>("zgg", "Z->gg tree");
  eeTree_.init(eeTree);
//   ggTree_.init(tree);
}

// ------------ method called once each job just after ending the event loop  ------------
void
ZeeTreeMaker::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(ZeeTreeMaker);
