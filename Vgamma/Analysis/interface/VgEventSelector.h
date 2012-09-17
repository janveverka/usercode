/**
 * \class VgEventSelector
 * 
 * \brief Applies the selection to the given event.
 * 
 * \author Jan Veverka, Caltech
 * \date 16 September 2012.
 */
#ifndef Vgamma_Analysis_interface_VgEventSelector_h
#define Vgamma_Analysis_interface_VgEventSelector_h

#include "boost/shared_ptr.hpp"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "PhysicsTools/SelectorUtils/interface/Selector.h"
#include "Vgamma/Analysis/interface/VgEvent.h"

//_____________________________________________________________________
namespace cit {
  
  class VgEventSelector : public Selector<VgEvent> {
  public:
    typedef edm::ParameterSet PSet;
    /// Ctor and dtor
    VgEventSelector(PSet const &);
    ~VgEventSelector();
    /// Selection interface
    using Selector<VgEvent>::operator();
    bool operator()(VgEvent const &, pat::strbitset &);
    /// Accessor(s)
    VgEvent const & selectedEvent() const;
  private:
    PSet const & cfg_;
    boost::shared_ptr<VgEvent> selectedEvent_;
  }; // class VgEventSelector
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_interface_VgEventSelector_h
