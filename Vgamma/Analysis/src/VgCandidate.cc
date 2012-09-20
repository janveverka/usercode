/**
 * \brief Class Implementation
 * \author Jan Veverka
 * \date 15 September 2008
 */
#include "Vgamma/Analysis/interface/VgCandidate.h"

using cit::VgCandidate;


//______________________________________________________________________________
/// Default ctor implementation
VgCandidate::VgCandidate() : 
  momentum_(0, 0, 0, 0), 
  type_(kCombined), 
  weight_(1.),
  charge_(0)
{} // Default ctor


//______________________________________________________________________________
/// Copy ctor
VgCandidate::VgCandidate(VgCandidate const & other) : 
  momentum_(other.momentum_), 
  type_(other.type_), 
  weight_(other.weight_),
  charge_(other.charge_)
{} // Copy ctor


//______________________________________________________________________________
/// Checks if this candidate is equal to the other.
bool
VgCandidate::operator==(VgCandidate const & other) const
{
  return (momentum_ == other.momentum() &&
          type_ == other.type() &&
          weight_ == other.weight() &&
          charge_ == other.charge());
}
// bool
// VgCandidate::operator==(VgCandidate const & other)
