/**
 * Source for the executable that does the VecBos analysis:
 * produces a root file with various histograms of the of the 
 * VecBos trees.
 * 
 * Jan Veverka, Caltech, 12 June 2012
 */

#include <iostream>
#include <boost/shared_ptr.hpp>
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"
#include "Zmmg/FWLite/interface/VecBosAnalyzer.h"

/*****************************************************************************
 * Declare all functions here
 *****************************************************************************/
int checkCommandLineArguments(int, char **);
void printUsage();
void printWelcomeMessage();
void printGoodbyeMessage();
int main(int, char **);


//_____________________________________________________________________________
/**
 * Checks the validity of the command line arguments; prints usage
 * information to the standard output if needed.  Returns the status
 * if the check; status = 0 means no problem, status > 0 means error.
 */
int checkCommandLineArguments(int argc, char **argv) {
  if ( argc < 2 ) {
    printUsage();
    return 1;
  }
  return 0;
} // checkCommandLineArguments


//_____________________________________________________________________________
/**
 * Prints usage to the standard output.
 */
void printUsage() {
  std::cout << "Usage: analyze-vecbos [cfg.py]" << std::endl; 
} // printUsage


//_____________________________________________________________________________
/**
 * Prints a friendly welcome message to the standard output.
 **/
void printWelcomeMessage() {
  std::cout << "Welcome to VecBos Analysis!" << std::endl; 
} // printWelcomeMessage


//_____________________________________________________________________________
/**
 * Prints a friendly good-bye message to the standard output.
 **/
void printGoodbyeMessage() {
  std::cout << "Exiting VecBos Analysis with success." << std::endl; 
} // printGoodbyeMessage


//_____________________________________________________________________________
/**
 * Main entry point of execution
 */
int main(int argc, char **argv) {
  int status = checkCommandLineArguments(argc, argv);
  if (status > 0) {
    return status;
  }
  
  printWelcomeMessage();
  
  // Get the configuration:
  PythonProcessDesc builder(argv[1],argc,argv);
  boost::shared_ptr<edm::ParameterSet> cfg(
    builder.processDesc()->getProcessPSet()
    );
  
  // Instantiate the analyzer:
  cit::VecBosAnalyzer analyzer(cfg);
  
  // Run the analyzer:
  analyzer.run();
  
  // That's it!
  printGoodbyeMessage();
} // main
