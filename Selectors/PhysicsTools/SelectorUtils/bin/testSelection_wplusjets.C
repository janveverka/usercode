#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/FWLite/interface/Event.h"
#include "DataFormats/FWLite/interface/ChainEvent.h"
#include "DataFormats/FWLite/interface/MultiChainEvent.h"
#include "PhysicsTools/SelectorUtils/interface/WPlusJetsEventSelector.h"
#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"
#include "ElectroWeakAnalysis/MultiBosons/bin/MuonHistogrammer.cc"

#include "Math/GenVector/PxPyPzM4D.h"

#include <iostream>
#include <cmath>      //necessary for absolute function fabs()
#include <boost/shared_ptr.hpp>
#include <boost/lexical_cast.hpp>

//Root includes
#include "TROOT.h"
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TSystem.h"

using namespace std;

int main ( int argc, char ** argv )
{

  // load framework libraries
  gSystem->Load( "libFWCoreFWLite" );
  AutoLibraryLoader::enable();

  if ( argc < 2 ) {
    std::cout << "Usage : " << argv[0] << " [parameters.py]" << std::endl;
    return 0;
  }

  // Get the python configuration
  PythonProcessDesc builder(argv[1]);
  edm::ParameterSet const& shyftParameters = builder.processDesc()->getProcessPSet()->getParameter<edm::ParameterSet>("wplusjetsAnalysis");
  edm::ParameterSet const& inputs = builder.processDesc()->getProcessPSet()->getParameter<edm::ParameterSet>("inputs");
  edm::ParameterSet const& outputs = builder.processDesc()->getProcessPSet()->getParameter<edm::ParameterSet>("outputs");
  edm::ParameterSet const& muonHistosAllCfg = builder.processDesc()->getProcessPSet()->getParameter<edm::ParameterSet>("muonHistosAll");
  edm::ParameterSet const& muonHistosSelCfg = builder.processDesc()->getProcessPSet()->getParameter<edm::ParameterSet>("muonHistosSel");

  // book a set of histograms
  fwlite::TFileService fs = fwlite::TFileService( outputs.getParameter<std::string>("outputName") );
  TFileDirectory theDir = fs.mkdir( "histos" );
  theDir.cd();
  TH1F *hMuRelIsoSelected = theDir.make<TH1F>("hMuRelIsoSelected", "selected #mu rel. iso.", 100, 0., 0.1);
  TH1F *hMuRelIsoPassed = theDir.make<TH1F>("hMuRelIsoPassed", "passed #mu rel. iso.", 100, 0., 0.1);

  MuonHistogrammer muonHistosAll(muonHistosAllCfg, fs);
  MuonHistogrammer muonHistosSel(muonHistosSelCfg, fs);

  // This object 'event' is used both to get all information from the
  // event as well as to store histograms, etc.
  fwlite::ChainEvent ev ( inputs.getParameter<std::vector<std::string> > ("fileNames") );

  //cout << "Making event selector" << endl;
  WPlusJetsEventSelector wPlusJets( shyftParameters );
  pat::strbitset ret = wPlusJets.getBitTemplate();

  //loop through each event
  uint record = 0;
  for( ev.toBegin();
       ! ev.atEnd() && record < 200;
       ++ev, ++record)
  {
    if (record % 100 == 0)
      std::cout << "Begin processing record " << record << std::endl;
/*    std::cout << "run: " << ev.id().run()
              << ", event: " << ev.id().event()
              << std::endl;*/
    ret.set(false);

    bool passed = wPlusJets(ev, ret);
    std::vector<reco::ShallowClonePtrCandidate> const & electrons =  wPlusJets.selectedElectrons();
    std::vector<reco::ShallowClonePtrCandidate> const & muons     =  wPlusJets.selectedMuons();
    std::vector<reco::ShallowClonePtrCandidate> const & jets      =  wPlusJets.cleanedJets();
    std::vector<reco::ShallowClonePtrCandidate> const & jetsBeforeClean = wPlusJets.selectedJets();

    string bit_;

    bit_ = "Trigger" ;
    bool passTrigger = ret[ bit_ ];
    bit_ = "== 1 Lepton";
    bool passOneLepton = ret[ bit_ ];
    bit_ = "= 0 Jets";
    // bool jet0 = ret[bit_];
    bit_ = ">=1 Jets";
    bool jet1 = ret[bit_];
    bit_ = ">=2 Jets";
    bool jet2 = ret[bit_];
    bit_ = ">=3 Jets";
    bool jet3 = ret[bit_];
    bit_ = ">=4 Jets";
    bool jet4 = ret[bit_];
    bit_ = ">=5 Jets";
    bool jet5 = ret[bit_];

    bool anyJets = jet1 || jet2 || jet3 || jet4 || jet5;

    if ( anyJets && passOneLepton && passTrigger && 0) {
      cout << "Nele = " << electrons.size() << ", Nmuo = " << muons.size() << ", Njets_all = " << jets.size() << ", Njets_clean = " << jetsBeforeClean.size() << endl;
    }

    // make plots
    // loop over the muons
    for (std::vector<reco::ShallowClonePtrCandidate>::const_iterator muClone = muons.begin();
         muClone != muons.end() && muClone->hasMasterClonePtr(); ++muClone) {
      // get a pat object pointer from an iterator
      reco::CandidatePtr muPtr = muClone->masterClonePtr();
      const pat::Muon * muon = dynamic_cast<const pat::Muon*>( muPtr.get() );

      double hcalIso = muon->hcalIso();
      double ecalIso = muon->ecalIso();
      double trkIso  = muon->trackIso();
      double pt      = muon->pt() ;

      double relIso = (ecalIso + hcalIso + trkIso) / pt;

      hMuRelIsoSelected->Fill(relIso);
      if (passed) hMuRelIsoPassed->Fill(relIso);

    }

    // all muons in the event
//     edm::EventBase const & event = ev;
    muonHistosAll.analyze(ev);
    muonHistosSel.analyze(muons);

  } //end event loop

  //cout << "Printing" << endl;
  wPlusJets.print(std::cout);
  //cout << "We're done!" << endl;

  return 0;
}
