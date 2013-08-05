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
    namespace correction_applicator {
      /// Forward declarations
      class Configuration;
      // typedef boost::shared_ptr<Configuration> ConfigPtr;
      typedef edm::ParameterSet PSet;
      typedef boost::shared_ptr<PSet> PSetPtr;
    } // namespace correction_applicator

    using correction_applicator::Configuration;
    using correction_applicator::PSetPtr;
    
    //_________________________________________________________________
    class CorrectionApplicator {
    public:
      CorrectionApplicator(PSetPtr);
      ~CorrectionApplicator();
      void run();
    protected:
      void initialize();
      void beginRun();
      void loopOverEvents();
      void endRun();
      Configuration *cfg_;
    }; // class CorrectionApplicator

    //_______________________________________________________________
    class correction_applicator::Configuration {
    public:
      Configuration(PSetPtr cfg) {source_ = cfg;}
      ~Configuration() {}
      PSetPtr getSource() {return source_;};
    private:
      PSetPtr source_;
    }; // class correction_applicator::Configuration

  } // namespace hgg
} // namespace mit

#endif // ifndef FWLite_Hgg_CorrectionApplicator_h
