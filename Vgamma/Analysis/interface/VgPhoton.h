/**
 * \class VgPhoton
 * 
 * \brief Represents a photon in the Vgamma analysis.
 * Derives from the VgLeafCandidate and adds methods for isolation
 * calculation.
 * 
 * \author Jan Veverka, Caltech
 * \date 22 September 2012.
 */

#ifndef Vgamma_Analysis_interface_VgPhoton_h
#define Vgamma_Analysis_interface_VgPhoton_h

#include <math.h>
#include "Vgamma/Analysis/interface/VgLeafCandidate.h"

namespace cit {
  class VgPhoton : public VgLeafCandidate {
  public:
    /// Static isolation data
    struct EffectiveArea {
      struct Barrel {
	static const double kTracker;
	static const double kEcal;
	static const double kHcal;
      }; // struct Barrel
      struct Endcaps {
	static const double kTracker;
	static const double kEcal;
	static const double kHcal;
      }; // struct Endcaps
    }; // struct EffectiveArea

    struct PtSlope {
      static const double kTracker;
      static const double kEcal;
      static const double kHcal;
    }; // struct PhotonPtSlope

    /// Ctor and dtor
    VgPhoton(VgLeafCandidate const &);
    VgPhoton();
    ~VgPhoton() {}

    /// Photon specific accessors
    double scEta() const {return tree().phoSCEta[key()];}
    double scAbsEta() const {return fabs(scEta());}
    bool isInBarrel() const {return scAbsEta() < 1.5;}

    double trackEA() const {
      return isInBarrel() ? EffectiveArea::Barrel ::kTracker :
                            EffectiveArea::Endcaps::kTracker ;
    }

    double ecalEA() const {
      return isInBarrel() ? EffectiveArea::Barrel ::kEcal :
                            EffectiveArea::Endcaps::kEcal ;
    }

    double hcalEA() const {
      return isInBarrel() ? EffectiveArea::Barrel ::kHcal :
                            EffectiveArea::Endcaps::kHcal ;
    }

    double trackIsoRaw() const {
      return tree().phoTrkIsoHollowDR04[key()] - PtSlope::kTracker * pt();
    }

    double ecalIsoRaw() const {
      return tree().phoEcalIsoDR04[key()] - PtSlope::kEcal * pt();
    }

    double hcalIsoRaw() const {
      return tree().phoHcalIsoDR04[key()] - PtSlope::kHcal * pt();
    }

    double trackIso() const {return trackIsoRaw() - rho() * trackEA();}
    double ecalIso() const {return ecalIsoRaw() - rho() * ecalEA();}
    double hcalIso() const {return hcalIsoRaw() - rho() * hcalEA();}

  }; // class VgPhoton

} // namespace cit

#endif // #define Vgamma_Analysis_interface_VgPhoton_h

