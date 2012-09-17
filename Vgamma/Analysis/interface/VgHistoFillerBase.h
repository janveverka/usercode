/**
 * Definition of the VgHistoFillerBase class.
 * 
 * Base class for various HistoFillers that book and fill 
 * groups of related histograms, e.g. muon quantities, photon quantities,
 * etc.
 * 
 * Jan Veverka, Caltech, 08 September 2012.
 */
#ifndef Vgamma_Analysis_VgHistoFillerBase_h
#define Vgamma_Analysis_VgHistoFillerBase_h

#include <map>
#include <string>
#include "TH1.h"

#include "Vgamma/Analysis/interface/VgAnalyzerTree.h"
#include "Vgamma/Analysis/interface/VgEvent.h"

//_____________________________________________________________________
namespace cit {
  class VgHistoFillerBase {
  public:
    typedef std::map<std::string, TH1*> HistoCollection;

    VgHistoFillerBase(VgAnalyzerTree const & tree,
                      HistoCollection & histos) :
      tree_(&tree),
      histos_(histos) //,
      // collection_(0)
    {}
    
    ~VgHistoFillerBase() {}
    virtual void bookHistograms() = 0;
    virtual void fillHistograms(VgEvent const&) = 0;
  protected:    
    VgAnalyzerTree const * tree_;
    HistoCollection &      histos_;
  }; // class VgHistoFillerBase
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_VgHistoFillerBase_h
