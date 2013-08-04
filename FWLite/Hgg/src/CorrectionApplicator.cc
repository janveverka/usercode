/**
 * Implementation of the \class CorrectionApplicator
 * 
 * Jan Veverka, MIT, jan.veverka@cern.ch
 * 04 August 2013.
 */

#include <iostream>
#include "FWLite/Hgg/interface/CorrectionApplicator.h"

using mit::hgg::CorrectionApplicator;

//_____________________________________________________________________________
/**
 * Constructor
 */
CorrectionApplicator::CorrectionApplicator(PSetPtr cfg) :
  cfg_(cfg)
{
} // Constructor


//_____________________________________________________________________________
/**
 * Destructor
 */
CorrectionApplicator::~CorrectionApplicator()
{
} // Destructor


//_____________________________________________________________________________
/**
 * Run the correction application.
 */
void
CorrectionApplicator::run()
{
  std::cout << "CorrectionApplicator::run()\n";
} // run()
