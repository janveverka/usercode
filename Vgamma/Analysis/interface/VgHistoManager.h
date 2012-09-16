/**
 * Definition of the VgHistoManager class.
 * 
 * Holds pointers to all histograms and calls HistoFillers.
 * 
 * Jan Veverka, Caltech, 08 September 2012.
 */
#ifndef Vgamma_Analysis_VgHistoManager_h
#define Vgamma_Analysis_VgHistoManager_h

#include <map>
#include <string>
#include "TDirectory.h"
#include "TH1.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "Vgamma/Analysis/interface/VgAnalyzerTree.h"
#include "Vgamma/Analysis/interface/VgHistoFillerBase.h"


//_____________________________________________________________________
namespace cit {
  
  class VgHistoManager {
  public:
    typedef edm::ParameterSet PSet;
    typedef std::vector<VgHistoFillerBase*> VgHistoFillerCollection;

    VgHistoManager(VgAnalyzerTree const&, TDirectory&, PSet const&,
                   bool);
    ~VgHistoManager();
    void bookHistograms();
    void fillHistograms(VgEvent const&);
  private:
    VgHistoFillerCollection fillers_;
    VgHistoFillerBase::HistoCollection histos_;
    PSet const & cfg_;
    bool isMC_;
  }; // class VgHistoManager
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_VgHistoManager_h
