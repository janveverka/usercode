/**
 * Implementation of the VecBosAnalyzer class.
 * 
 * Jan Veverka, Caltech, 12 June 2012.
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
  maxEventsInput_(-1),
  reportEvery_(1),
  titleStyle_("")
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
  
  chain->SetBranchStatus("rhoFastjet", 1);
  chain->SetBranchStatus("rhoJetsFastJet", 1);

  chain->SetBranchStatus("nPU", 1);
  chain->SetBranchStatus("nPV", 1);
  
  chain->SetBranchStatus("nPho", 1);
  chain->SetBranchStatus("energyPho", 1);
  chain->SetBranchStatus("etaPho", 1);
  chain->SetBranchStatus("phiPho", 1);
  chain->SetBranchStatus("dr03HollowTkSumPtPho", 1);
  chain->SetBranchStatus("dr03EcalRecHitSumEtPho", 1);
  chain->SetBranchStatus("dr03HcalTowerSumEtPho", 1);
  chain->SetBranchStatus("hasPixelSeedPho", 1);
  chain->SetBranchStatus("hOverEPho", 1);
  chain->SetBranchStatus("superClusterIndexPho", 1);
  chain->SetBranchStatus("hOverEPho", 1);
  
  chain->SetBranchStatus("nSC", 1);
  chain->SetBranchStatus("etaSC", 1);
  chain->SetBranchStatus("rawEnergySC", 1);
  chain->SetBranchStatus("etaWidthSC", 1);
  chain->SetBranchStatus("e3x3SC", 1);
  chain->SetBranchStatus("covIEtaIEtaSC", 1);
  // chain->SetBranchStatus("", 1);
  
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
  
  bookPileupHistograms();
  bookPhotonHistograms();
  bookMuonHistograms();
  
  if (titleStyle_ == "mpl")
    setMplStyleTitles();
  
  cwd->cd();
} // bookHistograms


//_____________________________________________________________________________
/**
 * Books the pielup histograms.
 */
void
VecBosAnalyzer::bookPileupHistograms()
{
  histos_["nPU0"] = new TH1F(
    "nPU0", "Early OOT Pileup;True number of interactions;Events / 1", 
    101, -0.5, 100.5
  );
  
  histos_["nPU1"] = new TH1F(
    "nPU1", "In-Time Pileup;True number of interactions;Events / 1", 
    101, -0.5, 100.5
  );
  
  histos_["nPU2"] = new TH1F(
    "nPU2", "Late OOT Pileup;True number of interactions;Events / 1", 
    101, -0.5, 100.5
  );
  
  histos_["nPU0v1"] = new TH2F(
    "nPU0v1", 
    "True number of interactions;Early OOT Pileup;In-Time Pileup;Events", 
    31, -0.5, 61.5, 31, -0.5, 61.3
  );
  
  histos_["nPU0v2"] = new TH2F(
    "nPU0v2", 
    "True number of interactions;Early OOT Pileup;Late OOT Pileup;Events",
    31, -0.5, 61.5, 31, -0.5, 61.3
  );
  
  histos_["nPU1v2"] = new TH2F(
    "nPU1v2", 
    "True number of interactions;In-Time Pileup;Late OOT Pileup;Events", 
    31, -0.5, 61.5, 31, -0.5, 61.3
  );
  
  histos_["nPV"] = new TH1F(
    "nPV", "Reconstructed Primary Vertices;Number of Vertices;Events / 1", 
    101, -0.5, 100.5
  );
  
  histos_["rhoFastJet"] = new TH1F("rhoFastJet", ";#rho;Events", 100, 0, 100);
  histos_["rhoJetsFastJet"] = new TH1F("rhoJetsFastJet", "Jets;#rho;Events", 
                                       100, 0, 100);
} // bookPileupHistograms


//_____________________________________________________________________________
/**
 * Books the muon histograms.
 */
void
VecBosAnalyzer::bookMuonHistograms()
{
  histos_["nMuon"] = new TH1F("nMuon", "Muon;Multiplicity;Events / 1", 
                              51, -0.5, 50.5);
  histos_["ptMuon"] = new TH1F("ptMuon", "Muon;pt (GeV);Events / GeV", 
                               100, -0.5, 100.5);
  histos_["etaMuon"] = new TH1F("etaMuon", "Muon;#eta;Events / 0.1", 
                                60, -3, 3);
  histos_["phiMuon"] = new TH1F("phiMuon", "Muon;#phi;Events / #frac{#pi}{50}", 
                                100, -TMath::Pi(), TMath::Pi());
} // bookMuonHistograms


//_____________________________________________________________________________
/**
 * Books the photon histograms.
 */
void
VecBosAnalyzer::bookPhotonHistograms()
{
  histos_["nPho"] = new TH1F("nPho", "Photon;Multiplicity;Events / 1", 
                             21, -0.5, 20.5);  
  histos_["ptPho"] = new TH1F("ptPho", 
                              "Photon;pt (GeV);Events / GeV", 101, -0.5, 100.5);
  histos_["etaPho"] = new TH1F("etaPho", "Photon;#eta;Events / 0.1", 60, -3, 3);
  histos_["phiPho"] = new TH1F("phiPho", "Photon;#phi;Events / #frac{#pi}{50}", 
                               100, -TMath::Pi(), TMath::Pi());
  
  histos_["trkIsoPho"] = new TH1F(
    "trkIsoPho", "Photon;Track Isolation (GeV);Events / 0.2 GeV", 
    100, 0, 20
  );

  histos_["ecalIsoPho"] = new TH1F(
    "ecalIsoPho", "Photon;ECAL Isolation (GeV);Events / 0.2 GeV", 
    100, 0, 20
  );
  
  histos_["hcalIsoPho"] = new TH1F(
    "hcalIsoPho", "Photon;Track Isolation (GeV);Events / 0.2 GeV", 
    100, 0, 20
  );
  
  histos_["hasPixelSeedPhoEB"] = new TH1F(
    "hasPixelSeedPhoEB", "Barrel;Photon Pixel Seed Match;Events / 1",
    2, -0.5, 1.5
  );
    
  histos_["hasPixelSeedPhoEE"] = new TH1F(
    "hasPixelSeedPhoEE", "Barrel;Photon Pixel Seed Match;Events / 1",
    2, -0.5, 1.5
  );
    
  histos_["hOverEPho"] = new TH1F(
    "hOverEPho", ";Photon H/E;Events / 0.005",
    100, 0, 0.5
  );
    
  histos_["etaWidthPhoEB"] = new TH1F(
    "etaWidthPhoEB", "Barrel;Photon #sigma_{#eta} #times 10^{3};Events / 0.2",
    150, 0, 30
  );
    
  histos_["etaWidthPhoEE"] = new TH1F(
    "etaWidthPhoEE", "Endcaps;Photon #sigma_{#eta} #times 10^{3};Events / 1",
    150, 0, 150
  );
    
  histos_["r9PhoEB"] = new TH1F(
    "r9PhoEB", "Barrel;Photon R_{9};Events / 0.0025",
    60, 0.85, 1
  );
    
  histos_["r9PhoEE"] = new TH1F(
    "r9PhoEE", "Endcaps;Photon R_{9};Events / 0.0025",
    60, 0.85, 1
  );
    
  histos_["sihihPhoEB"] = new TH1F(
    "sihihPhoEB", 
    "Barrel;Photon #sigma_{i#eta i#eta} #times 10^{3};Events / 0.25",
    100, 0, 25
  );
    
  histos_["sihihPhoEE"] = new TH1F(
    "sihihPhoEE",
    "Endcaps;Photon #sigma_{i#eta i#eta} #times 10^{3};Events / 1",
    100, 0, 100
  );
    
} // bookPhotonHistograms


//_____________________________________________________________________________
/**
 * Sets the matplotlib-style histogram titles.
 */
void
VecBosAnalyzer::setMplStyleTitles()
{
  setMplStyleTitlesForPileupHistograms();
  setMplStyleTitlesForPhotonHistograms();
  setMplStyleTitlesForMuonHistograms();
} // setMplStyleTitles


//_____________________________________________________________________________
/**
 * Sets the matplotlib-style titles for the pileup histograms.
 */
void
VecBosAnalyzer::setMplStyleTitlesForPileupHistograms()
{
} // setMplStyleTitlesForPileupHistograms


//_____________________________________________________________________________
/**
 * Sets the matplotlib-style titles for the photon histograms.
 */
void
VecBosAnalyzer::setMplStyleTitlesForPhotonHistograms()
{
  histos_["r9PhoEB"]->GetXaxis()->SetTitle("Photon $R_{9}$");
} // setMplStyleTitlesForPhotonHistograms


//_____________________________________________________________________________
/**
 * Sets the matplotlib-style titles for the muon histograms.
 */
void
VecBosAnalyzer::setMplStyleTitlesForMuonHistograms()
{
} // setMplStyleTitlesForMuonHistograms


//_____________________________________________________________________________
/**
 * Fills the histograms.
 */
void
VecBosAnalyzer::fillHistograms()
{
  /// Shorthand notation
  VecBosTree const& t = *tree_;

  fillPileupHistograms();
  
  histos_["nPho"]->Fill(t.nPho);
  histos_["nMuon"]->Fill(t.nMuon);
  
  /// Fill the photons
  for (Int_t i=0; i < t.nPho; ++i) {
    fillHistogramsForPhotonIndex(i);
  }

  /// Fill the muons
  for (Int_t i=0; i < t.nMuon; ++i) {
    fillHistogramsForMuonIndex(i);
  }
} // fillHistograms


//_____________________________________________________________________________
/**
 * Fills the pileup histograms.
 */
void
VecBosAnalyzer::fillPileupHistograms()
{
  /// Shorthand notation
  VecBosTree const& t = *tree_;

  histos_["nPU0"]->Fill(t.nPU[0]);
  histos_["nPU1"]->Fill(t.nPU[1]);
  histos_["nPU2"]->Fill(t.nPU[2]);

  histos_["nPU0v1"]->Fill(t.nPU[0], t.nPU[1]);
  histos_["nPU0v2"]->Fill(t.nPU[0], t.nPU[2]);
  histos_["nPU1v2"]->Fill(t.nPU[1], t.nPU[2]);

  histos_["rhoFastJet"]->Fill(t.rhoFastjet);
  histos_["rhoJetsFastJet"]->Fill(t.rhoJetsFastJet);

  histos_["nPV"]->Fill(t.nPV);
} // fillPileupHistograms


//_____________________________________________________________________________
/**
 * Fills the photon histograms.
 */
void
VecBosAnalyzer::fillHistogramsForPhotonIndex(Int_t iPho)
{
  /// Shorthand notation
  VecBosTree const& t = *tree_;
  
  /// Some of the variables are supercluster related. Get the SC index.
  Int_t iSC = t.superClusterIndexPho[iPho];
  
  histos_["ptPho"]->Fill(t.energyPho[iPho] / 
                          TMath::CosH(t.etaPho[iPho]));
  histos_["etaPho"]->Fill(t.etaPho[iPho]);
  histos_["phiPho"]->Fill(t.phiPho[iPho]);
  histos_["trkIsoPho"]->Fill(t.dr03HollowTkSumPtPho[iPho]);
  histos_["ecalIsoPho"]->Fill(t.dr03EcalRecHitSumEtPho[iPho]);
  histos_["hcalIsoPho"]->Fill(t.dr03HcalTowerSumEtPho[iPho]);
  histos_["hOverEPho"]->Fill(t.hOverEPho[iPho]);
  
  if (TMath::Abs(t.etaSC[iSC]) < 1.5) {
    /// Barrel
    histos_["hasPixelSeedPhoEB"]->Fill(t.hasPixelSeedPho[iPho]);
    histos_["etaWidthPhoEB"]->Fill(1000 * t.etaWidthSC[iSC]);
    histos_["r9PhoEB"]->Fill(t.e3x3SC[iSC] / t.rawEnergySC[iSC]);
    histos_["sihihPhoEB"]->Fill(1000 * TMath::Sqrt(t.covIEtaIEtaSC[iSC]));
  } else {
    /// Endcaps
    histos_["hasPixelSeedPhoEE"]->Fill(t.hasPixelSeedPho[iPho]);
    histos_["etaWidthPhoEE"]->Fill(1000 * t.etaWidthSC[iSC]);
    histos_["r9PhoEE"]->Fill(t.e3x3SC[iSC] / t.rawEnergySC[iSC]);
    histos_["sihihPhoEE"]->Fill(1000 * TMath::Sqrt(t.covIEtaIEtaSC[iSC]));
  }
} // fillHistogramsForPhotonIndex


//_____________________________________________________________________________
/**
 * Fills the muon histograms.
 */
void
VecBosAnalyzer::fillHistogramsForMuonIndex(Int_t i)
{
  /// Shorthand notation
  VecBosTree const& t = *tree_;

  histos_["ptMuon"]->Fill(t.energyMuon[i] / 
                          TMath::CosH(t.etaMuon[i]));
  histos_["etaMuon"]->Fill(t.etaMuon[i]);
  histos_["phiMuon"]->Fill(t.phiMuon[i]);
} // fillHistogramsForMuonIndex


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

