/**
 * \brief Implementation of the VgPhoton class.
 * \author Jan Veverka, Caltech
 * \date 22 September 2012
 */

#include <iostream>
#include <sstream>
#include "FWCore/Utilities/interface/Exception.h"
#include "Vgamma/Analysis/interface/VgPhoton.h"

using cit::VgPhoton;

const double VgPhoton::EffectiveArea::Barrel::kTracker = 0.0167;
const double VgPhoton::EffectiveArea::Barrel::kEcal    = 0.183 ;
const double VgPhoton::EffectiveArea::Barrel::kHcal    = 0.062 ;

const double VgPhoton::EffectiveArea::Endcaps::kTracker = 0.032;
const double VgPhoton::EffectiveArea::Endcaps::kEcal    = 0.090;
const double VgPhoton::EffectiveArea::Endcaps::kHcal    = 0.180;

const double VgPhoton::PtSlope::kTracker = 0.001 ;
const double VgPhoton::PtSlope::kEcal    = 0.006 ;
const double VgPhoton::PtSlope::kHcal    = 0.0025;


//______________________________________________________________________________
/**
 * Copy ctor.
 */
VgPhoton::VgPhoton(VgLeafCandidate const & other) :
  VgLeafCandidate(other)
{
  if (other.type() != kPhoton) {
    std::ostringstream msg(std::ostringstream::out);
    msg << "VgPhoton::VgPhoton(VgLeafCandidate const & other): other must "
	<< " be of ParticleType::kPhoton; got: " << other.type();
    throw cms::Exception("BadPhoton") << msg.str();
  }
}


//______________________________________________________________________________
/**
 * Default ctor.
 */
VgPhoton::VgPhoton() :
  VgLeafCandidate()
{}


