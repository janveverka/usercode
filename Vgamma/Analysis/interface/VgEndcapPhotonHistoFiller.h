/**
 * \class VgEndcapPhotonHistoFiller
 * 
 * \brief Fills barrel photon Vgamma histograms.
 * 
 * \author Jan Veverka, Caltech 
 * \date 23 September 2012
 */
#ifndef Vgamma_Analysis_VgEndcapPhotonHistoFiller_h
#define Vgamma_Analysis_VgEndcapPhotonHistoFiller_h

#include "Vgamma/Analysis/interface/VgPhotonHistoFiller.h"

//_____________________________________________________________________
namespace cit {
  
  class VgEndcapPhotonHistoFiller : public VgPhotonHistoFiller {
  public:
    VgEndcapPhotonHistoFiller();
    ~VgEndcapPhotonHistoFiller();
    void bookHistograms();
    void fillHistograms(VgEvent const&);
//     void fillCand(VgLeafCandidate const &);
  }; // class VgEndcapPhotonHistoFiller
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_VgEndcapPhotonHistoFiller_h
