/**
 * Implementation of the VgMuonHistoFiller class.
 * \author Jan Veverka, Caltech
 * \date 08 September 2012
 */

#include <iostream>
#include "TDirectory.h"
#include "TMath.h"
#include "Vgamma/Analysis/interface/VgMuon.h"
#include "Vgamma/Analysis/interface/VgMuonHistoFiller.h"

using namespace std;
using cit::VgMuonHistoFiller;

/**
 * Ctor.
 */
VgMuonHistoFiller::VgMuonHistoFiller() : VgHistoFillerBase()
{} // Default ctor.


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
  TDirectory * cwd = gDirectory;
  if (cwd->GetDirectory("Muons")) cwd->cd("Muons");
  else cwd->mkdir("Muons")->cd();

  histos_["muN"] = new TH1F("muN", ";Muon Multiplicity;Events / 1", 
                            51, -0.5, 50.5);
  
  histos_["muPt"] = new TH1F("muPt", ";P_{T}^{#mu} (GeV);Events / GeV", 
                             100, 0, 100.);
  
  histos_["muEta"] = new TH1F("muEta", ";#eta_{#mu};Events / 0.1", 
                              60, -3, 3);
  
  histos_["muPhi"] = new TH1F("muPhi", ";#phi_{#mu};Events / #frac{#pi}{50}", 
                              102, -1.02 * TMath::Pi(), 1.02 * TMath::Pi());
  
  histos_["muIsGlobal"] = new TH1F("muIsGlobal", ";#mu is global;Events", 
                                   4, -1.5 , 2.5);
  
  histos_["muNormChi2"] = new TH1F("muNormChi2", ";Muon #chi^{2}/n_{dof};Events / 0.2", 
                                   110, 0, 11);
  
  histos_["muChamberHits"] = new TH1F("muChamberHits", ";n^{#mu}_{hits};Events", 
                                      11, -0.5, 10.5);
  
  histos_["muStations"] = new TH1F("muStations", ";n^{#mu}_{station};Events", 
                                   6, -0.5, 5.5);
  
  histos_["muDxy"] = new TH1F("muDxy", ";d^{#mu}_{xy} (#mum);Events / 10 #mum", 
                              100, -500, 500);
  
  histos_["muDz"] = new TH1F("muDz", ";d^{#mu}_{z} (#mum);Events / 40 #mum", 
                             100, -2000, 2000);
  
  histos_["muPixelHits"] = new TH1F("muPixelHits", ";n^{#mu}_{pixel};Events",
                                    11, -0.5, 10.5);
  
  histos_["muTkHits"] = new TH1F("muTkHits", ";n^{#mu}_{tracker};Events", 
                                 51, -0.5, 50.5);
  
  histos_["muCombRelIso"] = new TH1F("muCombRelIso", 
                                     ";I^{rel}_{comb} (%);Events / 0.1%", 
                                     110, 0, 11);

  cwd->cd();

} // VgMuonHistoFiller::bookHistograms(..)


/**
 * Fills the histograms.
 */
void
VgMuonHistoFiller::fillHistograms(cit::VgEvent const& event)
{
  cit::VgLeafCandidates const & muons = event.muons();
  histos_["muN"]->Fill(muons.size());
  /// Loop over muons
  for (cit::VgLeafCandidates::const_iterator mu = muons.begin();
       mu != muons.end(); ++mu) {
    fillCand(*mu, event.weight());
  } /// Loop over muons  
} // VgMuonHistoFiller::fillHistograms(..)


/**
 * Fills the histograms for object with index i.
 */
void
VgMuonHistoFiller::fillCand(cit::VgLeafCandidate const & cand, double weight)
{
  cit::VgMuon mu(cand);
  cit::VgAnalyzerTree const & tree = mu.tree();
  unsigned i = mu.key();
  weight *= mu.weight();

  histos_["muPt"         ]->Fill(mu.pt ()                        , weight);
  histos_["muEta"        ]->Fill(mu.eta()                        , weight);
  histos_["muPhi"        ]->Fill(mu.phi()                        , weight);
  histos_["muIsGlobal"   ]->Fill(mu.isGlobalMuon()               , weight);
  histos_["muNormChi2"   ]->Fill(tree.muChi2NDF               [i], weight);
  histos_["muChamberHits"]->Fill(tree.muNumberOfValidMuonHits [i], weight);
  histos_["muStations"   ]->Fill(tree.muStations              [i], weight);
  histos_["muDxy"        ]->Fill(1e4 * tree.muPVD0            [i], weight);
  histos_["muDz"         ]->Fill(1e4 * tree.muPVDz            [i], weight);
  histos_["muPixelHits"  ]->Fill(tree.muNumberOfValidPixelHits[i], weight);
  histos_["muTkHits"     ]->Fill(tree.muNumberOfValidTrkHits  [i], weight);
  histos_["muCombRelIso" ]->Fill(mu.combRelIso()                 , weight);

} // VgMuonHistoFiller::fillObjectWithIndex(..)

