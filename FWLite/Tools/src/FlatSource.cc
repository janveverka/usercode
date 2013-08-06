/**
 * \file FWLite/Tools/src/FlatSource.cc
 * \class FlatSource
 *
 * \brief Implementation of the class
 *
 * \author Jan Veverka, MIT, jan.veverka@cern.ch
 * \date 6 August 2013
 */

#include "FWLite/Tools/interface/FlatSource.h"

using namespace std;
using namespace fwlite::tools;


//___________________________________________________________________________
/**
 * Ctor
 */
FlatSource::FlatSource(PSet const& cfg) :
  cfg_  (new Configuration(cfg)              ),
  chain_(new TChain(cfg_->treeName().c_str()))
{} // FlatSource::FlatSource()


//___________________________________________________________________________
/**
 * Initilizes FlatSource
 */
void
FlatSource::initialize()
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
flat_source::Configuration::Configuration(PSet const& cfg) :
  treeName_ (cfg.getParameter<string> ("treeName" )),
  fileNames_(cfg.getParameter<vstring>("fileNames"))
{} // flat_source::Configuration::Configuration()

