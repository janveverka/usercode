/**
 * \class VgEvent
 * 
 * \brief Holds data Z->mmg event data for the VgHistoManager.
 * Specifies candidates whose quantities will be filled in histograms.
 * 
 * \author Jan Veverka, Caltech 
 * \date 08 September 2012
 */
#ifndef Vgamma_Analysis_VgEvent_h
#define Vgamma_Analysis_VgEvent_h

#include <vector>
#include "Vgamma/Analysis/interface/VgAnalyzerTree.h"

//_____________________________________________________________________
namespace cit {
  
  class VgEvent {
  public:
    typedef std::vector<UInt_t> Collection;
    VgEvent(VgAnalyzerTree const&);
    ~VgEvent();
    Collection const & muons() const;
    Collection const & photons() const;
    void read();
  private:
    VgAnalyzerTree const & tree_;
    Collection photons_;
    Collection muons_;
  }; // class VgEvent
  
} // namespace cit


#endif // #ifndef Vgamma_Analysis_VgEvent_h
