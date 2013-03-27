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

  histos_["dimuN"] = new TH1F("dimuN", ";n_{#mu#mu};Events / 1", 
                              51, -0.5, 50.5);
  histos_["dimuMass"] = new TH1F("dimuMass", ";m_{#mu#mu} (GeV);Events / GeV",
                                 150, 0., 150.);
  histos_["dimuPt"] = new TH1F("dimuPt", ";P_{T}^{#mu#mu} (GeV);Events / GeV", 
                               100, 0., 100.);
  histos_["dimuEta"] = new TH1F("dimuEta", ";#eta_{#mu#mu};Events / 0.1", 
                                60, -3, 3);
  histos_["dimuPhi"] = new TH1F("dimuPhi", 
                                ";#phi_{#mu#mu};Events / #frac{#pi}{50}", 
                                100, -TMath::Pi(), TMath::Pi());
  histos_["dimuY"] = new TH1F("dimuY", ";Dimuon y;Events / 0.1", 
                                60, -3, 3);
  histos_["mu1Pt"] = new TH1F("mu1Pt",
                              ";P_{T}^{#mu,lead} (GeV);Events / GeV", 
                               100, 0., 100.);
  histos_["mu2Pt"] = new TH1F("mu2Pt",
                              ";P_{T}^{#mu,sublead} (GeV);Events / GeV",
                               100, 0., 100.);
  histos_["mu2PtOverMu1Pt"] = new TH1F("mu2PtOverMu1Pt",
                              ";P_{T}^{#mu,sublead} / P_{T}^{#mu,lead} (%);Events / %",
                               200, 0., 200.);

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
    fillCand(*mm, event.weight());
  } /// Loop over dimuons  
} // VgDimuonHistoFiller::fillHistograms(..)


/**
 * Fills the histograms for object with index i.
 */
void
VgDimuonHistoFiller::fillCand(cit::VgCombinedCandidate const & mm, 
                              double weight)
{
  // LeafCand const & mu = dynamic_cast<LeafCand const &>(cand);
  // unsigned i = mu.key();
  weight *= mm.weight();
  VgLeafCandidate const & mu1 = mm.daughter(0);
  VgLeafCandidate const & mu2 = mm.daughter(1);
  histos_["dimuMass"]->Fill(mm.m (), weight);
  histos_["dimuPt" ]->Fill(mm.pt (), weight);
  histos_["dimuEta"]->Fill(mm.eta(), weight);
  histos_["dimuPhi"]->Fill(mm.phi(), weight);
  histos_["dimuY"  ]->Fill(mm.y  (), weight);
  histos_["mu1Pt"]->Fill(mu1.pt(), weight);  // Should this be weight1? No.
  histos_["mu2Pt"]->Fill(mu2.pt(), weight);  // Should this be weight2? No.
  histos_["mu2PtOverMu1Pt"]->Fill(100. * mu2.pt() / mu1.pt(), weight);
} // VgDimuonHistoFiller::fillObjectWithIndex(..)
