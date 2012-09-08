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

//_____________________________________________________________________
namespace cit {
  class VgHistoFillerBase {
  public:
    typedef std::map<std::string, TH1*> HistoCollection;

    VgHistoFillerBase(VgAnalyzerTree const& tree,
                      HistoCollection & histos,
                      const Int_t * numObjects = 0) :
      tree_(tree),
      histos_(histos),
      numObjects_(numObjects)
    {}
    
    ~VgHistoFillerBase() {}
    virtual void bookHistograms() = 0;
    virtual void fillHistograms() = 0;
  protected:
    virtual void fillObjectWithIndex(UInt_t) = 0;

    virtual void loopOverObjects() {
      if (numObjects_ != 0)
        for (Int_t index = 0; index < *numObjects_; ++index)
          fillObjectWithIndex(index);
    } // loopOverObjects(..)
    
    VgAnalyzerTree const & tree_;
    HistoCollection &      histos_;
    const Int_t    *       numObjects_;
  }; // class VgHistoFillerBase
  
} // namespace cit

#endif // #ifndef Vgamma_Analysis_VgHistoFillerBase_h
