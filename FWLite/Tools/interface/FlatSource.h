/**
 * \file  FWLite/Tools/interface/FlatSource.h
 * \class fwlite::tools::FlatSource definition
 *
 * \brief Provides a chain of trees configurable from Python.
 *        Mandatory parameters:
 *            treeName = cms.string('my_tree')
 *            fileNames = cms.vstring('file1', 'file2', ...)
 *        Optional parameters:
 *            variables = cms.vstring('i/I', x/F', 'y/F')
 *
 * \author Jan Veverka, MIT, jan.veverka@cern.ch
 * \date 7 August 2013
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
      typedef std::vector<std::string> vstring;
      typedef flat_source::Configuration Configuration;
      FlatSource(PSet const& cfg);
      ~FlatSource() {}
      TChain & chain() {return *chain_;}
      template <typename T> T& operator[](std::string const& name);
    protected:
      void initialize();
      void initializeVariable(std::string const& variable);
      std::string getName(std::string const& variable);
      char getType(std::string const& variable);
      vstring split (std::string const& variable);
      void addFloat(std::string const& name);
      void addInt(std::string const& name);
      boost::shared_ptr<Configuration> cfg_  ;
      boost::shared_ptr<TChain       > chain_;
      std::map<std::string, Float_t> floats_;
      std::map<std::string, Int_t  > ints_  ;
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
      vstring     const& variables() const {return variables_;}
    private:
      void initialize();
      PSet const& source_   ;
      std::string treeName_ ;
      vstring     fileNames_;
      vstring     variables_;
    }; // class flat_source::Configuration
    
  } // namespace tools
} // namespace fwlite

#endif // ifndef FWLite_Tools_FlatSource_h
