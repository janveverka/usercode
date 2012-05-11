#include <string>
#include <iostream>
#include <vector>

#include "TROOT.h"
#include "fitBWxCBtoHistForAdi.C"

//   KEY: TH1F     dataZmass;1     dataZmass
//   KEY: TH1F     dataZmassEB;1   dataZmassEB
//   KEY: TH1F     dataZmassEE;1   dataZmassEE
//   KEY: TH1F     dataZmassEBHR9;1        dataZmassEBHR9
//   KEY: TH1F     dataZmassEBLR9;1        dataZmassEBLR9

using namespace std;

const unsigned kNumFits = 5;

/// Create a workspace to collect all the relevant objects.
RooWorkspace w("w", "Fit BWxCB to a histogram");

///_____________________________________________________________________________
/// Main entry point to execution.
void fitMultipleZpeaks() {
  const char * modelName = "signal"; // signal only
  const string hnames[kNumFits] = {"dataZmass", "dataZmassEB", "dataZmassEE",
                                   "dataZmassEBHR9", "dataZmassEBLR9"};

  setupModel(w);

  vector<float> sigmas;
  vector<float> esigmas;
  /// Loop over the fits
  for (unsigned i=0; i <  kNumFits; ++i) {
    const char *hname = hnames[i].c_str();
    TH1 *hist = getHistFromFile(hname, "MggDATA.root");
    importBinnedData(hist, w, hname);
    fitModelToData(w, hname, modelName);
    plotFittedModel(w, hname, modelName);
    sigmas.push_back(w.var("sigma")->getVal());
    esigmas.push_back(w.var("sigma")->getError());
  }
  
  
//   for (unsigned i=0; i <  kNumFits; ++i) {
//     const char *hname = hnames[i].c_str();    
//     TCanvas *c1 = (TCanvas*) gROOT->GetListOfCanvases()->FindObject(hname);
//     c1->Print(hname);
//   }
  
  
  /// Print report
  cout << "== Sigma CB ==" << endl;
  for (unsigned i=0; i <  kNumFits; ++i) {
    const char *hname = hnames[i].c_str();
    cout << setw(15) << hname << ": "
         << setw(10) << sigmas[i] << " +/- "
         << setw(5)  << esigmas[i] << endl;
  }
  
} /// fitMultipleZpeaks()
