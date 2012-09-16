/**
 * \class VgMCPileupHistoFiller
 * 
 * \brief Fills MC-only pileup Vgamma histograms.
 * 
 * \author Jan Veverka, Caltech 
 * \date 08 September 2012
 */
#ifndef Vgamma_Analysis_VgMCPileupHistoFiller_h
#define Vgamma_Analysis_VgMCPileupHistoFiller_h

#include "Vgamma/Analysis/interface/VgHistoFillerBase.h"

//_____________________________________________________________________
namespace cit {
  
  class VgMCPileupHistoFiller : public VgHistoFillerBase {
  public:
    VgMCPileupHistoFiller(VgAnalyzerTree const& tree,
                        HistoCollection & histos);
    ~VgMCPileupHistoFiller();
    void bookHistograms();
    void fillHistograms(VgEvent const&);
  }; // class VgMCPileupHistoFiller
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_VgMCPileupHistoFiller_h
