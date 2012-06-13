/**
 * Implementation of the VecBosAnalyzer class.
 * 
 * Jan Veverka, Caltech, 12 June 2012.
 */

#include <iostream>
#include "TTree.h"
#include "TChain.h"
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
    output_->Write();
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

  // Loop over the events
  for (Long64_t ientry=0; ientry < tree_->fChain->GetEntriesFast(); ientry++) {
    if (maxEventsInput_ >= 0 && ientry >= maxEventsInput_) break;
    cout << ientry << endl;
    if (tree_->LoadTree(ientry) < 0) break;
    tree_->fChain->GetEntry(ientry);
    // if (pass(ientry) == false) continue;
  } // end of loop over the events
  
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
    if (maxEvents.existsAs<Long64_t>("input", false)) {
      maxEventsInput_ = maxEvents.getUntrackedParameter<Long64_t>("input", -1);
    } // exists input
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
 * Initialization.
 */
void
VecBosAnalyzer::init()
{
  parseConfiguration();
  tree_->fChain->SetBranchStatus("*", 0);  // disable all branches  
} // init

