/**
 * Implementation of the VgDimuonHistoFiller class.
 * \author Jan Veverka, Caltech
 * \date 19 September 2012
 */

#include <iostream>
#include "TDirectory.h"
#include "TMath.h"
#include "Vgamma/Analysis/interface/VgDimuonHistoFiller.h"

using namespace std;
using cit::VgDimuonHistoFiller;

/**
 * Ctor.
 */
VgDimuonHistoFiller::VgDimuonHistoFiller() : VgHistoFillerBase()
{} // Default ctor.


/**
 * Dtor.
 */
VgDimuonHistoFiller::~VgDimuonHistoFiller() {}


/**
 * Books the histograms.
 */
void
VgDimuonHistoFiller::bookHistograms()
{

  TDirectory * cwd = gDirectory;
  if (cwd->GetDirectory("Dimuons")) cwd->cd("Dimuons");
  else cwd->mkdir("Dimuons")->cd();

  histos_["dimuN"] = new TH1F("dimuN", ";Dimuon Multiplicity;Events / 1", 
                              51, -0.5, 50.5);
  histos_["dimuMass"] = new TH1F("dimuMass", ";Dimuon mass (GeV);Events / GeV",
                                 150, 0., 150.);
  histos_["dimuPt"] = new TH1F("dimuPt", ";Dimuon P_{T} (GeV);Events / GeV", 
                               100, 0., 100.);
  histos_["dimuEta"] = new TH1F("dimuEta", ";Dimuon #eta;Events / 0.1", 
                                60, -3, 3);
  histos_["dimuPhi"] = new TH1F("dimuPhi", 
                                ";Dimuon #phi;Events / #frac{#pi}{50}", 
                                100, -TMath::Pi(), TMath::Pi());
  histos_["dimuY"] = new TH1F("dimuY", ";Dimuon y;Events / 0.1", 
                                60, -3, 3);
  histos_["mu1Pt"] = new TH1F("mu1Pt",
                              ";Leading muon P_{T} (GeV);Events / GeV", 
                               100, 0., 100.);
  histos_["mu2Pt"] = new TH1F("mu2Pt",
                              ";Subleading muon P_{T} (GeV);Events / GeV",
                               100, 0., 100.);
  histos_["mu2PtOverMu1Pt"] = new TH1F("mu2PtOverMu1Pt",
                              ";Subleading muon P_{T} (GeV);Events / GeV",
                               100, 0., 1.);

  cwd->cd();

} // VgDimuonHistoFiller::bookHistograms(..)


/**
 * Fills the histograms.
 */
void
VgDimuonHistoFiller::fillHistograms(cit::VgEvent const& event)
{
  cit::VgCombinedCandidates const & dimuons = event.dimuons();
  histos_["dimuN"]->Fill(dimuons.size());
  /// Loop over dimuons
  for (cit::VgCombinedCandidates::const_iterator mm = dimuons.begin();
       mm != dimuons.end(); ++mm) {
    fillCand(*mm);
  } /// Loop over dimuons  
} // VgDimuonHistoFiller::fillHistograms(..)


/**
 * Fills the histograms for object with index i.
 */
void
VgDimuonHistoFiller::fillCand(cit::VgCombinedCandidate const & mm)
{
  // LeafCand const & mu = dynamic_cast<LeafCand const &>(cand);
  // unsigned i = mu.key();
  double wgt = mm.weight();
  VgLeafCandidate const & mu1 = mm.daughter(0);
  VgLeafCandidate const & mu2 = mm.daughter(1);
  histos_["dimuMass"]->Fill(mm.m (), wgt);
  histos_["dimuPt" ]->Fill(mm.pt (), wgt);
  histos_["dimuEta"]->Fill(mm.eta(), wgt);
  histos_["dimuPhi"]->Fill(mm.phi(), wgt);
  histos_["dimuY"  ]->Fill(mm.y  (), wgt);
  histos_["mu1Pt"]->Fill(mu1.pt(), wgt);  // Should this be wgt1?
  histos_["mu2Pt"]->Fill(mu2.pt(), wgt);  // Should this be wgt2?
  histos_["mu2PtOverMu1Pt"]->Fill(mu2.pt() / mu1.pt(), wgt);
} // VgDimuonHistoFiller::fillObjectWithIndex(..)
