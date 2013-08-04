/**
 * Source for the executable that applies the Q-Q corrections
 * to the photon ID MVA input variables.  It reads a tree 
 * and creates a new tree with the corrected and raw input 
 * variables as well as the corresponding ID MVA outputs for both.
 * 
 * Jan Veverka, MIT, jan.veverka@cern.ch
 * 04 August 2013
 */

#include <iostream>
#include <boost/shared_ptr.hpp>
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"
#include "FWLite/Hgg/interface/CorrectionApplicator.h"
#include "FWLite/Tools/interface/Stopwatch.h"


/*****************************************************************************
 * Declare all functions here
 *****************************************************************************/
int  main(int, char **);
int  checkCommandLineArguments(int, char **);
void printUsage(char **);
void printWelcomeMessage();
void printGoodbyeMessage();


//_____________________________________________________________________________
/**
 * Main entry point of execution
 */
int main(int argc, char **argv) { 
  int status = checkCommandLineArguments(argc, argv);
  if (status > 0) {
    return status;
  }
  
  Stopwatch stopwatch;
  stopwatch.Start();
  
  printWelcomeMessage();
  
  // Get the configuration:
  PythonProcessDesc builder(argv[1],argc,argv);
  boost::shared_ptr<edm::ParameterSet> cfg(
    builder.processDesc()->getProcessPSet()
    );
  
  // Instantiate the analyzer:
  mit::hgg::CorrectionApplicator applicator(cfg);
  
  // Run the analyzer:
  applicator.run();

  // Print timing information
  std::cout.precision(1);
  std::cout << "CPU time:  " << stopwatch.humanReadableCpuTime () << "\n"
            << "Real time: " << stopwatch.humanReadableRealTime() << "\n"; 
  
  // That's it!
  printGoodbyeMessage();
} // main


//_____________________________________________________________________________
/**
 * Checks the validity of the command line arguments; prints usage
 * information to the standard output if needed.  Returns the status
 * if the check; status = 0 means no problem, status > 0 means error.
 */
int checkCommandLineArguments(int argc, char **argv) {
  if ( argc < 2 ) {
    printUsage(argv);
    return 1;
  }
  return 0;
} // checkCommandLineArguments


//_____________________________________________________________________________
/**
 * Prints usage to the standard output.
 */
void printUsage(char **argv) {
  std::cout << "hgg-apply-corrections - apply ID MVA corrections\n"
            << "\n"
            << "Applies the Q-Q corrections to the photon ID MVA input\n"
            << "variables.  It reads a tree and creates a new tree with\n"
            << "the corrected and raw input variables as well as the ID MVA\n"
            << "output for both.\n"
            << "\n"
            << "Usage: " << argv[0] << " [cfg.py]\n";
} // printUsage(..)


//_____________________________________________________________________________
/**
 * Prints a friendly welcome message to the standard output.
 **/
void printWelcomeMessage() {
  std::cout << "Welcome to the MIT Hgg corrector of the photon MVA ID "
            << "inputs!\n";
} // printWelcomeMessage


//_____________________________________________________________________________
/**
 * Prints a friendly good-bye message to the standard output.
 **/
void printGoodbyeMessage() {
  std::cout << "Exiting the corrector with success!" << std::endl; 
} // printGoodbyeMessage


