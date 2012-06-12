/**
 * Implementation of the VecBosAnalyzer class.
 * 
 * Jan Veverka, Caltech, 12 June 2012.
 */

#include "Zmmg/FWLite/interface/VecBosAnalyzer.h"

using cit::VecBosAnalyzer;

//_____________________________________________________________________
/**
 * Constructor
 */
VecBosAnalyzer::VecBosAnalyzer(boost::shared_ptr<edm::ParameterSet> cfg)
{
  cfg_ = cfg;
  init();
} // ctor


//_____________________________________________________________________
/**
 * Destructor
 */
VecBosAnalyzer::~VecBosAnalyzer(){}


//_____________________________________________________________________
/**
 * Initialization.
 */
void
VecBosAnalyzer::init()
{
  
} // init
