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
using cit::VgHistoManager;
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
  maxEventsToProcess_(-1),
  reportEvery_(1),
  titleStyle_(""),
  histoManagers_(),
  stopwatch_(),
  eventWeight_(1),
  verbosity_(0)
{
  init();
} // ctor


//_____________________________________________________________________________
/**
 * Destructor
 */
VgAnalyzer::~VgAnalyzer()
{
//   if (histoManager_ !=0 ) {
//     delete histoManager_;
//   }
  
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
  // Long64_t totalEntries = tree_->fChain->GetEntriesFast();
  Long64_t totalEntries = tree_->fChain->GetEntries();
  Long64_t maxEntry = totalEntries;
  if (0 <= maxEventsToProcess_ && maxEventsToProcess_ < maxEntry) {
    maxEntry = maxEventsToProcess_;
  }

  // Loop over the events.
  cout << "Start processing " << maxEntry << " records..." << endl;
  stopwatch_.Start();
  Long64_t ientry=0;
  for (; ientry < maxEntry; ientry++) {
    if (tree_->LoadTree(ientry) < 0) break;
    if (ientry % reportEvery_ == 0) reportEvent(ientry, maxEntry);
    tree_->fChain->GetEntry(ientry);

    VgEvent event(*tree_);
    event.readFromTree();
    
    // Loop over histoManagers_
    for (HistoManagers::iterator worker = histoManagers_.begin();
         worker != histoManagers_.end(); ++worker)
      worker->fillHistograms(event);
    // End of loop over histoManagers_
      
  } // end of loop over the events
  
  cout.precision(3);
  cout << "Processed " << ientry << " of " << totalEntries
       << " (" << (float) 100 * ientry / totalEntries << "%) records." << endl;
  
  // Loop over workers
  for (HistoManagers::iterator worker = histoManagers_.begin();
        worker != histoManagers_.end(); ++worker) {
    cout << "== " << worker->output().GetName() << " ==" << endl;
    worker->print(cout);
    cout << endl;
  } // Loop over workers
  
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
  parseHistograms();
  parseMaxEvents();
  parseOptions();
  parseEventWeight();
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
  
  string versionString = "V14MC";
  if (inputs.existsAs<string>("version")) {
    versionString = inputs.getParameter<string>("version");
  }
  
  // cout << "VgAnalyzer::parseInputs(): version: " << versionString << endl;
  
  VgAnalyzerTree::Version version = VgAnalyzerTree::kV14MC;
  if        (versionString == string("V14MC"  )) {
           version = VgAnalyzerTree::kV14MC   ;
  } else if (versionString == string("V14Data")) {
           version = VgAnalyzerTree::kV14Data ;
  } else if (versionString == string("V15MC"  )) {
           version = VgAnalyzerTree::kV15MC   ;
  } else {
    throw cms::Exception("BanConfiguration") << "VgAnalyzer::parseInputs(): "
                                             << "Version must be one of: "
                                             << "V14MC, V14Data, V15MC";
  }

  if (inputs.existsAs<vector<string> >("activeBranches")) {
    activeBranches_ = inputs.getParameter<vector<string> >("activeBranches");
  } else {
    activeBranches_.push_back("nMu");
    activeBranches_.push_back("mu*");
    activeBranches_.push_back("nPho");
    activeBranches_.push_back("pho*");
    activeBranches_.push_back("rho*");
    if (version == VgAnalyzerTree::kV14MC ||
        version == VgAnalyzerTree::kV15MC) {
      activeBranches_.push_back("nPU");
    }
  }
  
//   cout << "Active branches:" << endl;
//   for (vector<string>::const_iterator branch = activeBranches_.begin();
//        branch != activeBranches_.end(); ++branch) {
//     cout << *branch << endl;
//   }
    
  TChain *chain = new TChain(treeName.c_str());
  for (vstring::const_iterator filename = filesToProcess.begin();
       filename != filesToProcess.end(); ++filename) {
    chain->Add(filename->c_str());
  }
  
  tree_ = new VgAnalyzerTree(chain, version);  
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
 * Parses the histogram configuration and fills the histoManagers_.
 */
void
VgAnalyzer::parseHistograms()
{
  PSet const& histograms = cfg_->getParameter<PSet>("histograms");
  
  bool isMC(tree_->run == 1);
  if (histograms.existsAs<bool>("isMC")) {
    isMC = histograms.getParameter<bool>("isMC");
  } 
  
  /// Loop over workers
  vector<string> workers = histograms.getParameterNamesForType<PSet>();
  for (vector<string>::const_iterator worker = workers.begin();
       worker != workers.end(); ++worker) {
    TDirectory * subdir = output_->mkdir(worker->c_str());
    PSet const & cfg = histograms.getParameter<PSet>(*worker);
    histoManagers_.push_back(new VgHistoManager(*tree_, *subdir, cfg, isMC));
  } /// Loop over workers
} // parseConfiguration


//_____________________________________________________________________________
/**
 * Parses the configuration and sets the data members of 
 * the maximum number of events to process maxEventsToProcess_
 * and the frequency of the event processesing reporting
 * reportEvery_.
 */
void
VgAnalyzer::parseMaxEvents()
{
  if (cfg_->existsAs<PSet>("maxEvents")) {
    PSet const& maxEvents = cfg_->getParameter<PSet>("maxEvents");
    maxEventsToProcess_ = maxEvents.getUntrackedParameter<Long64_t>("toProcess", -1);
    reportEvery_ = maxEvents.getUntrackedParameter<Long64_t>("reportEvery", 1);
  } // exists maxEvents
} // parseMaxEvents()


//_____________________________________________________________________________
/**
 * Parses the configuration of options and sets the data members of 
 * the titleStyle_ and verbosity_.
 */
void
VgAnalyzer::parseOptions()
{
  if (cfg_->existsAs<PSet>("options")) {
    cout << "Parsing options ..." << endl;
    PSet const& options = cfg_->getParameter<PSet>("options");
    if (options.existsAs<string>("titleStyle")) {
      titleStyle_ = options.getParameter<string>("titleStyle");
    }
    if (options.existsAs<Long64_t>("verbosity")) {
      cout << "Found option verbosity = " 
           << options.getParameter<Long64_t>("verbosity") << endl;
      verbosity_ = options.getParameter<Long64_t>("verbosity");
    } else {
      cout << "No option verbosity found." << endl;
    } // verbosity
  } else {
    cout << "No configuration options found." << endl;
  }// exists options
} // parseOptions()


//_____________________________________________________________________________
/**
 * Parses the configuration of the event weight inputs. Calculates and sets
 * it when found. 
 */
void
VgAnalyzer::parseEventWeight()
{
  if (cfg_->existsAs<PSet>("eventWeight")) {
    PSet const& ew = cfg_->getParameter<PSet>("eventWeight");
    double   xs   = ew.getParameter<double  >("crossSectionInPicoBarns");
    double   lumi = ew.getParameter<double  >("scaleToLumiInInverseFemtoBarns");
    Long64_t nevt = ew.getParameter<Long64_t>("totalProcessedEvents");
    // convert lumi to inverse picobarns 1/pb
    lumi *= 1e3;
    eventWeight_ = xs * lumi / nevt;
  } // exists eventWeight  
} // parseEventWeight


//_____________________________________________________________________________
/**
 * Sets the status of the unused branches to 0 to save time.
 */
void
VgAnalyzer::setBranchesStatus()
{
  TTree *chain = tree_->fChain;
//  chain->SetBranchStatus("*", 1);  // enable all branches  
  chain->SetBranchStatus("*", 0);  // disable all branches  
//   chain->SetBranchStatus("nEle", 1);
//   chain->SetBranchStatus("ele*", 1);
  for (vector<string>::const_iterator branch = activeBranches_.begin();
       branch != activeBranches_.end(); ++branch) {
    chain->SetBranchStatus(branch->c_str(), 1);
  }
  
} // setBranchesStatus



//_____________________________________________________________________________
/**
 * Initialization.
 */
void
VgAnalyzer::init()
{
  parseConfiguration();
  applyConfiguration();
  setBranchesStatus();
  turnOnTreeCaching(5e8); // 5e8 = 500,000,000 = 500 MB
  // histoManagers_.push_back(new cit::VgHistoManager(*tree_, *output_));
} // init


//_____________________________________________________________________________
/**
 * Initialization.
 * Precondition: parseConfiguration() was called
 */
void
VgAnalyzer::applyConfiguration()
{
  if (verbosity_ > 0) {
    cout << "Applying event weight " << eventWeight_ << endl;
  }
  tree_->fChain->SetWeight(eventWeight_, "global");  
} // applyConfiguration


//_____________________________________________________________________________
/**
 * Turns on caching of the tree branches.
 */
void
VgAnalyzer::turnOnTreeCaching(long cacheSize)
{
  TTree *chain = tree_->fChain;
  chain->SetCacheSize(cacheSize);
  for (vector<string>::const_iterator branch = activeBranches_.begin();
       branch != activeBranches_.end(); ++branch) {
    chain->AddBranchToCache(branch->c_str());
  }
  
  // chain->AddBranchToCache("*"); 
//   chain->AddBranchToCache("nMu");
//   chain->AddBranchToCache("mu*");
//   chain->AddBranchToCache("nPho");
//   chain->AddBranchToCache("pho*");
//   chain->AddBranchToCache("rho*");
//   if (tree_->version() == VgAnalyzerTree::kV14MC ||
//       tree_->version() == VgAnalyzerTree::kV15MC) {
//     chain->AddBranchToCache("nPU");
//   }
} 
// void
// VgAnalyzer::turnOnTreeCaching(long cacheSize)



//_____________________________________________________________________________
/**
 * Report event being processed inside the event loop.
 */
void
VgAnalyzer::reportEvent(Long64_t thisEntry, Long64_t entriesToProcess)
{
  
    stopwatch_.Stop();
    double realTime = stopwatch_.RealTime();
    stopwatch_.Start(false);

    if (entriesToProcess >= 0) {
    double progress = (double) thisEntry / entriesToProcess;
    double eta = 99999999;
      
    if (progress > 0.) 
      eta = (1. - progress) / progress * realTime;

    string etastring = "?";
    if (eta < 9999999) etastring = humanReadableTime(eta);
    
    cout.precision(3);
    cout << "Processing record " << thisEntry + 1
         << " of " << entriesToProcess << ", "
         << 100 * progress << "%"
//          << ", Elapsed: " << stopwatch_.RealTime() << "s = "
//          << humanReadableTime(realTime) << ", "
//          << "ETA: " << etastring 
         << endl;
  } else {
    cout << "Processing record " << thisEntry + 1 << endl;
  }
} // reportEvent


//_____________________________________________________________________________
/**
 * Returns a string representing timeInSeconds in human readable format.
 */
string
VgAnalyzer::humanReadableTime(double timeInSeconds) const
{
  char buffer[64];
  sprintf(buffer, "%01.0f:%02.0f:%02.1f", 
          floor(timeInSeconds / 3600.), 
          floor(fmod(timeInSeconds, 3600.) / 60.),
          fmod(timeInSeconds, 60.));
  return string(buffer);
}
// string
// VgAnalyzer::humanReadableTime(double timeInSeconds) const
