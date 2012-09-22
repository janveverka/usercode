/**
 * \class VgPileupHistoFiller
 * 
 * \brief Fills pileup Vgamma histograms common for data and MC.
 * 
 * \author Jan Veverka, Caltech 
 * \date 08 September 2012
 */
#ifndef Vgamma_Analysis_interface_VgPileupHistoFiller_h
#define Vgamma_Analysis_interface_VgPileupHistoFiller_h

#include "Vgamma/Analysis/interface/VgHistoFillerBase.h"

//_____________________________________________________________________
namespace cit {
  
  class VgPileupHistoFiller : public VgHistoFillerBase {
  public:
    VgPileupHistoFiller();
    ~VgPileupHistoFiller();
    void bookHistograms();
    void fillHistograms(VgEvent const&);
  }; // class VgPileupHistoFiller
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_interface_VgPileupHistoFiller_h
