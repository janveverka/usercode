/**
 * Implementation of the VgPhotonHistoFiller class.
 * \author Jan Veverka, Caltech
 * \date 08 September 2012
 */

#include <iostream>
#include "TDirectory.h"
#include "TMath.h"
#include "Vgamma/Analysis/interface/VgPhoton.h"
#include "Vgamma/Analysis/interface/VgPhotonHistoFiller.h"

using namespace std;
using cit::VgPhotonHistoFiller;

/**
 * Ctor.
 */
VgPhotonHistoFiller::VgPhotonHistoFiller() : VgHistoFillerBase()
{} // Default ctor.


/**
 * Dtor.
 */
VgPhotonHistoFiller::~VgPhotonHistoFiller() {}


/**
 * Books the histograms.
 */
void
VgPhotonHistoFiller::bookHistograms()
{
  TDirectory * cwd = gDirectory;
  if (cwd->GetDirectory("Photons")) cwd->cd("Photons");
  else cwd->mkdir("Photons")->cd();

  histos_["phoN"] = new TH1F("phoN", ";Photon Multiplicity;Events / 1", 
                             21, -0.5, 20.5);  
  histos_["phoPt"] = new TH1F(
    "phoPt", ";Photon P_{T} (GeV);Events / GeV", 100, 0, 100
  );
  histos_["phoEta"] = new TH1F(
    "phoEta", ";Photon #eta;Events / 0.1", 60, -3, 3
  );
  histos_["phoSCEta"] = new TH1F(
    "phoSCEta", ";Photon Super Cluster #eta;Events / 0.1", 60, -3, 3
  );
  histos_["phoPhi"] = new TH1F(
    "phoPhi", ";Photon #phi;Events / #frac{#pi}{50}", 
    100, -TMath::Pi(), TMath::Pi()
  );
  histos_["phoTrkIso"] = new TH1F(
    "phoTrkIso", ";Photon Tracker Isolation (GeV);Events / 0.05 GeV", 
    100, 0, 5
  );

  histos_["phoEcalIso"] = new TH1F(
    "phoEcalIso", ";Photon ECAL Isolation (GeV);Events / 0.1 GeV", 
    100, 0, 10
  );
  
  histos_["phoHcalIso"] = new TH1F(
    "phoHcalIso", ";Photon HCAL Isolation (GeV);Events / 0.05 GeV", 
    100, 0, 5
  );
  
  histos_["phoHasPixelSeed"] = new TH1F(
    "phoHasPixelSeed", ";Photon Pixel Seed Match;Events / 1",
    2, -0.5, 1.5
  );
    
  histos_["phoHoverE"] = new TH1F(
    "phoHoverE", ";Photon H/E;Events / 0.005",
    100, 0, 0.5
  );
    
  histos_["phoR9"] = new TH1F(
    "phoR9", ";Photon R_{9};Events / 0.0025",
    60, 0.85, 1
  );
    
  histos_["phoSihih"] = new TH1F(
    "phoSihih",
    ";Photon #sigma_{i#eta i#eta} #times 10^{3};Events / 1",
    100, 0, 100
  );
    
  histos_["phoSipip"] = new TH1F(
    "phoSipip",
    ";Photon #sigma_{i#phi i#phi} #times 10^{3};Events / 1",
    100, 0, 100
  );

  cwd->cd();
    
} // VgPhotonHistoFiller::bookHistograms(..)


/**
 * Fills the histograms.
 */
void
VgPhotonHistoFiller::fillHistograms(cit::VgEvent const& event)
{
  cit::VgLeafCandidates const & photons = event.photons();
  histos_["phoN"]->Fill(photons.size());
  /// Loop over photons
  for (cit::VgLeafCandidates::const_iterator pho = photons.begin();
       pho != photons.end(); ++pho) {
    fillCand(*pho);
  } /// Loop over photons  
} // VgPhotonHistoFiller::fillHistograms(..)


/**
 * Fills the histograms for object with index i.
 */
void
VgPhotonHistoFiller::fillCand(cit::VgLeafCandidate const & cand)
{
  cit::VgPhoton pho(cand);
  double wgt = pho.weight();
  unsigned i = pho.key();
  cit::VgAnalyzerTree const & tree = pho.tree();

  histos_["phoPt" ]->Fill(pho.pt (), wgt);
  histos_["phoEta"]->Fill(pho.eta(), wgt);
  histos_["phoSCEta"]->Fill(pho.scEta(), wgt);
  histos_["phoPhi"]->Fill(pho.phi(), wgt);
  histos_["phoTrkIso"]->Fill(pho.trackIso(), wgt);
  histos_["phoEcalIso"]->Fill(pho.ecalIso(), wgt);
  histos_["phoHcalIso"]->Fill(pho.hcalIso(), wgt);
  histos_["phoHoverE"]->Fill(tree.phoHoverE[i], wgt);
  histos_["phoHasPixelSeed"]->Fill(tree.phohasPixelSeed[i], wgt);
  histos_["phoSihih"]->Fill(1000 * tree.phoSigmaIEtaIEta[i], wgt);
  histos_["phoSipip"]->Fill(1000 * tree.phoSigmaIPhiIPhi[i], wgt);
  histos_["phoR9"]->Fill(tree.phoR9[i], wgt);
} // VgPhotonHistoFiller::fillObjectWithIndex(..)

