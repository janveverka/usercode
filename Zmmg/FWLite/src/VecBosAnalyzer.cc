/**
 * Implementation of the VecBosAnalyzer class.
 * 
 * Jan Veverka, Caltech, 12 June 2012.
 */

#include <iostream>
#include "TChain.h"
#include "TDirectory.h"
#include "TH1F.h"
#include "TMath.h"
#include "TTree.h"
#include "DataFormats/Provenance/interface/LuminosityBlockRange.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "Zmmg/FWLite/interface/VecBosAnalyzer.h"

using cit::VecBosAnalyzer;
using cit::VecBosTree;
using namespace std;
//_____________________________________________________________________________
/**
 * Constructor
 */
VecBosAnalyzer::VecBosAnalyzer(
  boost::shared_ptr<edm::ParameterSet> cfg
) :
  cfg_(cfg),
  tree_(0),
  output_(0),
  maxEventsInput_(-1)
{
  init();
} // ctor


//_____________________________________________________________________________
/**
 * Destructor
 */
VecBosAnalyzer::~VecBosAnalyzer()
{
  if (tree_ != 0) {
    TTree *chain = tree_->fChain;
    delete tree_;
    if (chain != 0) {
      delete chain;
    }
  }
  
  if (output_ != 0) {
    output_->Close();
    delete output_;
  }
} // dtor


//_____________________________________________________________________________
/**
 * Run the analysis.
 */
void
VecBosAnalyzer::run()
{
  // Make sure we have a tree connected.
  if (tree_->fChain == 0) return;

  // Get the number of events to loop over.
  Long64_t maxEntry = tree_->fChain->GetEntriesFast();
  if (0 <= maxEventsInput_ && maxEventsInput_ < maxEntry) {
    maxEntry = maxEventsInput_;
  }

  // Loop over the events.
  Long64_t ientry=0;
  for (; ientry < maxEntry; ientry++) {
    if (tree_->LoadTree(ientry) < 0) break;
    if (ientry % reportEvery_ == 0) reportEvent(ientry);
    tree_->fChain->GetEntry(ientry);
    // if (pass(ientry) == false) continue;
    fillHistograms();
  } // end of loop over the events
  
  cout << "Processed " << ientry << " records." << endl;
  cout << "Writing " << output_->GetName() << "." << endl;
  output_->Write();
  
} // run


//_____________________________________________________________________________
/**
 * Parses the configuration and sets the corresponding data members.
 */
void
VecBosAnalyzer::parseConfiguration()
{
  parseInputs();
  parseOutputs();

  if (cfg_->existsAs<PSet>("maxEvents")) {
    PSet const& maxEvents = cfg_->getParameter<PSet>("maxEvents");
    maxEventsInput_ = maxEvents.getUntrackedParameter<Long64_t>("input", -1);
    reportEvery_ = maxEvents.getUntrackedParameter<Long64_t>("reportEvery", 1);
  } // exists maxEvents
  
} // parseConfiguration


//_____________________________________________________________________________
/**
 * Parses the configuration and sets the inputs.
 */
void
VecBosAnalyzer::parseInputs()
{
  PSet const& inputs = cfg_->getParameter<PSet>("inputs");

  typedef vector<string> vstring;
  vstring filesToProcess;

//   typedef vector<edm::LuminosityBlockRange> Lumis;
//   map<string,Lumis*> filesToLumis;
//   vector<Lumis*> lumisToProcess;
  
  // Process differently depending on if we are fed a list of files or 
  // a list of files with associated LumiBlocks
  if (inputs.existsAs<vstring>("fileNames")) {
    // No need to worry about the luminosity blocks
    filesToProcess = inputs.getParameter<vstring>("fileNames");
  /*********************************************************************  
  } else if(inputs.existsAs<vector<edm::ParameterSet> >("fileNames")) {    
    vector<edm::ParameterSet> files(
      inputs.getParameter<vector<edm::ParameterSet> >("fileNames")
      );
    // Iterate over the files
    for (vector<edm::ParameterSet>::const_iterator c = files.begin();
         c != files.end(); ++c) {           
        // make map of file names to lumiblock sets
        Lumis const &templumisref = c->getParameter<Lumis>("lumisToProcess");
        lumisToProcess.push_back(new Lumis());
        lumisToProcess.back()->resize(templumisref.size());
        copy(templumisref.begin(), templumisref.end(),
             lumisToProcess.back()->begin());

        vector<string> fileNames = c->getParameter<vector<string> >("fileNames");
        filesToProcess.reserve(filesToProcess.size()+fileNames.size());
        filesToProcess.insert(filesToProcess.end(),fileNames.begin(),fileNames.end());  

        for (vector<string>::const_iterator f = fileNames.begin(); f != fileNames.end(); ++f)
          filesToLumis[*f] = lumisToProcess.back();
      }
  ****************************************************************************/
  } else {
    throw cms::Exception("InvalidInput") << "fileNames must be of type "
                                         << "vstring or VPSet!" << endl;
  }

  TChain *chain = new TChain("ntp1");
  for (vstring::const_iterator filename = filesToProcess.begin();
       filename != filesToProcess.end(); ++filename) {
    chain->Add(filename->c_str());
  }
  
  tree_ = new VecBosTree(chain);  
} // parseInputs


//_____________________________________________________________________________
/**
 * Parses the output configuration and opens the output file.
 */
void
VecBosAnalyzer::parseOutputs()
{
  PSet const& outputs = cfg_->getParameter<PSet>("outputs");
  string const& outputName = outputs.getParameter<string>("outputName");
  output_ = new TFile(outputName.c_str(), "recreate");
} // parseConfiguration


//_____________________________________________________________________________
/**
 * Sets the status of the unused branches to 0 to save time.
 */
void
VecBosAnalyzer::setBranchesStatus()
{
  TTree *chain = tree_->fChain;
  chain->SetBranchStatus("*", 0);  // disable all branches  
  chain->SetBranchStatus("nPU", 1);
  chain->SetBranchStatus("nPV", 1);
  
  chain->SetBranchStatus("nPho", 1);
  chain->SetBranchStatus("energyPho", 1);
  chain->SetBranchStatus("etaPho", 1);
  chain->SetBranchStatus("phiPho", 1);
  
  chain->SetBranchStatus("nMuon", 1);
  chain->SetBranchStatus("etaMuon", 1);
  chain->SetBranchStatus("energyMuon", 1);
  chain->SetBranchStatus("phiMuon", 1);
} // setBranchesStatus


//_____________________________________________________________________________
/**
 * Books the histograms to be filled.
 */
void
VecBosAnalyzer::bookHistograms()
{
  TDirectory *cwd = gDirectory;
  output_->cd();  
  
  histos_["nPU0"] = new TH1F(
    "nPU0", "Early OOT Pileup;True number of interactions;Events", 
    101, -0.5, 100.5
  );
  
  histos_["nPU1"] = new TH1F(
    "nPU1", "In-Time Pileup;True number of interactions;Events", 
    101, -0.5, 100.5
  );
  
  histos_["nPU2"] = new TH1F(
    "nPU2", "Late OOT Pileup;True number of interactions;Events", 
    101, -0.5, 100.5
  );
  
  histos_["nPV"] = new TH1F(
    "nPV", "Reconstructed Primary Vertices;Number of Vertices;Events", 
    101, -0.5, 100.5
  );
  
  histos_["nPho"] = new TH1F("nPho", "Photon;Multiplicity;Events", 
                             101, -0.5, 100.5);  
  histos_["ptPho"] = new TH1F("ptPho", "Photon;pt;Events", 101, -0.5, 100.5);
  histos_["etaPho"] = new TH1F("etaPho", "Photon;#eta;Events", 100, -3, 3);
  histos_["phiPho"] = new TH1F("phiPho", "Photon;#phi;Events", 
                               100, -TMath::Pi(), TMath::Pi());
  
  histos_["nMuon"] = new TH1F("nMuon", "Muon;Multiplicity;Events", 
                              101, -0.5, 100.5);
  histos_["ptMuon"] = new TH1F("ptMuon", "Muon;pt;Events", 100, -0.5, 100.5);
  histos_["etaMuon"] = new TH1F("etaMuon", "Muon;#eta;Events", 100, -3, 3);
  histos_["phiMuon"] = new TH1F("phiMuon", "Muon;#phi;Events", 
                                100, -TMath::Pi(), TMath::Pi());
  
  cwd->cd();
} // bookHistograms


//_____________________________________________________________________________
/**
 * Fills the histograms.
 */
void
VecBosAnalyzer::fillHistograms()
{
  histos_["nPU0"]->Fill(tree_->nPU[0]);
  histos_["nPU1"]->Fill(tree_->nPU[1]);
  histos_["nPU2"]->Fill(tree_->nPU[2]);

  histos_["nPV"]->Fill(tree_->nPV);
  histos_["nPho"]->Fill(tree_->nPho);
  histos_["nMuon"]->Fill(tree_->nMuon);
  
  /// Fill the photons
  for (Int_t i=0; i < tree_->nPho; ++i) {
    histos_["ptPho"]->Fill(tree_->energyPho[i] / 
                           TMath::CosH(tree_->etaPho[i]));
    histos_["etaPho"]->Fill(tree_->etaPho[i]);
    histos_["phiPho"]->Fill(tree_->phiPho[i]);
  }

  /// Fill the muons
  for (Int_t i=0; i < tree_->nMuon; ++i) {
    histos_["ptMuon"]->Fill(tree_->energyMuon[i] / 
                            TMath::CosH(tree_->etaMuon[i]));
    histos_["etaMuon"]->Fill(tree_->etaMuon[i]);
    histos_["phiMuon"]->Fill(tree_->phiMuon[i]);
  }
} // fillHistograms


//_____________________________________________________________________________
/**
 * Initialization.
 */
void
VecBosAnalyzer::init()
{
  parseConfiguration();
  bookHistograms();
  setBranchesStatus();
} // init


//_____________________________________________________________________________
/**
 * Report event being processed inside the event loop.
 */
void
VecBosAnalyzer::reportEvent(Long64_t ientry)
{
  cout << "Processing record " << ientry + 1 << endl;
} // reportEvent

