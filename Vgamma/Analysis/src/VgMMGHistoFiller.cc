/**
 * Implementation of the VgMMGHistoFiller class.
 * \author Jan Veverka, Caltech
 * \date 19 September 2012
 */

#include <iostream>
#include <sstream>
#include <string>
#include "TDirectory.h"
#include "TMath.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "Vgamma/Analysis/interface/VgMMGHistoFiller.h"

using namespace std;
using cit::VgMMGHistoFiller;

/**
 * Ctor.
 */
VgMMGHistoFiller::VgMMGHistoFiller(VgAnalyzerTree const& tree,
                                   HistoCollection & histos) :
  VgHistoFillerBase(tree, histos)
{} // Default ctor.


/**
 * Dtor.
 */
VgMMGHistoFiller::~VgMMGHistoFiller() {}


/**
 * Books the histograms.
 */
void
VgMMGHistoFiller::bookHistograms()
{
  TDirectory * cwd = gDirectory;
  if (cwd->GetDirectory("MMGCands")) cwd->cd("MMGCands");
  else cwd->mkdir("MMGCands")->cd();

  histos_["mmgN"] = new TH1F("mmgN", ";Z#gamma Multiplicity;Events / 1", 
                             51, -0.5, 50.5);
  histos_["mmgMass"] = new TH1F("mmgMass", ";M_{Z#gamma} (GeV);Events / GeV",
                                150, 0., 150.);
  histos_["mmgPt"] = new TH1F("mmgPt", ";P_{T}^{Z#gamma} (GeV);Events / GeV", 
                              100, 0., 100.);
  histos_["mmgEta"] = new TH1F("mmgEta", 
			       ";#eta_{Z#gamma};Events / 0.1", 
                               100, -5, 5);
  histos_["mmgPhi"] = new TH1F("mmgPhi", 
                               ";#phi_{Z#gamma};Events / #frac{#pi}{50}", 
                               100, -TMath::Pi(), TMath::Pi());
  histos_["mmgY"] = new TH1F("mmgY", ";y_{Z#gamma};Events / 0.1", 
                             100, -5, 5);
  histos_["mmgMinDR"] = new TH1F("mmgMinDR",
                                 ";min #Delta R(#mu^{#pm},#gamma);Events / 0.1", 
                                 100, 0., 10.);
  histos_["mmgMaxDR"] = new TH1F("mmgMaxDR",
                                 ";max #Delta R(#mu^{#pm},#gamma);Events / 0.1",
                                 100, 0., 10.);

  cwd->cd();
} // VgMMGHistoFiller::bookHistograms(..)


/**
 * Fills the histograms.
 */
void
VgMMGHistoFiller::fillHistograms(cit::VgEvent const& event)
{
  cit::VgCombinedCandidates const & mmgCands = event.mmgCands();
  histos_["mmgN"]->Fill(mmgCands.size());
  /// Loop over mmgCands
  for (cit::VgCombinedCandidates::const_iterator mmg = mmgCands.begin();
       mmg != mmgCands.end(); ++mmg) {
    fillCand(*mmg);
  } /// Loop over mmgCands  
} // VgMMGHistoFiller::fillHistograms(..)


/**
 * Fills the histograms for object with index i.
 */
void
VgMMGHistoFiller::fillCand(cit::VgCombinedCandidate const & mmg)
{
  // Check if we have a got the mu mu gamma right.
  VgLeafCandidate const & mu1 = mmg.daughter(0);
  VgLeafCandidate const & mu2 = mmg.daughter(1);
  VgLeafCandidate const & pho = mmg.daughter(2);
  if (mu1.type() != cit::VgCandidate::kMuon || 
      mu2.type() != cit::VgCandidate::kMuon || 
      pho.type() != cit::VgCandidate::kPhoton) {
    ostringstream msg;
    msg << "Expect daughters of type " 
        << cit::VgCandidate::kMuon << ", " 
        << cit::VgCandidate::kMuon << ", "
        << cit::VgCandidate::kPhoton << " but got " 
        << mu1.type() << ", " << mu2.type() << ", " << pho.type();
    throw cms::Exception("BadMMGCand") << msg.str();                                     
  }

  double wgt = mmg.weight();
  double dr1 = pho.momentum().DeltaR(mu1.momentum());
  double dr2 = pho.momentum().DeltaR(mu2.momentum());
  
  histos_["mmgMass"]->Fill(mmg.m (), wgt);
  histos_["mmgPt" ]->Fill(mmg.pt (), wgt);
  histos_["mmgEta"]->Fill(mmg.eta(), wgt);
  histos_["mmgPhi"]->Fill(mmg.phi(), wgt);
  histos_["mmgY"  ]->Fill(mmg.y  (), wgt);
  histos_["mmgMinDR"]->Fill(TMath::Min(dr1, dr2), wgt);
  histos_["mmgMaxDR"]->Fill(TMath::Max(dr1, dr2), wgt);
  
} // VgMMGHistoFiller::fillObjectWithIndex(..)
