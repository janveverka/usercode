/**
 * \class VgDimuonSelector
 * 
 * \brief Applies the selection to the given dimuon.
 * 
 * \author Jan Veverka, Caltech
 * \date 19 September 2012.
 */
#ifndef Vgamma_Analysis_interface_VgDimuonSelector_h
#define Vgamma_Analysis_interface_VgDimuonSelector_h

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "PhysicsTools/SelectorUtils/interface/Selector.h"
#include "PhysicsTools/SelectorUtils/interface/strbitset.h"
#include "Vgamma/Analysis/interface/VgCombinedCandidate.h"

//_____________________________________________________________________
namespace cit {
  
  class VgDimuonSelector : public Selector<VgCombinedCandidate> {
  public:
    typedef edm::ParameterSet PSet;
    /// Ctor and dtor
    VgDimuonSelector(PSet const &);
    ~VgDimuonSelector();
    /// Selection interface
    using Selector<VgCombinedCandidate>::operator();
    bool operator()(VgCombinedCandidate const &, pat::strbitset &);
  private:
    void init(const double & minMass);
  }; // class VgDimuonSelector
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_interface_VgDimuonSelector_h
