/**
 * Definition of the VgHistoFillerBase class.
 * 
 * Base class for various HistoFillers that book and fill 
 * groups of related histograms, e.g. muon quantities, photon quantities,
 * etc.
 * 
 * Jan Veverka, Caltech, 08 September 2012.
 */
#ifndef Vgamma_Analysis_interface_VgHistoFillerBase_h
#define Vgamma_Analysis_interface_VgHistoFillerBase_h

#include <map>
#include <string>
#include "TH1.h"

#include "Vgamma/Analysis/interface/VgEvent.h"

//_____________________________________________________________________
namespace cit {
  class VgHistoFillerBase {
  public:
    typedef std::map<std::string, TH1*> HistoCollection;

    VgHistoFillerBase() {}    
    ~VgHistoFillerBase() {}
    virtual void bookHistograms() = 0;
    virtual void fillHistograms(VgEvent const&) = 0;
  protected:    
    HistoCollection        histos_;
  }; // class VgHistoFillerBase
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_interface_VgHistoFillerBase_h
