/**
 * \file  FWLite/Tools/interface/FlatChainSource.h
 * \class fwlite::tools::FlatChainSource definition
 *
 * \brief Provides a chain of trees configurable from Python.
 *        Mandatory configuration parameters:
 *            treeName = cms.string('my_tree')
 *            fileNames = cms.vstring('file1', 'file2', ...)
 *            variables = cms.vstring('i/I', x/F', 'y/F', ...)
 *
 * \author Jan Veverka, MIT, jan.veverka@cern.ch
 * \date 9 August 2013
 */

#ifndef FWLite_Tools_FlatChainSource_h
#define FWLite_Tools_FlatChainSource_h

#include <string>
#include <vector>
#include <boost/shared_ptr.hpp>
#include "TChain.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWLite/Tools/interface/ChainSource.h"

//______________________________________________________________________________
namespace fwlite {
  namespace tools {

    //__________________________________________________________________________
    namespace flat_chain_source {
      /// Forward declaration - nested class workaround
      class Configuration;
    } // namespace flat_chain_source
    
    //__________________________________________________________________________
    class FlatChainSource : public ChainSource {
    public:
      typedef edm::ParameterSet PSet;
      typedef std::vector<std::string> vstring;
      typedef flat_chain_source::Configuration Configuration;
      FlatChainSource(PSet const& cfg);
      ~FlatChainSource() {}
      template <typename T> T& get(std::string const& name);
      Float_t& getF(std::string const& name){return floats_[name];}
      Int_t  & getI(std::string const& name){return ints_  [name];}
      Float_t& F(std::string const& name){return floats_[name];}
      Int_t  & I(std::string const& name){return ints_  [name];}
    protected:
      void initialize();
      void initializeVariable(std::string const& variable);
      std::string getName(std::string const& variable);
      char getType(std::string const& variable);
      vstring split (std::string const& variable);
      void addFloat(std::string const& name);
      void addInt(std::string const& name);
      boost::shared_ptr<Configuration> cfg_  ;
      std::map<std::string, Float_t> floats_;
      std::map<std::string, Int_t  > ints_  ;
    }; // class FlatChainSource

    //__________________________________________________________________________
    /// Configuration of FlatChainSource
    class flat_chain_source::Configuration : public ChainSource::Configuration {
    public:
      Configuration(PSet const& cfg);
      vstring const& variables() const {return variables_;}
    protected:
      vstring variables_;
    }; // class flat_chain_source::Configuration
    
  } // namespace tools
} // namespace fwlite

#endif // ifndef FWLite_Tools_FlatChainSource_h
