/**
 * Implementation of the VgPhotonHistoFiller class.
 * \author Jan Veverka, Caltech
 * \date 08 September 2012
 */

#include <iostream>
#include "TMath.h"
#include "Vgamma/Analysis/interface/VgPhotonHistoFiller.h"

using namespace std;
using cit::VgPhotonHistoFiller;

/**
 * Ctor.
 */
VgPhotonHistoFiller::VgPhotonHistoFiller(VgAnalyzerTree const& tree,
                                         HistoCollection & histos) :
  VgHistoFillerBase(tree, histos)
{  
} // 


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
  histos_["phoN"] = new TH1F("phoN", ";Photon Multiplicity;Events / 1", 
                             21, -0.5, 20.5);  
  histos_["phoPt"] = new TH1F(
    "phoPt", ";Photon P_{T} (GeV);Events / GeV", 101, -0.5, 100.5
  );
  histos_["phoEta"] = new TH1F(
    "phoEta", ";Photon #eta;Events / 0.1", 60, -3, 3
  );
  histos_["phoPhi"] = new TH1F(
    "phoPhi", ";Photon #phi;Events / #frac{#pi}{50}", 
    100, -TMath::Pi(), TMath::Pi()
  );
  histos_["phoTrkIso"] = new TH1F(
    "phoTrkIso", ";Photon Track Isolation (GeV);Events / 0.2 GeV", 
    100, 0, 20
  );

  histos_["phoEcalIso"] = new TH1F(
    "phoEcalIso", ";Photon ECAL Isolation (GeV);Events / 0.2 GeV", 
    100, 0, 20
  );
  
  histos_["phoHcalIso"] = new TH1F(
    "phoHcalIso", ";Photon HCAL Isolation (GeV);Events / 0.2 GeV", 
    100, 0, 20
  );
  
  histos_["phoEBHasPixelSeed"] = new TH1F(
    "phoEBHasPixelSeed", "Barrel;Photon Pixel Seed Match;Events / 1",
    2, -0.5, 1.5
  );
    
  histos_["phoEEHasPixelSeed"] = new TH1F(
    "phoEEHasPixelSeed", "Endcaps;Photon Pixel Seed Match;Events / 1",
    2, -0.5, 1.5
  );
    
  histos_["phoHoverE"] = new TH1F(
    "phoHoverE", ";Photon H/E;Events / 0.005",
    100, 0, 0.5
  );
    
  histos_["phoEBR9"] = new TH1F(
    "phoEBR9", "Barrel;Photon R_{9};Events / 0.0025",
    60, 0.85, 1
  );
    
  histos_["phoEER9"] = new TH1F(
    "phoEER9", "Endcaps;Photon R_{9};Events / 0.0025",
    60, 0.85, 1
  );
    
  histos_["phoEBSihih"] = new TH1F(
    "phoEBSihih", 
    "Barrel;Photon #sigma_{i#eta i#eta} #times 10^{3};Events / 0.25",
    100, 0, 25
  );
    
  histos_["phoEESihih"] = new TH1F(
    "phoEESihih",
    "Endcaps;Photon #sigma_{i#eta i#eta} #times 10^{3};Events / 1",
    100, 0, 100
  );
    
  histos_["phoEBSipip"] = new TH1F(
    "phoEBSipip", 
    "Barrel;Photon #sigma_{i#phi i#phi} #times 10^{3};Events / 0.25",
    100, 0, 50
  );
    
  histos_["phoEESipip"] = new TH1F(
    "phoEESipip",
    "Endcaps;Photon #sigma_{i#phi i#phi} #times 10^{3};Events / 1",
    100, 0, 100
  );
    
} // VgPhotonHistoFiller::bookHistograms(..)


/**
 * Fills the histograms.
 */
void
VgPhotonHistoFiller::fillHistograms(cit::VgEvent const& event)
{
  histos_["phoN"]->Fill(tree_.nPho);
  collection_ = &event.photons();
  loopOverObjects();  
} // VgPhotonHistoFiller::fillHistograms(..)


/**
 * Fills the histograms for object with index i.
 */
void
VgPhotonHistoFiller::fillCand(Cand const & cand)
{
  LeafCand const & pho = dynamic_cast<LeafCand const &>(cand);
  double wgt = pho.weight();
  unsigned i = pho.key();

  histos_["phoPt" ]->Fill(pho.pt (), wgt);
  histos_["phoEta"]->Fill(pho.eta(), wgt);
  histos_["phoPhi"]->Fill(pho.phi(), wgt);
  histos_["phoTrkIso"]->Fill(tree_.phoTrkIsoHollowDR04[i], wgt);
  histos_["phoEcalIso"]->Fill(tree_.phoEcalIsoDR04[i], wgt);
  histos_["phoHcalIso"]->Fill(tree_.phoHcalIsoDR04[i], wgt);
  histos_["phoHoverE"]->Fill(tree_.phoHoverE[i], wgt);
  
  if (TMath::Abs(tree_.phoSCEta[i]) < 1.5) {
    /// Barrel
    histos_["phoEBHasPixelSeed"]->Fill(tree_.phohasPixelSeed[i], wgt);
    histos_["phoEBSihih"]->Fill(1000 * tree_.phoSigmaIEtaIEta[i], wgt);
    histos_["phoEBSipip"]->Fill(1000 * tree_.phoSigmaIPhiIPhi[i], wgt);
    histos_["phoEBR9"]->Fill(tree_.phoR9[i], wgt);
  } else {
    /// Endcaps
    histos_["phoEEHasPixelSeed"]->Fill(tree_.phohasPixelSeed[i], wgt);
    histos_["phoEESihih"]->Fill(1000 * tree_.phoSigmaIEtaIEta[i], wgt);
    histos_["phoEESipip"]->Fill(1000 * tree_.phoSigmaIPhiIPhi[i], wgt);
    histos_["phoEER9"]->Fill(tree_.phoR9[i], wgt);
  }
} // VgPhotonHistoFiller::fillObjectWithIndex(..)

