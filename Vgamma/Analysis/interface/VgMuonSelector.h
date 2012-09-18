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
      // 1. muon is reconstructed as a "global muon" (out-in fit)
      const int & isGlobalMuon,
      // 2. maximum global muon fit normalized chi2
      const double & maxNormChi2,
      // 3. minimum number of valid muon hits matched to the global fit
      const int & minMuonHits,
      // 4. muon is reconsturcted as a "tracker muon" (in-out fit)
      const int & isTrackerMuon
    );
    double   minPt_;
    double   maxAbsEta_;
    bool isGlobalMuon_;
    unsigned minPixelHits_;
  }; // class VgMuonSelector
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_interface_VgMuonSelector_h
