#include "TCanvas.h"
#include "TDirectory.h"
#include "TFile.h"
#include "TH1.h"
// #include "T.h"

#include "RooAbsPdf.h"
#include "RooArgList.h"
#include "RooDataHist.h"
#include "RooPlot.h"
#include "RooRealVar.h"
#include "RooWorkspace.h"


void setupModel(RooWorkspace & w);
/// void createToyDataHist(RooWorkspace & w, const char *hname, const char *fname);
TH1* getHistFromFile(const char *hname, const char *fname);
TH1* getHistFromCanvasInFile(const char *hname, const char *cname, 
                             const char *fname);
void importBinnedData(TH1 *hist, RooWorkspace & w, const char *name="data");
void fitModelToData(RooWorkspace & w, const char *dataName="data",
                    const char *modelName="model");
void plotFittedModel(RooWorkspace & w, const char *dataName="data",
                     const char *modelName="model");


///_____________________________________________________________________________
/// Main entry point to execution.
void fitBWxCBtoHistForAdi() {
  /// Create a workspace to collect all the relevant objects.
  RooWorkspace w("w", "Fit BWxCB to a histogram");
  // const char * modelName = "model"; // scb = 2.207
  const char * modelName = "signal"; // scb = 2.159

  setupModel(w);
  // createToyDataHist(w, "toyData", "fitBWxCBHistForAdi.root");
  // TH1 *hist = getHistFromFile("toyData", "fitBWxCBHistForAdi.root");
  TH1 *hist = getHistFromCanvasInFile("dataZmass", "c1", "ZplotData.root");
  importBinnedData(hist, w);
  fitModelToData(w, "data", modelName);
  plotFittedModel(w, "data", modelName);
} /// fitBWxCBtoHistForAdi()


///_____________________________________________________________________________
void setupModel(RooWorkspace& w){
  w.factory("BreitWigner::bw(m[30,130], MZ[91.2], GZ[2.5])");
  w.factory("CBShape::cb(m, dm[-10,10], sigma[3, 0.1, 20], "
                        "alpha[1.5, 0.1, 10], power[1.5, 0.1, 10])");
  w.factory("FCONV::signal(m, bw, cb)");
  w.factory("Exponential::exp(m, decay[-0.04, -100, 100])");
  w.factory("SUM::model(S[100,0,1e9] * signal, B[10,0,1e9] * exp)");
} /// setupModel()


///_____________________________________________________________________________
// void createToyDataHist(RooWorkspace &, const char *hname, const char *fname){
//   ;
// } /// createToyDataHist()


///_____________________________________________________________________________
TH1* getHistFromFile(const char *hname, const char *fname){
  /// Store a pointer to the current working directory.
  TDirectory *currentDirectory = gDirectory;

  /// Fetch the hist from the canvas in the file:
  TFile *file = TFile::Open(fname);
  TH1 *hist = (TH1*) file->Get(hname);

  /// Make sure we got the hist:
  assert(hist);

  /// Get our own clone of the hist in our directory so that we can 
  /// close the original file.
  TH1 *histClone = (TH1F*) hist->Clone();

  /// Make sure we got the clone:
  assert(histClone);

  /// Move the cloned hist in our directory.
  histClone->SetDirectory(currentDirectory);

  /// Clean up the file:
  file->Close();
  delete file;

  /// Voila
  return histClone;
} /// getHistFromFile()


///_____________________________________________________________________________
TH1* getHistFromCanvasInFile(const char *hname, const char *cname, 
                             const char *fname)
{
  /// Store a pointer to the current working directory.
  TDirectory *currentDirectory = gDirectory;

  /// Fetch the hist from the canvas in the file:
  TFile *file = TFile::Open(fname);
  TCanvas *canvas = (TCanvas*) file->Get(cname);
  TH1 *hist = (TH1*) canvas->GetListOfPrimitives()->FindObject(hname);

  /// Make sure we got the hist:
  assert(hist);

  /// Get our own clone of the hist in our directory so that we can 
  /// close the original file.
  TH1 *histClone = (TH1F*) hist->Clone();

  /// Make sure we got the clone:
  assert(histClone);

  /// Move the cloned hist in our directory.
  histClone->SetDirectory(currentDirectory);

  /// Clean up the file:
  file->Close();
  delete file;

  /// Voila
  return histClone;
} /// getHistFromCanvasInFile()


///_____________________________________________________________________________
void importBinnedData(TH1 *hist, RooWorkspace & w, const char *name){
  RooDataHist data(name, hist->GetTitle(), RooArgList(*w.var("m")), hist);
  w.import(data);
} /// importBinnedData()


///_____________________________________________________________________________
void fitModelToData(RooWorkspace & w, const char *dataName, 
                    const char *modelName) {
  w.pdf(modelName)->fitTo(*w.data(dataName), RooFit::Range(70, 110));
} /// fitModelToData()


///_____________________________________________________________________________
void plotFittedModel(RooWorkspace & w, const char *dataName,
                     const char *modelName) {
  RooPlot * plot = w.var("m")->frame();
  plot->SetTitle(dataName);
  w.data(dataName)->plotOn(plot);
  w.pdf(modelName)->plotOn(plot);
  w.pdf(modelName)->plotOn(plot, RooFit::Components("exp"), 
                         RooFit::LineStyle(kDashed));
  w.pdf(modelName)->paramOn(plot);
  TCanvas * canvas = new TCanvas(dataName, dataName);
  plot->Draw();
} /// plotFittedModel()
