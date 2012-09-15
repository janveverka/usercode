/**
 * Implementation of the VgAnalyzer class.
 * 
 * Jan Veverka, Caltech, 08 September 2012.
 */

#include <iostream>
#include "TChain.h"
#include "TDirectory.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TMath.h"
#include "TTree.h"
#include "DataFormats/Provenance/interface/LuminosityBlockRange.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "Vgamma/Analysis/interface/VgAnalyzer.h"

using cit::VgAnalyzer;
using cit::VgAnalyzerTree;
using namespace std;
//_____________________________________________________________________________
/**
 * Constructor
 */
VgAnalyzer::VgAnalyzer(
  boost::shared_ptr<edm::ParameterSet> cfg
) :
  cfg_(cfg),
  tree_(0),
  output_(0),
  maxEventsInput_(-1),
  reportEvery_(1),
  titleStyle_(""),
  histoManager_(0)
{
  init();
} // ctor


//_____________________________________________________________________________
/**
 * Destructor
 */
VgAnalyzer::~VgAnalyzer()
{
  if (histoManager_ !=0 ) {
    delete histoManager_;
  }
  
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
VgAnalyzer::run()
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
    // fillHistograms();
    histoManager_->fillHistograms();
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
VgAnalyzer::parseConfiguration()
{
  parseInputs();
  parseOutputs();

  if (cfg_->existsAs<PSet>("maxEvents")) {
    PSet const& maxEvents = cfg_->getParameter<PSet>("maxEvents");
    maxEventsInput_ = maxEvents.getUntrackedParameter<Long64_t>("input", -1);
    reportEvery_ = maxEvents.getUntrackedParameter<Long64_t>("reportEvery", 1);
  } // exists maxEvents
  
  if (cfg_->existsAs<PSet>("options")) {
    PSet const& options = cfg_->getParameter<PSet>("options");
    if (options.existsAs<string>("titleStyle"))
      titleStyle_ = options.getParameter<string>("titleStyle");
  }
} // parseConfiguration


//_____________________________________________________________________________
/**
 * Parses the configuration and sets the inputs.
 */
void
VgAnalyzer::parseInputs()
{
  PSet const& inputs = cfg_->getParameter<PSet>("inputs");

  typedef vector<string> vstring;
  vstring filesToProcess;
  string treeName;

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

  if (inputs.existsAs<string>("treeName")) {
    treeName = inputs.getParameter<string>("treeName");
  } else {
    treeName = "VgAnalyzerKit/EventTree";
  }
  
  TChain *chain = new TChain(treeName.c_str());
  for (vstring::const_iterator filename = filesToProcess.begin();
       filename != filesToProcess.end(); ++filename) {
    chain->Add(filename->c_str());
  }
  
  tree_ = new VgAnalyzerTree(chain);  
} // parseInputs


//_____________________________________________________________________________
/**
 * Parses the output configuration and opens the output file.
 */
void
VgAnalyzer::parseOutputs()
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
VgAnalyzer::setBranchesStatus()
{
  TTree *chain = tree_->fChain;
  chain->SetBranchStatus("*", 1);  // enable all branches  
//   chain->SetBranchStatus("*", 0);  // disable all branches  
//   
//   chain->SetBranchStatus("rhoFastjet", 1);
//   chain->SetBranchStatus("rhoJetsFastJet", 1);
// 
//   chain->SetBranchStatus("nPU", 1);
//   chain->SetBranchStatus("nPV", 1);
//   
//   chain->SetBranchStatus("PVxPV", 1);
//   chain->SetBranchStatus("PVyPV", 1);
//   chain->SetBranchStatus("PVzPV", 1);
//   
//   chain->SetBranchStatus("beamSpotX", 1);
//   chain->SetBranchStatus("beamSpotY", 1);
//   chain->SetBranchStatus("beamSpotZ", 1);
//   
//   chain->SetBranchStatus("nPho", 1);
//   chain->SetBranchStatus("energyPho", 1);
//   chain->SetBranchStatus("phoEta", 1);
//   chain->SetBranchStatus("phoPhi", 1);
//   chain->SetBranchStatus("dr03HollowTkSumPtPho", 1);
//   chain->SetBranchStatus("dr03EcalRecHitSumEtPho", 1);
//   chain->SetBranchStatus("dr03HcalTowerSumEtPho", 1);
//   chain->SetBranchStatus("hasPixelSeedPho", 1);
//   chain->SetBranchStatus("hOverEPho", 1);
//   chain->SetBranchStatus("superClusterIndexPho", 1);
//   chain->SetBranchStatus("hOverEPho", 1);
//   
//   chain->SetBranchStatus("nSC", 1);
//   chain->SetBranchStatus("etaSC", 1);
//   chain->SetBranchStatus("rawEnergySC", 1);
//   chain->SetBranchStatus("etaWidthSC", 1);
//   chain->SetBranchStatus("e3x3SC", 1);
//   chain->SetBranchStatus("covIEtaIEtaSC", 1);
//   // chain->SetBranchStatus("", 1);
//   
//   chain->SetBranchStatus("nMuon", 1);
//   chain->SetBranchStatus("etaMuon", 1);
//   chain->SetBranchStatus("energyMuon", 1);
//   chain->SetBranchStatus("phiMuon", 1);
// 
//   // electron veto branches
//   chain->SetBranchStatus("nEle", 1);
//   chain->SetBranchStatus("superClusterIndexEle", 1);
//   chain->SetBranchStatus("superClusterIndexPho", 1);
//   chain->SetBranchStatus("hasMatchedConversionEle", 1);
//   chain->SetBranchStatus("gsfTrackIndexEle", 1);
//   chain->SetBranchStatus("nGsfTrack", 1);
//   chain->SetBranchStatus("expInnerLayersGsfTrack", 1);
  
} // setBranchesStatus



//_____________________________________________________________________________
/**
 * Initialization.
 */
void
VgAnalyzer::init()
{
  parseConfiguration();
  setBranchesStatus();
  histoManager_ = new cit::VgHistoManager(*tree_, *output_);
} // init


//_____________________________________________________________________________
/**
 * Report event being processed inside the event loop.
 */
void
VgAnalyzer::reportEvent(Long64_t ientry)
{
  cout << "Processing record " << ientry + 1 << endl;
} // reportEvent

