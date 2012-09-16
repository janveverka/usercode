/**
 * \class VgMuonHistoFiller
 * 
 * \brief Fills muon Vgamma histograms.
 * 
 * \author Jan Veverka, Caltech 
 * \date 08 September 2012
 */
#ifndef Vgamma_Analysis_VgMuonHistoFiller_h
#define Vgamma_Analysis_VgMuonHistoFiller_h

#include "Vgamma/Analysis/interface/VgHistoFillerBase.h"

//_____________________________________________________________________
namespace cit {
  
  class VgMuonHistoFiller : public VgHistoFillerBase {
  public:
    VgMuonHistoFiller(VgAnalyzerTree const& tree,
                      HistoCollection & histos);
    ~VgMuonHistoFiller();
    void bookHistograms();
    void fillHistograms(VgEvent const&);
    void fillCand(Cand const&);
  }; // class VgMuonHistoFiller
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_VgMuonHistoFiller_h
