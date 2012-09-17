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
  weight_(1.) 
{} // Default ctor

//______________________________________________________________________________
/// Copy ctor
VgCandidate::VgCandidate(VgCandidate const & other) : 
  momentum_(other.momentum_), 
  type_(other.type_), 
  weight_(other.weight_) 
{} // Copy ctor

