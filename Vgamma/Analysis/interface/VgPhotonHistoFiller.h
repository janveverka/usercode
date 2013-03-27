/**
 * \class VgPhotonHistoFiller
 * 
 * \brief Fills photon Vgamma histograms.
 * 
 * \author Jan Veverka, Caltech 
 * \date 08 September 2012
 */
#ifndef Vgamma_Analysis_VgPhotonHistoFiller_h
#define Vgamma_Analysis_VgPhotonHistoFiller_h

#include "Vgamma/Analysis/interface/VgHistoFillerBase.h"

//_____________________________________________________________________
namespace cit {
  
  class VgPhotonHistoFiller : public VgHistoFillerBase {
  public:
    VgPhotonHistoFiller();
    ~VgPhotonHistoFiller();
    virtual void bookHistograms();
    virtual void fillHistograms(VgEvent const&);
    virtual void fillCand(VgLeafCandidate const &, double);
  }; // class VgPhotonHistoFiller
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_VgPhotonHistoFiller_h
