/**
 * \file FWLite/Tools/src/ChainSource.cc
 * \class ChainSource
 *
 * \brief Implementation of the class
 *
 * \author Jan Veverka, MIT, jan.veverka@cern.ch
 * \date 6 August 2013
 */

#include "FWLite/Tools/interface/ChainSource.h"

using namespace ::std;
using ::fwlite::tools::ChainSource;


//___________________________________________________________________________
/**
 * Ctor
 */
ChainSource::ChainSource(PSet const& cfg) :
  cfg_  (new Configuration(cfg)              ),
  chain_(new TChain(cfg_->treeName().c_str()))
{
  initialize();
} // ChainSource::ChainSource()


//___________________________________________________________________________
/**
 * Initilizes ChainSource
 */
void
ChainSource::initialize()
{
  Configuration::vstring::const_iterator fileName = cfg_->fileNames().begin();
  for (; fileName != cfg_->fileNames().end(); ++fileName) {
    chain_->Add(fileName->c_str());
  }
} // Configuration::Configuration()


//___________________________________________________________________________
/**
 * Configuration Ctor
 */
ChainSource::Configuration::Configuration(PSet const& cfg) :
  treeName_ (cfg.getParameter<string> ("treeName" )),
  fileNames_(cfg.getParameter<vstring>("fileNames"))
{} // ChainSource::Configuration::Configuration()

