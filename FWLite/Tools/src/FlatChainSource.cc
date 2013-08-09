/**
 * \file FWLite/Tools/src/FlatChainSource.cc
 * \class FlatChainSource
 *
 * \brief Implementation of the class
 *
 * \author Jan Veverka, MIT, jan.veverka@cern.ch
 * \date 9 August 2013
 */

#include <boost/algorithm/string.hpp>
#include "FWCore/Utilities/interface/Exception.h"
#include "FWLite/Tools/interface/FlatChainSource.h"

using namespace ::std;
using ::fwlite::tools::ChainSource;
using ::fwlite::tools::FlatChainSource;

typedef cms::Exception Bad;

//___________________________________________________________________________
/**
 * Ctor
 */
FlatChainSource::FlatChainSource(PSet const& cfg) :
  ChainSource(cfg),
  cfg_  (new Configuration(cfg))
{
  initialize();
} // FlatChainSource::FlatChainSource()


//___________________________________________________________________________
/**
 * Initilizes FlatChainSource
 */
void
FlatChainSource::initialize()
{
  /// We read no branches by default
  chain_->SetBranchStatus("*", 0);
  
  Configuration::vstring::const_iterator variable = cfg_->variables().begin();
  for (; variable != cfg_->variables().end(); ++variable) {
    initializeVariable(*variable);
  }
} // FlatChainSource::initialize()


//___________________________________________________________________________
/**
 * Initilizes variable of FlatChainSource described by the given string
 */
void
FlatChainSource::initializeVariable(string const& variable)
{
  string name = getName(variable);
  char   type = getType(variable);
  switch (type) {
    case 'F': addFloat(name); break;
    case 'I': addInt  (name); break;
    default:
      throw Bad("BadBranch") << "Branch type `" << type << "' not supprted!";
  }

} // FlatChainSource::initializeVariable()


//___________________________________________________________________________
/**
 * Parses the given string to the variable name
 */
string
FlatChainSource::getName(string const& variable)
{
  return split(variable)[0];
} // FlatChainSource::getName(string const& variable)


//___________________________________________________________________________
/**
 * Parses the given string to the variable type
 */
char
FlatChainSource::getType(string const& variable)
{
  return split(variable)[1][0];
} // FlatChainSource::getType(string const& variable)


//___________________________________________________________________________
/**
 * Splits the given string by the '/' delimiter and returns the tokens.
 */
FlatChainSource::vstring
FlatChainSource::split(string const& variable)
{
  vstring tokens;
  boost::split(tokens, variable, boost::is_any_of("/"));

  if (tokens.size() != 2 or tokens[1].size() != 1) {
    throw Bad("BadVariable") << "Illegal variable `" << variable << "'!";
  }

  return tokens;
} // FlatChainSource::split(string const& variable)


//___________________________________________________________________________
/**
 * Creates a float buffer and sets the branch status and address
 */
void
FlatChainSource::addFloat(std::string const& name)
{
  chain_->SetBranchAddress(name.c_str(), &floats_[name]);
  chain_->SetBranchStatus(name.c_str(), 1);
} // FlatChainSource::addFloat()


//___________________________________________________________________________
/**
 * Creates an int buffer and sets the branch status and address
 */
void
FlatChainSource::addInt(std::string const& name)
{
  chain_->SetBranchAddress(name.c_str(), &ints_[name]);
  chain_->SetBranchStatus(name.c_str(), 1);
} // FlatChainSource::addFloat()


//___________________________________________________________________________
/**
 * Returns the leaf buffer of the given name
 */
template <typename T>
T&
FlatChainSource::get(string const& name)
{
  /// All supported types are implemented through specializations.
  throw Bad("BadType") << __FUNCTION__ << ": Type `" << typeid(T).name
                       << "' not supported!";
} // FlatChainSource::get(const char *name)()


/// Start a hack around gcc complaining about template specialization in
/// in different namespace, see
/// http://stackoverflow.com/questions/2282349/
/// specialization-of-templateclass-tp-struct-stdless-in-different-namespace
namespace fwlite {
  namespace tools {


    //_______________________________________________________________________
    /**
    * Returns the float buffer of the given name.
    * USAGE:
    *   FlatChainSource input(cfg);
    *   input.chain().GetEntry(iEntry);
    *   Float_t x = input.get<Float_t>("x")
    */
    template <>
    Float_t&
    FlatChainSource::get<Float_t>(string const& name)
    {
      return floats_[name];
    } // FlatChainSource::get<Float_t>(sting const& name)


    //_______________________________________________________________________
    /**
    * Returns the flot buffer of the given name
    */
    template <>
    Int_t&
    FlatChainSource::get<Int_t>(string const& name)
    {
      return ints_[name];
    } // FlatChainSource::get<Int_t>(sting const& name)


  } // namespace tools
} // namespace fwlite
//
//
// //___________________________________________________________________________
// /**
//  * Method boiler plate
//  */
// void
// FlatChainSource::()
// {
// } // FlatChainSource::()




//==============================================================================
/// Implementation of \class FlatChainSource::Configuration
//==============================================================================

//___________________________________________________________________________
/**
 * Configuration Ctor
 */
FlatChainSource::Configuration::Configuration(PSet const& cfg) :
  ChainSource::Configuration(cfg),
  variables_(cfg.getParameter<vstring>("variables"))
{} // FlatChainSource::Configuration::Configuration()
