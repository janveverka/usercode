/**
 * \brief Implementation of the VgMuon class.
 * \author Jan Veverka, Caltech
 * \date 22 September 2012
 */

#include <iostream>
#include <sstream>
#include "TMath.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "Vgamma/Analysis/interface/VgMuon.h"

using cit::VgMuon;

const double VgMuon::kCombIsoEffectiveArea = TMath::Pi() * 0.3 * 0.3;

//______________________________________________________________________________
/**
 * Copy ctor.
 */
VgMuon::VgMuon(VgLeafCandidate const & other) :
  VgLeafCandidate(other)
{
  if (other.type() != kMuon) {
    std::ostringstream msg(std::ostringstream::out);
    msg << "VgMuon::VgMuon(VgLeafCandidate const & other): other must "
	<< " be of ParticleType::kMuon; got: " << other.type();
    throw cms::Exception("BadMuon") << msg.str();
  }
}


//______________________________________________________________________________
/**
 * Default ctor.
 */
VgMuon::VgMuon() :
  VgLeafCandidate()
{}

