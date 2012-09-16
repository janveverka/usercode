/**
 * \class VgEvent
 * 
 * \brief Class implementation.
 * 
 * \author Jan Veverka, Caltech 
 * \date 09 September 2012
 */

#include "Vgamma/Analysis/interface/VgEvent.h"
#include "Vgamma/Analysis/interface/VgLeafCandidate.h"

using cit::VgEvent;
typedef cit::VgCandidate Cand;
typedef cit::VgLeafCandidate LeafCand;

/**
 * Ctor
 */
VgEvent::VgEvent(VgAnalyzerTree const& tree) :
  tree_(tree)
{
  read();
}

/**
 * Dtor
 */
VgEvent::~VgEvent()
{}

/**
 * Updates the muon and photon collections to contain
 * all the muons and photon indices from the current event.
 */
void
VgEvent::read()
{
  photons_.clear();
  muons_  .clear();

  photons_.reserve(tree_.nPho);
  muons_  .reserve(tree_.nMu );

  for (Int_t i=0; i < tree_.nPho; ++i) 
    photons_.push_back(new LeafCand(tree_, Cand::kPhoton, i));

  for (Int_t i=0; i < tree_.nMu ; ++i) 
    muons_  .push_back(new LeafCand(tree_, Cand::kMuon  , i));
}

/**
 * Photon getter.
 */
VgEvent::Collection const &
VgEvent::photons() const
{
  return photons_;
}

/**
 * Muon getter.
 */
VgEvent::Collection const &
VgEvent::muons() const
{
  return muons_;
}
