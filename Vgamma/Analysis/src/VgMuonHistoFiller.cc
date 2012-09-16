/**
 * Implementation of the VgMuonHistoFiller class.
 * \author Jan Veverka, Caltech
 * \date 08 September 2012
 */

#include <iostream>
#include "TMath.h"
#include "Vgamma/Analysis/interface/VgMuonHistoFiller.h"

using namespace std;
using cit::VgMuonHistoFiller;

/**
 * Ctor.
 */
VgMuonHistoFiller::VgMuonHistoFiller(VgAnalyzerTree const& tree,
                                     HistoCollection & histos) :
  VgHistoFillerBase(tree, histos)
{  
} // 


/**
 * Dtor.
 */
VgMuonHistoFiller::~VgMuonHistoFiller() {}


/**
 * Books the histograms.
 */
void
VgMuonHistoFiller::bookHistograms()
{
  histos_["muN"] = new TH1F("muN", ";Muon Multiplicity;Events / 1", 
                            51, -0.5, 50.5);
  histos_["muPt"] = new TH1F("muPt", ";Muon P_{T} (GeV);Events / GeV", 
                             100, -0.5, 100.5);
  histos_["muEta"] = new TH1F("muEta", ";Muon #eta;Events / 0.1", 
                              60, -3, 3);
  histos_["muPhi"] = new TH1F("muPhi", ";Muon #phi;Events / #frac{#pi}{50}", 
                              100, -TMath::Pi(), TMath::Pi());
} // VgMuonHistoFiller::bookHistograms(..)


/**
 * Fills the histograms.
 */
void
VgMuonHistoFiller::fillHistograms(cit::VgEvent const& event)
{
  histos_["muN"]->Fill(tree_.nMu);
  collection_ = & event.muons();
  loopOverObjects();  
} // VgMuonHistoFiller::fillHistograms(..)


/**
 * Fills the histograms for object with index i.
 */
void
VgMuonHistoFiller::fillCand(Cand const& cand)
{
  LeafCand const & mu = dynamic_cast<LeafCand const &>(cand);
  unsigned i = mu.key();
  histos_["muPt" ]->Fill(tree_.muPt[i]);
  histos_["muEta"]->Fill(tree_.muEta[i]);
  histos_["muPhi"]->Fill(tree_.muPhi[i]);
} // VgMuonHistoFiller::fillObjectWithIndex(..)

