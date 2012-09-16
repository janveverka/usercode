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
#include <boost/ptr_container/ptr_vector.hpp>
#include "Vgamma/Analysis/interface/VgAnalyzerTree.h"
#include "Vgamma/Analysis/interface/VgCandidate.h"

//_____________________________________________________________________
namespace cit {
  
  class VgEvent {
  public:
    typedef boost::ptr_vector<VgCandidate> Collection;
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
