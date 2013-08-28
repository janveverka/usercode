/**
 * CorrectionApplicator.h - definition of the \class CorrectionApplicator
 *
 * Facilitates the application of the Q-Q corrections
 * to the photon ID MVA input variables.  Reads a tree
 * on the input and creates a new tree on the output.
 * The new tree contains both raw and corrected variables
 * used as the ID MVA inputs.  It also includes the ID MVA
 * value for both raw and corrected inputs.
 *
 * TODO:
 *    o Factor out the input chain stuff (config, init) in a separate class
 *    o Ditto for the output tree
 *    o Ditto for the BDT?
 * Jan Veverka, MIT, jan.veverka@cern.ch
 * 04 August 2013.
 */
#ifndef FWLite_Hgg_CorrectionApplicator_h
#define FWLite_Hgg_CorrectionApplicator_h

#include <string>
#include <vector>
#include <boost/shared_ptr.hpp>
#include "TChain.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWLite/Tools/interface/FlatChainSource.h"



//______________________________________________________________________________
namespace mit {
  namespace hgg {
    namespace correction_applicator {

      /// Forward declarations
      class Configuration;
      namespace configuration {
        class Inputs;
        class Outputs;
        class MaxEntries;
      } // namespace configuration
      
    } // namespace correction_applicator

    //__________________________________________________________________________
    class CorrectionApplicator {
    public:
      typedef edm::ParameterSet PSet;
      typedef boost::shared_ptr<PSet> PSetPtr;
      typedef correction_applicator::Configuration Configuration;
      /// 1st-level decomposition
      CorrectionApplicator(PSetPtr);
      ~CorrectionApplicator();
      void run();
    private:
      /// 2nd-level decomposition
      void initialize();
      void beginRun();
      void loopOverEntries();
      void endRun();
      /// 3rd-level decomposition
      void initializeInputs();
      void initializeOutputs();
      void initializeCorrectors();
      void initializePhotonIdMVAs();
      void reportEntry(Long64_t ientry, Long64_t entriesToProcess);
      void processEntry();
      /// Data members
      boost::shared_ptr<Configuration> process_;
      boost::shared_ptr<TChain> ichain_;
      fwlite::tools::FlatChainSource input_;
    }; // class CorrectionApplicator


    //__________________________________________________________________________
    /// Provides interface to the configuration
    class correction_applicator::Configuration {
    public:
      typedef edm::ParameterSet PSet;
      typedef boost::shared_ptr<PSet> PSetPtr;
      typedef boost::shared_ptr<configuration::Inputs> InputsPtr;
      typedef boost::shared_ptr<configuration::MaxEntries> MaxEntriesPtr;
      /// 2nd-level decomposition
      Configuration(PSetPtr source);
      ~Configuration() {}
      InputsPtr inputs() const {return inputs_;}
      MaxEntriesPtr maxEntries() const {return maxEntries_;}
      // PSetPtr source() {return source_;};
      // boost_shared
    private:
      /// 3rd-level decomposition
      void initialize();
      /// 4th-level decomposition
/*      void parseInputs();
      void parseOutputs();
      void parsePhotonIdMVA();*/
      /// Data members
      PSetPtr source_;
      InputsPtr inputs_;
      MaxEntriesPtr maxEntries_;
    }; // class correction_applicator::Configuration


    //__________________________________________________________________________
    /// Provides interface to the option section of the configuration.
    class correction_applicator::configuration::MaxEntries {
    public:
      typedef edm::ParameterSet PSet;
      MaxEntries(Long64_t toProcess, Long64_t reportEvery);
      void parse(PSet const& cfg);
      Long64_t toProcess  () const {return toProcess_  ;}
      Long64_t reportEvery() const {return reportEvery_;}
    private:
      Long64_t toProcess_;
      Long64_t reportEvery_;
    }; // class correction_applicator::configuration::Option


    //__________________________________________________________________________
    /// Provides interface to the inputs section of the configuration.
    class correction_applicator::configuration::Inputs {
    public:
      typedef edm::ParameterSet PSet;
      typedef std::vector<std::string> vstring;
      Inputs(PSet const& cfg);
      vstring const& fileNames() const {return fileNames_;}
      std::string const& treeName() const {return treeName_;}
    private:
      vstring  fileNames_;
      std::string treeName_;
    }; // class correction_applicator::configuration::Inputs

  } // namespace hgg
} // namespace mit

#endif // ifndef FWLite_Hgg_CorrectionApplicator_h
