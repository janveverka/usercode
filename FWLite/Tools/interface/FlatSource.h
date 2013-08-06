/**
 * \file  FWLite/Tools/interface/FlatSource.h
 * \class FlatSource definition
 *
 * \brief Provides a chain of trees configurable from Python.
 *
 * \author Jan Veverka, MIT, jan.veverka@cern.ch
 * \date 6 August 2013
 */

#ifndef FWLite_Tools_FlatSource_h
#define FWLite_Tools_FlatSource_h

#include <string>
#include <vector>
#include <boost/shared_ptr.hpp>
#include "TChain.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

//______________________________________________________________________________
namespace fwlite {
  namespace tools {

    //__________________________________________________________________________
    namespace flat_source {
      /// Forward declaration - nested class workaround
      class Configuration;
    } // namespace flat_source
    
    //__________________________________________________________________________
    class FlatSource {
    public:
      typedef edm::ParameterSet PSet;
      typedef flat_source::Configuration Configuration;
      FlatSource(PSet const& cfg);
      ~FlatSource();
      TChain & chain() {return *chain_;}
    private:
      void initialize();
      boost::shared_ptr<Configuration> cfg_;
      boost::shared_ptr<TChain>        chain_;
    }; // class FlatSource

    //__________________________________________________________________________
    /// Configuration of FlatSource
    class flat_source::Configuration {
    public:
      typedef edm::ParameterSet PSet;
      typedef std::vector<std::string> vstring;
      Configuration(PSet const& cfg);
      std::string const& treeName () const {return treeName_; }
      vstring     const& fileNames() const {return fileNames_;}
    private:
      std::string treeName_;
      vstring     fileNames_;
    }; // class flat_source::Configuration
    
  } // namespace tools
} // namespace fwlite

#endif // FWLite_Tools_FlatSource_h
