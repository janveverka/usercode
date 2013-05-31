// -*- C++ -*-
//
// Package:    GenParticleAnalyzer
// Class:      GenParticleAnalyzer
//
/**\class LLGammaAnalyzer LLGammaAnalyzer.cc Sherpa/LLGammaAnalyzer/src/LLGammaAnalyzer.cc

 Description: Analyzer GenParticles from Sherpa

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Jan Veverka,32 3-A13,+41227677936,
//         Created:  Mon Mar 22 05:44:30 CET 2010
// $Id: LLGammaAnalyzer.cc,v 1.1 2010/03/31 23:23:46 veverka Exp $
//
//


// system include files
#include <memory>
#include <map>
#include <string>

#include "TH1.h"
#include "TH2.h"
#include "TGraph.h"

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
//
// class declaration
//

class LLGammaAnalyzer : public edm::EDAnalyzer {
public:
  explicit LLGammaAnalyzer(const edm::ParameterSet&);
  ~LLGammaAnalyzer();


private:
  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;

  // ----------member data ---------------------------
  // simple map to contain all histograms;
  // histograms are booked in the beginJob()
  // method
  std::map<std::string,TH1F*> h1Container_;
  std::map<std::string,TH2F*> h2Container_;
  TGraph* llgMass3Vs2_;
  TGraph* llgMt3Vs2_;
  // input tags
  edm::InputTag srcLeptons_;
  edm::InputTag srcPhotons_;
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
LLGammaAnalyzer::LLGammaAnalyzer(const edm::ParameterSet& iConfig):
  h1Container_(),
  h2Container_(),
  llgMass3Vs2_(),
  llgMt3Vs2_(),
  srcLeptons_(iConfig.getUntrackedParameter<edm::InputTag>("srcLeptons")),
  srcPhotons_(iConfig.getUntrackedParameter<edm::InputTag>("srcPhotons"))
{
}


LLGammaAnalyzer::~LLGammaAnalyzer()
{
}

//
// member functions
//

#include "DataFormats/Candidate/interface/CompositeCandidate.h"
#include "CommonTools/CandUtils/interface/AddFourMomenta.h"
// ------------ method called to for each event  ------------
void
LLGammaAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   using namespace reco;
  // get gen. particle collection
  Handle<View<Candidate> > leptons;
  iEvent.getByLabel(srcLeptons_, leptons);

  Handle<View<Candidate> > photons;
  iEvent.getByLabel(srcPhotons_, photons);

  if (leptons->size() < 2) return;

  // find the leading lepton
  unsigned indexLeading=0, indexTrailing=1;
  if (leptons->at(0).pt() < leptons->at(1).pt() ) {
    indexLeading=1; indexTrailing=0;
  }

  // build the dilepton candidate
  CompositeCandidate dilepton;
  dilepton.addDaughter(leptons->at(indexLeading), "leading");
  dilepton.addDaughter(leptons->at(indexTrailing), "trailing");
  AddFourMomenta addP4;
  addP4.set(dilepton);

  // fill the dilepton histograms
  h1Container_["dileptonMass"]->Fill(dilepton.mass() );
  h1Container_["dileptonMt"]->Fill(dilepton.mt() );
  h1Container_["dileptonPt"]->Fill(dilepton.pt() );
  h1Container_["dileptonEta"]->Fill(dilepton.eta() );
  h1Container_["dileptonPhi"]->Fill(dilepton.phi() );
  h1Container_["dileptonY"]->Fill(dilepton.y() );
  h1Container_["leptonPtRatio1Over0"]->Fill(leptons->at(1).pt() / leptons->at(0).pt() );
  h1Container_["leptonPtRatioTOverL"]->Fill(
    dilepton.daughter("trailing")->pt() / dilepton.daughter("leading")->pt()
  );

  // build the llgamma candidate
  if (photons->size() < 1) return;
  CompositeCandidate llgamma;
  llgamma.addDaughter(dilepton, "dilepton");
  llgamma.addDaughter(photons->at(0), "photon");
  addP4.set(llgamma);

  h1Container_["llgMass"]->Fill(llgamma.mass() );
  h1Container_["llgMt"]->Fill(llgamma.mt() );
  h1Container_["llgPt"]->Fill(llgamma.pt() );
  h1Container_["llgEta"]->Fill(llgamma.eta() );
  h1Container_["llgPhi"]->Fill(llgamma.phi() );
  h1Container_["llgY"]->Fill(llgamma.y() );

  h2Container_["llgMass3Vs2Histo"]->Fill(dilepton.mass(), llgamma.mass() );
  h2Container_["llgMt3Vs2Histo"]->Fill(dilepton.mt(), llgamma.mt() );

  // grow the graph by 1000
  static unsigned long eventCount=0;
  unsigned long graphN = llgMass3Vs2_->GetN();
  if (eventCount > graphN) {
    llgMass3Vs2_->Set(graphN+1000);
    llgMt3Vs2_->Set(graphN+1000);
  }

  // insert a point
  llgMass3Vs2_->SetPoint(eventCount, dilepton.mass(), llgamma.mass() );
  llgMt3Vs2_->SetPoint(eventCount, dilepton.mt(), llgamma.mt() );
  ++eventCount;


  // fill the zgamma histograms



}

// ------------ method called once each job just before starting event loop  ------------
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
void
LLGammaAnalyzer::beginJob()
{
  // register to the TFileService
  edm::Service<TFileService> fs;

  // book histograms:
  h1Container_["dileptonMass"]=fs->make<TH1F>("dileptonMass", "m(l#bar{l}) [GeV/c^{2}]", 200, 0,  200);
  h1Container_["dileptonMt"]=fs->make<TH1F>("dileptonMt", "m_{#perp}  (l#bar{l}) [GeV/c^{2}]", 200, 0,  200);
  h1Container_["dileptonPt"]=fs->make<TH1F>("dileptonPt", "P_{#perp}   (l#bar{l}) [GeV/c]", 200, 0,  200);
  h1Container_["dileptonEta"]=fs->make<TH1F>("dileptonEta", "#eta(l#bar{l})", 100, -10,  10);
  h1Container_["dileptonPhi"]=fs->make<TH1F>("dileptonPhi", "#phi(l#bar{l})", 100, -4,  4);
  h1Container_["dileptonY"]=fs->make<TH1F>("dileptonY", "y(l#bar{l})", 100, -10,  10);
  h1Container_["leptonPtRatio1Over0"]=fs->make<TH1F>("leptonPtRatio1Over0", "lepton p_{#perp}  (1) /p_{#perp}  (0) [GeV/c^{2}]", 100, 0,  5);
  h1Container_["leptonPtRatioTOverL"]=fs->make<TH1F>("leptonPtRatioTOverL", "lepton p_{#perp}  (trailing) /p_{#perp}  (leading) [GeV/c^{2}]", 100, 0,  5);
  h1Container_["llgMass"]=fs->make<TH1F>("llgMass", "m(l#bar{l}#gamma) [GeV/c^{2}]", 200, 0,  500);
  h1Container_["llgMt"]=fs->make<TH1F>("llgMt", "m_{#perp}  (l#bar{l}#gamma) [GeV/c^{2}]", 200, 0,  200);
  h1Container_["llgPt"]=fs->make<TH1F>("llgPt", "P_{#perp}   (l#bar{l}#gamma) [GeV/c]", 200, 0,  200);
  h1Container_["llgEta"]=fs->make<TH1F>("llgEta", "#eta(l#bar{l}#gamma)", 100, -10,  10);
  h1Container_["llgPhi"]=fs->make<TH1F>("llgPhi", "#phi(l#bar{l}#gamma)", 100, -4,  4);
  h1Container_["llgY"]=fs->make<TH1F>("llgY", "y(l#bar{l}#gamma)", 100, -10,  10);
  h2Container_["llgMass3Vs2Histo"]=fs->make<TH2F>("llgMass3Vs2Histo", "m(l#bar{l}#gamma) vs m(l#bar{l})", 250, 0, 250, 250, 0, 500);
  h2Container_["llgMt3Vs2Histo"]=fs->make<TH2F>("llgMt3Vs2Histo", "m_{#perp}  (l#bar{l}#gamma) vs m_{#perp}  (l#bar{l})", 250, 0, 250, 250, 0, 250);
  llgMass3Vs2_=fs->make<TGraph>(); llgMass3Vs2_->SetNameTitle("llgMass3Vs2Graph", "m(l#bar{l}#gamma) vs m(l#bar{l})");
  llgMt3Vs2_=fs->make<TGraph>(); llgMt3Vs2_->SetNameTitle("llgMt3Vs2Graph", "m_{#perp}  (l#bar{l}#gamma) vs m_{#perp}  (l#bar{l})");
}

// ------------ method called once each job just after ending the event loop  ------------
void
LLGammaAnalyzer::endJob() {
}

//define this as a plug-in
#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(LLGammaAnalyzer);
