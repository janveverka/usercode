#include "RooPlot.h"
#include "RooDataSet.h"
#include "TFile.h"
#include "RooWorkspace.h"
#include "RooAbsPdf.h"
#include "RooFormulaVar.h"
#include "RooArgSet.h"
#include "RooArgList.h"
#include "RooRealVar.h"

void plotFitOn(RooPlot&, RooWorkspace&, int color = kBlue, double scale = 1.0);
RooDataSet* scaleDataSet(RooDataSet&, double);

//_____________________________________________________________________________
void 
overlay() 
{
  TFile *rootfile1 = TFile::Open("tight.pdf.root");
  TFile *rootfile2 = TFile::Open("mva.pdf.root");
  
  RooWorkspace *w1 = (RooWorkspace*) rootfile1->Get("zfit");
  RooWorkspace *w2 = (RooWorkspace*) rootfile2->Get("zfit");
  
  /// Normalize to 1
  Double_t sum1 = w1->data("dataset")->sumEntries();
  Double_t sum2 = w2->data("dataset")->sumEntries();
  assert(sum2 > 0);
  Double_t scale1 = 1.0;
  Double_t scale2 = sum1 / sum2;

  RooPlot * frame = w1->var("mass")->frame();
  plotFitOn(*frame, *w1, kBlue, scale1);
  plotFitOn(*frame, *w2, kRed , scale2);
  frame->Draw();
} // overlay(..)


//_____________________________________________________________________________
void 
plotFitOn(RooPlot &plot, RooWorkspace &w, int color, double scale) 
{
  using namespace RooFit;
  RooDataSet *data = scaleDataSet(*(RooDataSet*)w.data("dataset"), scale);
  data->plotOn(&plot, LineColor(color), MarkerColor(color));
  w.pdf ("model"  )->plotOn(&plot, LineColor(color));
} // plotFitOn(..)


//_____________________________________________________________________________
RooDataSet* 
scaleDataSet(RooDataSet& data, double scale)
{
  RooFormulaVar scaleFunc("scale", Form("%g", scale), RooArgList());
  data.addColumn(scaleFunc);
  data.Print();
  RooDataSet * scaledData = new RooDataSet(data.GetName(), data.GetTitle(),
                                           &data, *data.get(), "", "scale");
  return scaledData;
}



