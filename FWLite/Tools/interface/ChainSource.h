/**
 * \file  FWLite/Tools/interface/ChainSource.h
 * \class ChainSource definition
 *
 * \brief Provides a chain of trees given Python configuration.
 *
 * \author Jan Veverka, MIT, jan.veverka@cern.ch
 * \date 6 August 2013
 */

#ifndef FWLite_Tools_ChainSource_h
#define FWLite_Tools_ChainSource_h

#include <string>
#include <vector>
#include <boost/shared_ptr.hpp>
#include "TChain.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

//______________________________________________________________________________
namespace fwlite {
  namespace tools {

    //__________________________________________________________________________
    namespace chain_source {
      /// Forward declaration - nested class workaround
      class Configuration;
    } // namespace chain_source
    
    //__________________________________________________________________________
    class ChainSource {
    public:
      typedef edm::ParameterSet PSet;
      typedef chain_source::Configuration Configuration;
      ChainSource(PSet const& cfg);
      virtual ~ChainSource(){}
      TChain& chain() {return *chain_;}
      Configuration const& config() const {return *cfg_;}
    protected:
      virtual void initialize();
      boost::shared_ptr<Configuration> cfg_;
      boost::shared_ptr<TChain>        chain_;
    }; // class ChainSource

    //__________________________________________________________________________
    /// Configuration of ChainSource
    class chain_source::Configuration {
    public:
      typedef edm::ParameterSet PSet;
      typedef std::vector<std::string> vstring;
      Configuration(PSet const& cfg);
      std::string const& treeName () const {return treeName_; }
      vstring     const& fileNames() const {return fileNames_;}
    protected:
      std::string treeName_;
      vstring     fileNames_;
    }; // class chain_source::Configuration
    
  } // namespace tools
} // namespace fwlite

#endif // FWLite_Tools_ChainSource_h
