/**
 * Implementation of the VgPileupHistoFiller class.
 * \author Jan Veverka, Caltech
 * \date 08 September 2012
 */

#include <iostream>
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
  histos_["rho"] = new TH1F("rho", ";#rho;Events", 100, 0, 100);
  histos_["rhoNeutral"] = new TH1F("rhoNeutral", "Neutrals;#rho;Events", 
                                   100, 0, 100);
} // VgPileupHistoFiller::bookHistograms(..)


/**
 * Fills the histograms.
 */
void
VgPileupHistoFiller::fillHistograms(cit::VgEvent const& event)
{
  histos_["rho"]->Fill(tree_.rho);
  histos_["rhoNeutral"]->Fill(tree_.rhoNeutral);
} // VgPileupHistoFiller::fillHistograms(..)

/**
 * Would fill single objects from a collection but 
 * this doesn't apply here.  Have to define a function
 * that does nothing since its a part of the interface.
 */
void
VgPileupHistoFiller::fillObjectWithIndex(UInt_t i)
{}

