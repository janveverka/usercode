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

#include <iostream>
#include "boost/shared_ptr.hpp"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "PhysicsTools/SelectorUtils/interface/Selector.h"
#include "Vgamma/Analysis/interface/VgEvent.h"
#include "Vgamma/Analysis/interface/VgMuonSelector.h"
#include "Vgamma/Analysis/interface/VgPhotonSelector.h"
#include "Vgamma/Analysis/interface/VgDimuonSelector.h"

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
    /// Summary output
    void printCutflows(std::ostream &) const;
  private:
    void init(
      const bool &, // 1. Select muons
      const bool &, // 2. Select dimuon
      const bool &  // 3. Select photon
    );
    void selectMuons();
    void selectPhotons();
    void selectDimuons();
    boost::shared_ptr<VgEvent> selectedEvent_;
    VgMuonSelector passesMuonCuts_;
    VgDimuonSelector passesDimuonCuts_;
    VgPhotonSelector passesPhotonCuts_;
  }; // class VgEventSelector
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_interface_VgEventSelector_h
