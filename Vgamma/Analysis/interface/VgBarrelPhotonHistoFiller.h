/**
 * \class VgBarrelPhotonHistoFiller
 * 
 * \brief Fills barrel photon Vgamma histograms.
 * 
 * \author Jan Veverka, Caltech 
 * \date 23 September 2012
 */
#ifndef Vgamma_Analysis_VgBarrelPhotonHistoFiller_h
#define Vgamma_Analysis_VgBarrelPhotonHistoFiller_h

#include "Vgamma/Analysis/interface/VgPhotonHistoFiller.h"

//_____________________________________________________________________
namespace cit {
  
  class VgBarrelPhotonHistoFiller : public VgPhotonHistoFiller {
  public:
    VgBarrelPhotonHistoFiller();
    ~VgBarrelPhotonHistoFiller();
    void bookHistograms();
    void fillHistograms(VgEvent const&);
//     void fillCand(VgLeafCandidate const &);
  }; // class VgBarrelPhotonHistoFiller
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_VgBarrelPhotonHistoFiller_h
