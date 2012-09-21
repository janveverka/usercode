/**
 * \class VgMuonSelector
 * 
 * \brief Applies the selection to the given muon.
 * 
 * \author Jan Veverka, Caltech
 * \date 18 September 2012.
 */
#ifndef Vgamma_Analysis_interface_VgMuonSelector_h
#define Vgamma_Analysis_interface_VgMuonSelector_h

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "PhysicsTools/SelectorUtils/interface/Selector.h"
#include "PhysicsTools/SelectorUtils/interface/strbitset.h"
#include "Vgamma/Analysis/interface/VgLeafCandidate.h"

//_____________________________________________________________________
namespace cit {
  
  class VgMuonSelector : public Selector<VgLeafCandidate> {
  public:
    typedef edm::ParameterSet PSet;
    /// Ctor and dtor
    VgMuonSelector(PSet const &);
    ~VgMuonSelector();
    /// Selection interface
    using Selector<VgLeafCandidate>::operator();
    bool operator()(VgLeafCandidate const &, pat::strbitset &);
  private:
    void init(
      //  1. minimum transverse momentum
      const double & minPt         ,
      //  2. maximum pseudo-rapidity absolute value
      const double & maxAbsEta     ,
      //  3. muon is reconstructed as a "global muon" (out-in fit)
      const int    & isGlobalMuon  ,
      //  4. maximum global muon fit normalized chi2
      const double & maxNormChi2   ,
      //  5. minimum number of valid muon chamber hits matched to the 
      //     global fit
      const int    & minChamberHits,
      //  6. minimum number of muon stations with matched segments
      //     (global track: out-in fit)
      const int    & minStations   ,
      //  7. maximum inner track transverse impact parameter w.r.t the vertex
      //     absolute value
      const double & maxAbsDxy     ,
      //  8. maximum inner track transverse impact parameter w.r.t the vertex
      //     absolute value
      const double & maxAbsDz      ,
      //  9. minimum number of pixel hits
      const int    & minPixelHits  ,
      // 10. minimum number of tracker (pixels + strips) hits
      const int    & minTkHits     ,
      // 11. Sum of the Tracker, ECAL and HCAL isolations
      //     within a cone of DR < 0.3 around  the muon direction
      //     (vetoing a cone of 0.015 around that direction for the tracker
      //     isloation) divided by muon pt.
      const double & maxCombRelIso
    );
  }; // class VgMuonSelector
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_interface_VgMuonSelector_h
