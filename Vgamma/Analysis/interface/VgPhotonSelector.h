/**
 * \class VgPhotonSelector
 * 
 * \brief Applies the selection to a given photon.
 * 
 * \author Jan Veverka, Caltech
 * \date 18 September 2012.
 */
#ifndef Vgamma_Analysis_interface_VgPhotonSelector_h
#define Vgamma_Analysis_interface_VgPhotonSelector_h

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "PhysicsTools/SelectorUtils/interface/Selector.h"
#include "PhysicsTools/SelectorUtils/interface/strbitset.h"
#include "Vgamma/Analysis/interface/VgLeafCandidate.h"

//_____________________________________________________________________
namespace cit {
  
  class VgPhotonSelector : public Selector<VgLeafCandidate> {
  public:
    typedef edm::ParameterSet PSet;
    enum IsolationType {kIsoTracker, kIsoEcal, kIsoHcal};
    /// Ctor and dtor
    VgPhotonSelector(PSet const &);
    ~VgPhotonSelector();
    /// Selection interface
    using Selector<VgLeafCandidate>::operator();
    bool operator()(VgLeafCandidate const &, pat::strbitset &);
    /// Other methods
    double effectiveArea(double scAbsEta, IsolationType type) const;
    /// Static data
    static const double kBarrelIsoEffectiveAreaTracker ;
    static const double kBarrelIsoEffectiveAreaEcal    ;
    static const double kBarrelIsoEffectiveAreaHcal    ;
    static const double kEndcapsIsoEffectiveAreaTracker;
    static const double kEndcapsIsoEffectiveAreaEcal   ;
    static const double kEndcapsIsoEffectiveAreaHcal   ;
    static const double kIsoPtSlopeTracker             ;
    static const double kIsoPtSlopeEcal                ;
    static const double kIsoPtSlopeHcal                ;
  private:
    void init(
      const double &, // 1. minimum photon pt
      const double &, // 2. minimum supercluster pseudorapidity |eta|
      const double &, // 3. maximum supercluster pseudorapidity |eta|
      const double &, // 4. maximum shower width
      const int    &, // 5. has pixel match
      const double &, // 6. maximum tracker isolation
      const double &, // 7. maximum ECAL isolation
      const double & // 8. maximum HCAL isolation
    );
  }; // class VgPhotonSelector
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_interface_VgPhotonSelector_h
