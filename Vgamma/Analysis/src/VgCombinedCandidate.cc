/**
 * \class VgCombinedCandidate
 * \brief Class Implementation
 * \author Jan Veverka
 * \date 18 September 2008
 */
#include <assert.h>
#include <iostream>
#include "FWCore/Utilities/interface/Exception.h"
#include "Vgamma/Analysis/interface/VgCombinedCandidate.h"

using cit::VgCombinedCandidate;

typedef cms::Exception Bad;

//______________________________________________________________________________
/// Default Ctor 
VgCombinedCandidate::VgCombinedCandidate()
{}
// Default ctor


//______________________________________________________________________________
/// Copy Ctor 
VgCombinedCandidate::VgCombinedCandidate(VgCombinedCandidate const & other) : 
  VgCandidate(other)
{
  // Copy the daughters_
  daughters_.resize(other.daughters_.size());
  std::copy(other.daughters_.begin(), other.daughters_.end(), 
            daughters_.begin());
} // Copy ctor


//______________________________________________________________________________
void
VgCombinedCandidate::addDaughter(VgCandidate const & dau)
{
  switch (dau.type()) {
    case kElectron:
    case kMuon:
    case kPhoton:
      addDaughter(dynamic_cast<VgLeafCandidate const&>(dau));
      break;
    case kCombined:
      addDaughter(dynamic_cast<VgCombinedCandidate const&>(dau));
      break;
    default:
      /// This should never happen:
      throw Bad("BadParticleType") << "Unknown ParticleType: " << dau.type();
  } // switch (dau.type())
}
// void
// VgCombinedCandidate::addDaughter(VgCandidate const & dau)


//______________________________________________________________________________
void
VgCombinedCandidate::addDaughter(VgLeafCandidate const & dau)
{
  daughters_.push_back(dau);
  update();
}
// void
// VgCombinedCandidate::addDaughter(VgLeafCandidate const & dau)


//______________________________________________________________________________
void
VgCombinedCandidate::update()
{
  momentum_.SetPxPyPzE(0, 0, 0, 0);
  weight_ = 1.;
  charge_ = 0;
  for (VgLeafCandidates::const_iterator dau = daughters_.begin();
       dau != daughters_.end(); ++dau) {
    momentum_ += dau->momentum();
    weight_   *= dau->weight();
    charge_   += dau->charge();
  }
} // update(..)


//______________________________________________________________________________
void
VgCombinedCandidate::addDaughter(VgCombinedCandidate const & dau)
{
  for (VgLeafCandidates::const_iterator gdau = dau.daughters().begin();
       gdau != dau.daughters().end(); ++gdau) 
    daughters_.push_back(*gdau);
  update();
}
// void
// VgCombinedCandidate::addDaughter(VgCombinedCandidate const & dau)


//______________________________________________________________________________
bool
VgCombinedCandidate::operator==(VgCombinedCandidate const & other) const
{
  if (numDaughters() != other.numDaughters()) return false;

  for (unsigned i = 0; i < numDaughters(); ++i)
    if (!(daughter(i) == other.daughter(i))) return false;

  return VgCandidate::operator==(other); 
}
// bool
// VgCombinedCandidate::operator==(VgCombinedCandidate const & other)
