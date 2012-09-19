/**
 * Implementation of the VgPileupHistoFiller class.
 * \author Jan Veverka, Caltech
 * \date 08 September 2012
 */

#include <iostream>
#include "TDirectory.h"
#include "TMath.h"
#include "Vgamma/Analysis/interface/VgPileupHistoFiller.h"

using namespace std;
using cit::VgPileupHistoFiller;

/**
 * Ctor.
 */
VgPileupHistoFiller::VgPileupHistoFiller(VgAnalyzerTree const& tree,
                                         HistoCollection & histos) :
  VgHistoFillerBase(tree, histos)
{  
} // 


/**
 * Dtor.
 */
VgPileupHistoFiller::~VgPileupHistoFiller() {}


/**
 * Books the histograms.
 */
void
VgPileupHistoFiller::bookHistograms()
{
  TDirectory * cwd = gDirectory;
  if (cwd->GetDirectory("Pileup")) cwd->cd("Pileup");
  else cwd->mkdir("Pileup")->cd();

  histos_["rho"] = new TH1F("rho", ";#rho;Events", 100, 0, 100);
  histos_["rhoNeutral"] = new TH1F("rhoNeutral", "Neutrals;#rho;Events", 
                                   100, 0, 100);

  cwd->cd();
} // VgPileupHistoFiller::bookHistograms(..)


/**
 * Fills the histograms.
 */
void
VgPileupHistoFiller::fillHistograms(cit::VgEvent const& event)
{
  histos_["rho"]->Fill(tree_->rho);
  histos_["rhoNeutral"]->Fill(tree_->rhoNeutral);
} // VgPileupHistoFiller::fillHistograms(..)
