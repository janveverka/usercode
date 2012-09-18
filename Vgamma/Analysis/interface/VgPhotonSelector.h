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
    /// Ctor and dtor
    VgPhotonSelector(PSet const &);
    ~VgPhotonSelector();
    /// Selection interface
    using Selector<VgLeafCandidate>::operator();
    bool operator()(VgLeafCandidate const &, pat::strbitset &);
  private:
    void init(
      const double &, // 1. minimum photon pt      
      const double & // 2. maximum supercluster absolute pseudorapidity |eta|
    );
  }; // class VgPhotonSelector
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_interface_VgPhotonSelector_h
