/**
 * \file FWLite/Tools/src/FlatSource.cc
 * \class FlatSource
 *
 * \brief Implementation of the class
 *
 * \author Jan Veverka, MIT, jan.veverka@cern.ch
 * \date 7 August 2013
 */

#include <boost/algorithm/string.hpp>
#include "FWCore/Utilities/interface/Exception.h"
#include "FWLite/Tools/interface/FlatSource.h"

using namespace std;
using namespace fwlite::tools;

typedef cms::Exception Bad;

//___________________________________________________________________________
/**
 * Ctor
 */
FlatSource::FlatSource(PSet const& cfg) :
  cfg_  (new Configuration(cfg)              ),
  chain_(new TChain(cfg_->treeName().c_str()))
{
  initialize();
} // FlatSource::FlatSource()


//___________________________________________________________________________
/**
 * Initilizes FlatSource
 */
void
FlatSource::initialize()
{
  /// We read no branches by default
  chain_->SetBranchStatus("*", 0);
  
  Configuration::vstring::const_iterator fileName = cfg_->fileNames().begin();
  for (; fileName != cfg_->fileNames().end(); ++fileName) {
    chain_->Add(fileName->c_str());
  }

  Configuration::vstring::const_iterator variable = cfg_->variables().begin();
  for (; variable != cfg_->variables().end(); ++variable) {
    initializeVariable(*variable);
  }
} // FlatSource::initialize()


//___________________________________________________________________________
/**
 * Initilizes variable of FlatSource described by the given string
 */
void
FlatSource::initializeVariable(string const& variable)
{
  string name = getName(variable);
  char   type = getType(variable);
  switch (type) {
    case 'F': addFloat(name); break;
    case 'I': addInt  (name); break;
    default:
      throw Bad("BadBranch") << "Branch type `" << type << "' not supprted!";
  }

} // FlatSource::initializeVariable()


//___________________________________________________________________________
/**
 * Parses the given string to the variable name
 */
string
FlatSource::getName(string const& variable)
{
  return split(variable)[0];
} // FlatSource::getName(string const& variable)


//___________________________________________________________________________
/**
 * Parses the given string to the variable type
 */
char
FlatSource::getType(string const& variable)
{
  return split(variable)[1][0];
} // FlatSource::getType(string const& variable)


//___________________________________________________________________________
/**
 * Splits the given string by the '/' delimiter and returns the tokens.
 */
FlatSource::vstring
FlatSource::split(string const& variable)
{
  vstring tokens;
  boost::split(tokens, variable, boost::is_any_of("/"));

  if (tokens.size() != 2 or tokens[1].size() != 1) {
    throw Bad("BadVariable") << "Illegal variable `" << variable << "'!";
  }

  return tokens;
} // FlatSource::split(string const& variable)


//___________________________________________________________________________
/**
 * Creates a float buffer and sets the branch status and address
 */
void
FlatSource::addFloat(std::string const& name)
{
  chain_->SetBranchAddress(name.c_str(), &floats_[name]);
  chain_->SetBranchStatus(name.c_str(), 1);
} // FlatSource::addFloat()


//___________________________________________________________________________
/**
 * Creates an int buffer and sets the branch status and address
 */
void
FlatSource::addInt(std::string const& name)
{
  chain_->SetBranchAddress(name.c_str(), &ints_[name]);
  chain_->SetBranchStatus(name.c_str(), 1);
} // FlatSource::addFloat()


//___________________________________________________________________________
/**
 * Returns the leaf buffer of the given name
 */
template <typename T>
T&
FlatSource::operator[](string const& name)
{
  /// All supported types are implemented through specializations.
  throw Bad("BadType") << __FUNCTION__ << ": Type `" << typeid(T).name
                       << "' not supported!";
} // FlatSource::operator[](const char *name)()

/// Start a hack around gcc complaining about template specialization in
/// in different namespace, see
/// http://stackoverflow.com/questions/2282349/
/// specialization-of-templateclass-tp-struct-stdless-in-different-namespace
namespace fwlite {
  namespace tools {


    //_______________________________________________________________________
    /**
    * Returns the flot buffer of the given name
    */
    template <>
    Float_t&
    FlatSource::operator[]<Float_t>(string const& name)
    {
      return floats_[name];
    } // FlatSource::operator<Float_t>[](sting const& name)


    //_______________________________________________________________________
    /**
    * Returns the flot buffer of the given name
    */
    template <>
    Int_t&
    FlatSource::operator[]<Int_t>(string const& name)
    {
      return ints_[name];
    } // FlatSource::operator<Int_t>[](sting const& name)


  } // namespace tools
} // namespace fwlite
//
//
// //___________________________________________________________________________
// /**
//  * Method boiler plate
//  */
// void
// FlatSource::()
// {
// } // FlatSource::()




//==============================================================================
/// Implementation of \class flat_source::Configuration
//==============================================================================

//___________________________________________________________________________
/**
 * Configuration Ctor
 */
flat_source::Configuration::Configuration(PSet const& cfg) :
  source_   (cfg),
  treeName_ (cfg.getParameter<string> ("treeName" )),
  fileNames_(cfg.getParameter<vstring>("fileNames")),
  variables_()
{
  initialize();
} // flat_source::Configuration::Configuration()


//___________________________________________________________________________
/**
 * Initilizes optional parameters of flat_source::Configuration
 */
void
flat_source::Configuration::initialize()
{
  if (source_.existsAs<vstring>("variables")) {
    variables_ = source_.getParameter<vstring>("variables");
  }
} // flat_source::Configuration::initialize()

