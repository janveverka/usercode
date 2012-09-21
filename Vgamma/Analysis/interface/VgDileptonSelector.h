/**
 * \class VgDileptonSelector
 * 
 * \brief Applies the selection to the given dimuon.
 * 
 * \author Jan Veverka, Caltech
 * \date 19 September 2012.
 */
#ifndef Vgamma_Analysis_interface_VgDileptonSelector_h
#define Vgamma_Analysis_interface_VgDileptonSelector_h

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "PhysicsTools/SelectorUtils/interface/Selector.h"
#include "PhysicsTools/SelectorUtils/interface/strbitset.h"
#include "Vgamma/Analysis/interface/VgCombinedCandidate.h"

//_____________________________________________________________________
namespace cit {
  
  class VgDileptonSelector : public Selector<VgCombinedCandidate> {
  public:
    typedef edm::ParameterSet PSet;
    /// Ctor and dtor
    VgDileptonSelector(PSet const &);
    ~VgDileptonSelector();
    /// Selection interface
    using Selector<VgCombinedCandidate>::operator();
    bool operator()(VgCombinedCandidate const &, pat::strbitset &);
  private:
    void init(const int & charge, const double & minMass);
  }; // class VgDileptonSelector
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_interface_VgDileptonSelector_h
