//=============================================
// For ECAL with CMS Detector at LHC
// Roofit Macro for Unbinned fit to Z peak
//=============================================

#ifndef __CINT__
#include "RooGlobalFunc.h"
#include<stdio.h>
#include<string>
#include<sstream>
#include<iostream>
#endif

#include "RooAbsPdf.h"
#include "RooAddPdf.h"
#include "RooArgList.h"
#include "RooBreitWigner.h"
#include "RooCBShape.h"
#include "RooDataSet.h"
#include "RooExponential.h"
#include "RooFFTConvPdf.h"
#include "RooGaussian.h"
#include "RooPlot.h"
#include "RooRealVar.h"
#include "RooWorkspace.h"

#include "TCanvas.h"
#include "TROOT.h"
#include "TStopwatch.h"
#include "TStyle.h"
#include "TLatex.h"
#include "tdrstyle.C"

using namespace RooFit;

RooWorkspace* makefit(char *filename, char* FitTitle, char* Outfile, double minMass, double maxMass, double mean_bw, double gamma_bw, double cutoff_cb, const char *plotOpt, const int nbins);

void fitZraw() {
  
  // Choose the File Name, Title and Output File for Fit
  string file;
  cout << "Enter File Name:"<<endl;
  getline(cin, file);
  string Title;
  cout << "Enter Fit Title"<<endl;
  getline(cin, Title);
  string output;
  cout << "Enter Output File Name"<<endl;
  getline(cin, output);

  // Define Fit Inputs and Call Fit
  char* filename = file.c_str();
  char* FitTitle = Title.c_str();
  char* Outfile = output.c_str();
  double minMass = 60;
  double maxMass = 120;
  double mean_bw = 91.1876;
  double gamma_bw = 2.4952;
  double cutoff_cb = 1.0;
  const char *plotOpt = "NEU";
  const int nbins = 40;
  RooWorkspace *w = makefit(filename, FitTitle, Outfile, minMass,  maxMass,  mean_bw,  gamma_bw,  cutoff_cb,  plotOpt, nbins);
  cout << "Saving file..." << endl << flush;
  w->writeToFile(Form("%s.root", Outfile));
  delete w;
}  
//______________________________________________________________

RooWorkspace* makefit(char* filename, char* FitTitle, char* Outfile, double minMass, double maxMass, double mean_bw, double gamma_bw, double cutoff_cb, const char* plotOpt, const int nbins) {
  gROOT->ProcessLine(".L tdrstyle.C");
  setTDRStyle();
  gStyle->SetPadRightMargin(0.05);
  
  //Create Data Set
  RooRealVar mass("mass","m(EE)",minMass,maxMass,"GeV/c^{2}");
  RooDataSet *data = RooDataSet::read(filename,RooArgSet(mass));
  
  //====================== Parameters===========================
  
  //Crystal Ball parameters
  RooRealVar cbBias ("#Deltam_{CB}", "CB Bias", -.01, -10, 10, "GeV/c^{2}");
  RooRealVar cbSigma("sigma_{CB}", "CB Width", 1.7, 0.02, 5.0, "GeV/c^{2}");
  RooRealVar cbCut  ("a_{CB}","CB Cut", 1.05, 0.1, 3.0);
  RooRealVar cbPower("n_{CB}","CB Order", 2.45, 0.1, 20.0);
  cbCut.setVal(cutoff_cb);
  
  //Breit_Wigner parameters
  RooRealVar bwMean("m_{Z}","BW Mean", 91.1876, "GeV/c^{2}");
  bwMean.setVal(mean_bw);
  RooRealVar bwWidth("#Gamma_{Z}", "BW Width", 2.4952, "GeV/c^{2}");
  bwWidth.setVal(gamma_bw);
  
  // Fix the Breit-Wigner parameters to PDG values
  bwMean.setConstant(kTRUE);
  bwWidth.setConstant(kTRUE);
  
  // Exponential Background parameters
  RooRealVar expRate("#lambda_{exp}", "Exponential Rate", -0.064, -1, 1);
  RooRealVar c0("c_{0}", "c0", 1., 0., 50.);
  
  //Number of Signal and Background events
  RooRealVar nsig("N_{S}", "# signal events", 524, 0.1, 10000000000.);
  RooRealVar nbkg("N_{B}", "# background events", 43, 1., 10000000.);
  
  //============================ P.D.F.s=============================
  
  // Mass signal for two decay electrons p.d.f.
  RooBreitWigner bw("bw", "bw", mass, bwMean, bwWidth);
  RooCBShape  cball("cball", "Crystal Ball", mass, cbBias, cbSigma, cbCut, cbPower);
  RooFFTConvPdf BWxCB("BWxCB", "bw X crystal ball", mass, bw, cball);
  
  // Mass background p.d.f.
  RooExponential bg("bg", "exp. background", mass, expRate);
  
  // Mass model for signal electrons p.d.f.
  RooAddPdf model("model", "signal", RooArgList(BWxCB), RooArgList(nsig));
  
  
  TStopwatch t ;
  t.Start() ;
  model.fitTo(*data,FitOptions("mh"),Optimize(0),Timer(1));
  t.Print() ;
  
  TCanvas* c = new TCanvas("c","Unbinned Invariant Mass Fit", 0,0,800,600);
  
  //========================== Plotting  ============================
  //Create a frame
  RooPlot* plot = mass.frame(Range(minMass,maxMass),Bins(nbins));
  
  data->plotOn(plot);
  model.plotOn(plot);
  model.paramOn(plot, Format(plotOpt, AutoPrecision(1)), Parameters(RooArgSet(cbBias, cbSigma, cbCut, cbPower, bwMean, bwWidth, expRate, nsig, nbkg)), Layout(0.66,0.63));
  plot->getAttText()->SetTextSize(.03);
  plot->Draw();
  
  // Print Fit Values
  TLatex *tex = new TLatex();
  tex->SetNDC();
  tex->SetTextSize(.04);
  tex->SetTextFont(2);
  tex->DrawLatex(0.195,0.875, "CMS ECAL, 2012");
  tex->Draw();
  tex->SetTextSize(0.022);
  tex->DrawLatex(0.195, 0.81, FitTitle);
  tex->DrawLatex(0.195, 0.75, "Z #rightarrow ee^{+}");
  tex->SetTextSize(0.024);
  tex->DrawLatex(0.645, 0.59, Form("BW Mean = %.2f GeV/c^{2}", bwMean.getVal()));
  tex->DrawLatex(0.645, 0.54, Form("BW #sigma = %.2f GeV/c^{2}", bwWidth.getVal()));
  c->Update();
  c->Print(Outfile);
  RooWorkspace *w = new RooWorkspace("zfit");
  w->import(model);
  w->import(*data);
  return w;
}
