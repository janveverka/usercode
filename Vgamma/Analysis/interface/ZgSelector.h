/**
 * \class ZgSelector
 * 
 * \brief Applies the selection to the given Z(ll)gamma candidate.
 * 
 * \author Jan Veverka, Caltech
 * \date 19 September 2012.
 */
#ifndef Vgamma_Analysis_interface_ZgSelector_h
#define Vgamma_Analysis_interface_ZgSelector_h

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "PhysicsTools/SelectorUtils/interface/Selector.h"
#include "PhysicsTools/SelectorUtils/interface/strbitset.h"
#include "Vgamma/Analysis/interface/VgCombinedCandidate.h"

//_____________________________________________________________________
namespace cit {
  
  class ZgSelector : public Selector<VgCombinedCandidate> {
  public:
    typedef edm::ParameterSet PSet;
    /// Ctor and dtor
    ZgSelector(PSet const &);
    ~ZgSelector();
    /// Selection interface
    using Selector<VgCombinedCandidate>::operator();
    bool operator()(VgCombinedCandidate const &, pat::strbitset &);
  private:
    void init(const double & minDeltaR);
  }; // class ZgSelector
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_interface_ZgSelector_h
