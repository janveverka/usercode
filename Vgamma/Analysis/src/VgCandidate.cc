/**
 * \brief Class Implementation
 * \author Jan Veverka
 * \date 15 September 2008
 */
#include "Vgamma/Analysis/interface/VgCandidate.h"

using cit::VgCandidate;

//______________________________________________________________________________
/// Default Ctor implementation
VgCandidate::VgCandidate() : 
  momentum_(0, 0, 0, 0), 
  type_(kCombined), 
  weight_(1.) 
{}

