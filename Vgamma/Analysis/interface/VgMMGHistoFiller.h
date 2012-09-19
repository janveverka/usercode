/**
 * \class VgMMGHistoFiller
 * 
 * \brief Fills mumugamma candidate Vgamma histograms.
 * 
 * \author Jan Veverka, Caltech 
 * \date 19 September 2012
 */
#ifndef Vgamma_Analysis_interface_VgMMGHistoFiller_h
#define Vgamma_Analysis_interface_VgMMGHistoFiller_h

#include "Vgamma/Analysis/interface/VgHistoFillerBase.h"
#include "Vgamma/Analysis/interface/VgCombinedCandidate.h"

//_____________________________________________________________________
namespace cit {
  
  class VgMMGHistoFiller : public VgHistoFillerBase {
  public:
    VgMMGHistoFiller(VgAnalyzerTree const & tree,
                        HistoCollection & histos);
    ~VgMMGHistoFiller();
    void bookHistograms();
    void fillHistograms(VgEvent const&);
    void fillCand(VgCombinedCandidate const&);
  }; // class VgMMGHistoFiller
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_interface_VgMMGHistoFiller_h
