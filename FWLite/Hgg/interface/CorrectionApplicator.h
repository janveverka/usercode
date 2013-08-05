/**
 * Definition of the CorrectionApplicator class.
 * 
 * Facilitates the application of the Q-Q corrections
 * to the photon ID MVA input variables.  Reads a tree
 * on the input and creates a new tree on the output.
 * The new tree contains both raw and corrected variables
 * used as the ID MVA inputs.  It also includes the ID MVA
 * value for both raw and corrected inputs.
 * 
 * Jan Veverka, MIT, jan.veverka@cern.ch
 * 04 August 2013.
 */
#ifndef FWLite_Hgg_CorrectionApplicator_h
#include <boost/shared_ptr.hpp>
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#define FWLite_Hgg_CorrectionApplicator_h

//_____________________________________________________________________
namespace mit {
  namespace hgg {
    class CorrectionApplicator {
    public:
      typedef edm::ParameterSet PSet;
      typedef boost::shared_ptr<PSet> PSetPtr;
      CorrectionApplicator(PSetPtr);
      ~CorrectionApplicator();
      void run();
    protected:
      void initialize();
      void beginRun();
      void loopOverEvents();
      void endRun();
      PSetPtr cfg_;
    }; // class CorrectionApplicator    
  } // namespace hgg
} // namespace mit

#endif // ifndef FWLite_Hgg_CorrectionApplicator_h
