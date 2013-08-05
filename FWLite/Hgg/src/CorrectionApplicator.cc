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
  cfg_(new Configuration(cfg))
{
  initialize();
} // Constructor


//_____________________________________________________________________________
/**
 * Destructor
 */
CorrectionApplicator::~CorrectionApplicator()
{
  delete cfg_;
} // Destructor


//_____________________________________________________________________________
/**
 * Run the correction application.
 */
void
CorrectionApplicator::run()
{
  std::cout << "CorrectionApplicator::run()\n";
//   beginRun();
//   loopOverEvents();
//   endRun();
} // run()


//_____________________________________________________________________________
/**
 * Initializes data members.
 * Parses configuration, opens input file, retrieves the input tree,
 * defines variables to be read, sets their addresses, creates the 
 * output file and tree, initializes corrections.
 */
void
CorrectionApplicator::initialize()
{
} // initialize()


