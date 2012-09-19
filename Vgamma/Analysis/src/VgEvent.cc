/**
 * \class VgEvent
 * 
 * \brief Class implementation.
 * 
 * \author Jan Veverka, Caltech 
 * \date 09 September 2012
 */

#include <algorithm>
#include <iostream>
#include "Vgamma/Analysis/interface/VgEvent.h"
// #include "Vgamma/Analysis/interface/VgLeafCandidate.h"

using cit::VgEvent;
typedef cit::VgCandidate Cand;
typedef cit::VgLeafCandidate LeafCand;
typedef cit::VgCombinedCandidate CombCand;


//_____________________________________________________________________________
/**
 * Ctor
 */
VgEvent::VgEvent(VgAnalyzerTree const& tree) :
  tree_(tree)
{
  readFromTree();
}


//_____________________________________________________________________________
/**
 * Copy ctor
 */
VgEvent::VgEvent(VgEvent const& other) :
  tree_(other.tree_)
{
  putPhotons(other.photons_);
  putMuons(other.muons_);
  putDimuons(other.dimuons_);
} // Copy ctor


//_____________________________________________________________________________
/**
 * Dtor
 */
VgEvent::~VgEvent()
{}


//_____________________________________________________________________________
/**
 * Updates the muon and photon collections to contain
 * all the muons and photon indices from the current event.
 */
void
VgEvent::readFromTree()
{
  photons_.clear();
  muons_  .clear();

  photons_.reserve(tree_.nPho);
  muons_  .reserve(tree_.nMu );

  for (Int_t i=0; i < tree_.nPho; ++i) 
    photons_.push_back(LeafCand(tree_, Cand::kPhoton, i));

  for (Int_t i=0; i < tree_.nMu ; ++i) 
    muons_  .push_back(LeafCand(tree_, Cand::kMuon  , i));
}


//_____________________________________________________________________________
/**
 * Photon producer.
 */
void
VgEvent::putPhotons(cit::VgLeafCandidates const & photons)
{
  photons_.resize(photons.size());
  std::copy(photons.begin(), photons.end(), photons_.begin());
}


//_____________________________________________________________________________
/**
 * Muon producer.
 */
void
VgEvent::putMuons(cit::VgLeafCandidates const & muons)
{
  muons_.resize(muons.size());
  std::copy(muons.begin(), muons.end(), muons_.begin());
}


//_____________________________________________________________________________
/**
 * Dimuon producer.
 */
void
VgEvent::putDimuons(cit::VgCombinedCandidates const & dimuons)
{
  dimuons_.resize(dimuons.size());
  std::copy(dimuons.begin(), dimuons.end(), dimuons_.begin());
}


//_____________________________________________________________________________
/**
 * Dimuon combiner.
 */
void
VgEvent::combineMuonsToDimuons()
{
  unsigned n = muons_.size();
  dimuons_.reserve(n * (n-1) / 2);
  for (cit::VgLeafCandidates::const_iterator mu1 = muons_.begin();
       mu1 != muons_.end() - 1; ++mu1)
    for (cit::VgLeafCandidates::const_iterator mu2 = mu1 + 1;
         mu2 != muons_.end(); ++mu2) {
      VgCombinedCandidate dimuon;
      dimuon.addDaughter(*mu1);
      dimuon.addDaughter(*mu2);
      dimuons_.push_back(dimuon);
    }
}


//_____________________________________________________________________________
/**
 * Mu-mu-gamma combiner.
 */
void
VgEvent::combineDimuonsAndPhotonsToMmgCands()
{  
  mmgCands_.reserve(dimuons_.size() * photons_.size());
  for (cit::VgCombinedCandidates::const_iterator dimu = dimuons_.begin();
       dimu != dimuons_.end(); ++dimu)
    for (cit::VgLeafCandidates::const_iterator pho = photons_.begin();
         pho != photons_.end(); ++pho) {
      VgCombinedCandidate mmg;
      mmg.addDaughter(*dimu);
      mmg.addDaughter(*pho);
      mmgCands_.push_back(mmg);
    }
}
// void
// VgEvent::combineDimuonsAndPhotonsToMmgCands()


