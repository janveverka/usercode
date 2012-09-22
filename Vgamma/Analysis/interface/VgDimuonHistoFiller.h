/**
 * \class VgDimuonHistoFiller
 * 
 * \brief Fills dimuon Vgamma histograms.
 * 
 * \author Jan Veverka, Caltech 
 * \date 19 September 2012
 */
#ifndef Vgamma_Analysis_interface_VgDimuonHistoFiller_h
#define Vgamma_Analysis_interface_VgDimuonHistoFiller_h

#include "Vgamma/Analysis/interface/VgHistoFillerBase.h"
#include "Vgamma/Analysis/interface/VgCombinedCandidate.h"

//_____________________________________________________________________
namespace cit {
  
  class VgDimuonHistoFiller : public VgHistoFillerBase {
  public:
    VgDimuonHistoFiller();
    ~VgDimuonHistoFiller();
    void bookHistograms();
    void fillHistograms(VgEvent const&);
    void fillCand(VgCombinedCandidate const&);
  }; // class VgDimuonHistoFiller
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_interface_VgDimuonHistoFiller_h
