/**
 * \class VgMuon
 * 
 * \brief Represents a muon in the Vgamma analysis.
 * Derives from the VgLeafCandidate and adds methods for isolation
 * calculation etc.
 * 
 * \author Jan Veverka, Caltech
 * \date 22 September 2012.
 */

#ifndef Vgamma_Analysis_interface_VgMuon_h
#define Vgamma_Analysis_interface_VgMuon_h

#include "Vgamma/Analysis/interface/VgLeafCandidate.h"

namespace cit {
  class VgMuon : public VgLeafCandidate {
  public:
    /// Static isolation data
    static const double kCombIsoEffectiveArea;

    /// Ctor and dtor
    VgMuon(VgLeafCandidate const &);
    VgMuon();
    ~VgMuon() {}

    /// Muon specific accessors
    bool isGlobalMuon() const {return tree().muType[key()] & (1<<1);}
    double trackIso() const {return tree().muIsoTrk[key()];}
    double ecalIso() const {return tree().muIsoEcal[key()];}
    double hcalIso() const {return tree().muIsoHcal[key()];}
    double combEA() const {return kCombIsoEffectiveArea;}
    
    double combIso() const {
      return trackIso() + ecalIso() + hcalIso() - rho() * combEA();
    }
    
    double combRelIso() const {return combIso() / pt();}

  }; // class VgMuon

} // namespace cit

#endif // #define Vgamma_Analysis_interface_VgMuon_h

