// -*- C++ -*-
//
// Package:    GenParticleAnalyzer
// Class:      GenParticleAnalyzer
//
/**\class LNGammaAnalyzer LNGammaAnalyzer.cc Sherpa/LNGammaAnalyzer/src/LNGammaAnalyzer.cc

 Description: Analyzer GenParticles from Sherpa

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Jan Veverka,32 3-A13,+41227677936,
//         Created:  Mon Mar 22 05:44:30 CET 2010
// $Id: LNGammaAnalyzer.cc,v 1.1 2010/03/22 21:53:54 veverka Exp $
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

class LNGammaAnalyzer : public edm::EDAnalyzer {
public:
  explicit LNGammaAnalyzer(const edm::ParameterSet&);
  ~LNGammaAnalyzer();


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
  TGraph* lngMass3Vs2_;
  TGraph* lngMt3Vs2_;
  // input tags
  edm::InputTag srcLeptons_;
  edm::InputTag srcNeutrinos_;
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
LNGammaAnalyzer::LNGammaAnalyzer(const edm::ParameterSet& iConfig):
  h1Container_(),
  h2Container_(),
  lngMass3Vs2_(),
  lngMt3Vs2_(),
  srcLeptons_(iConfig.getUntrackedParameter<edm::InputTag>("srcLeptons")),
  srcNeutrinos_(iConfig.getUntrackedParameter<edm::InputTag>("srcNeutrinos")),
  srcPhotons_(iConfig.getUntrackedParameter<edm::InputTag>("srcPhotons"))
{
}


LNGammaAnalyzer::~LNGammaAnalyzer()
{
}

//
// member functions
//

#include "DataFormats/Candidate/interface/CompositeCandidate.h"
#include "CommonTools/CandUtils/interface/AddFourMomenta.h"
// ------------ method called to for each event  ------------
void
LNGammaAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   using namespace reco;
  // get gen. particle collection
  Handle<View<Candidate> > leptons;
  iEvent.getByLabel(srcLeptons_, leptons);

  Handle<View<Candidate> > neutrinos;
  iEvent.getByLabel(srcNeutrinos_, neutrinos);

  Handle<View<Candidate> > photons;
  iEvent.getByLabel(srcPhotons_, photons);

  if (leptons->size() < 1) return;
  if (neutrinos->size() < 1) return;

  // build the ln candidate
  CompositeCandidate ln;
  ln.addDaughter(leptons->at(0), "lepton");
  ln.addDaughter(neutrinos->at(0), "neutrino");
  AddFourMomenta addP4;
  addP4.set(ln);

  // fill the ln histograms
  h1Container_["lnMass"]->Fill(ln.mass() );
  h1Container_["lnMt"]->Fill(ln.mt() );
  h1Container_["lnPt"]->Fill(ln.pt() );
  h1Container_["lnEta"]->Fill(ln.eta() );
  h1Container_["lnPhi"]->Fill(ln.phi() );
  h1Container_["lnY"]->Fill(ln.y() );
  h1Container_["ptRatioLepOverNu"]->Fill(leptons->at(0).pt() / neutrinos->at(0).pt() );

  // build the lngamma candidate
  if (photons->size() < 1) return;
  CompositeCandidate lngamma;
  lngamma.addDaughter(ln, "ln");
  lngamma.addDaughter(photons->at(0), "photon");
  addP4.set(lngamma);

  h1Container_["lngMass"]->Fill(lngamma.mass() );
  h1Container_["lngMt"]->Fill(lngamma.mass() );
  h1Container_["lngPt"]->Fill(lngamma.pt() );
  h1Container_["lngEta"]->Fill(lngamma.eta() );
  h1Container_["lngPhi"]->Fill(lngamma.phi() );
  h1Container_["lngY"]->Fill(lngamma.y() );

  h2Container_["lngMass3Vs2Histo"]->Fill(ln.mass(), lngamma.mass() );
  h2Container_["lngMt3Vs2Histo"]->Fill(ln.mass(), lngamma.mass() );

  // grow the graph by 1000
  static unsigned long eventCount=0;
  unsigned long graphN = lngMass3Vs2_->GetN();
  if (eventCount > graphN) {
    lngMass3Vs2_->Set(graphN+1000);
    lngMt3Vs2_->Set(graphN+1000);
  }

  // insert a point
  lngMass3Vs2_->SetPoint(eventCount, ln.mass(), lngamma.mass() );
  lngMt3Vs2_->SetPoint(eventCount, ln.mt(), lngamma.mt() );
  ++eventCount;


  // fill the zgamma histograms



}

// ------------ method called once each job just before starting event loop  ------------
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
void
LNGammaAnalyzer::beginJob()
{
  // register to the TFileService
  edm::Service<TFileService> fs;

  // book histograms:
  h1Container_["lnMass"]=fs->make<TH1F>("lnMass", "m(l#nu) [GeV/c^{2}]", 200, 0,  200);
  h1Container_["lnMt"]=fs->make<TH1F>("lnMt", "m_{#perp}  (l#nu) [GeV/c^{2}]", 200, 0,  200);
  h1Container_["lnPt"]=fs->make<TH1F>("lnPt", "P_{#perp}   (l#nu) [GeV/c]", 200, 0,  200);
  h1Container_["lnEta"]=fs->make<TH1F>("lnEta", "#eta(l#nu)", 100, -10,  10);
  h1Container_["lnPhi"]=fs->make<TH1F>("lnPhi", "#phi(l#nu)", 100, -4,  4);
  h1Container_["lnY"]=fs->make<TH1F>("lnY", "y(l#nu)", 100, -10,  10);
  h1Container_["ptRatioLepOverNu"]=fs->make<TH1F>("ptRatioLepOverNu", "p_{#perp}  (l) / p_{#perp}  (#nu) [GeV/c^{2}]", 100, 0,  5);
  h1Container_["lngMass"]=fs->make<TH1F>("lngMass", "m(l#nu#gamma) [GeV/c^{2}]", 200, 0,  200);
  h1Container_["lngMt"]=fs->make<TH1F>("lngMt", "m_{#perp}  (l#nu#gamma) [GeV/c^{2}]", 200, 0,  200);
  h1Container_["lngPt"]=fs->make<TH1F>("lngPt", "P_{#perp}   (l#nu#gamma) [GeV/c]", 200, 0,  200);
  h1Container_["lngEta"]=fs->make<TH1F>("lngEta", "#eta(l#nu#gamma)", 100, -10,  10);
  h1Container_["lngPhi"]=fs->make<TH1F>("lngPhi", "#phi(l#nu#gamma)", 100, -4,  4);
  h1Container_["lngY"]=fs->make<TH1F>("lngY", "y(l#nu#gamma) ", 100, -10,  10);
  h2Container_["lngMass3Vs2Histo"]=fs->make<TH2F>("lngMass3Vs2Histo", "m(l#nu#gamma) vs m(l#nu) [GeV/c^{2}]", 250, 0, 250, 250, 0, 250);
  h2Container_["lngMt3Vs2Histo"]=fs->make<TH2F>("lngMt3Vs2Histo", "m_{#perp}  (l#nu#gamma) vs m_{#perp}  (l#nu) [GeV/c^{2}]", 250, 0, 250, 250, 0, 250);
  lngMass3Vs2_=fs->make<TGraph>(); lngMass3Vs2_->SetNameTitle("lngMass3Vs2Graph", "m(l#nu#gamma) vs m(l#nu) [GeV/c^{2}]");
  lngMt3Vs2_=fs->make<TGraph>(); lngMt3Vs2_->SetNameTitle("lngMt3Vs2Graph", "m_{#perp}  (l#nu#gamma) vs m_{#perp}  (l#nu) [GeV/c^{2}]");
}

// ------------ method called once each job just after ending the event loop  ------------
void
LNGammaAnalyzer::endJob() {
}

//define this as a plug-in
#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(LNGammaAnalyzer);
