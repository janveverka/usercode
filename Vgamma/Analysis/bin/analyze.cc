/**
 * Source for the executable that does the Vg analysis:
 * produces a root file with various histograms of the  
 * Vg trees.
 * 
 * Jan Veverka, Caltech, 08 September 2012
 */

#include <iostream>
#include <boost/shared_ptr.hpp>
#include "TStopwatch.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"
#include "Vgamma/Analysis/interface/VgAnalyzer.h"

/*****************************************************************************
 * Declare all functions here
 *****************************************************************************/
int checkCommandLineArguments(int, char **);
void printUsage(char **);
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
  std::cout << "Usage: " << argv[0] << " [cfg.py]" << std::endl; 
} // printUsage


//_____________________________________________________________________________
/**
 * Prints a friendly welcome message to the standard output.
 **/
void printWelcomeMessage() {
  std::cout << "Welcome to Vgamma Analysis!" << std::endl; 
} // printWelcomeMessage


//_____________________________________________________________________________
/**
 * Prints a friendly good-bye message to the standard output.
 **/
void printGoodbyeMessage() {
  std::cout << "Exiting Vgamma Analysis with success." << std::endl; 
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
  
  TStopwatch stopwatch;
  stopwatch.Start();
  
  printWelcomeMessage();
  
  // Get the configuration:
  PythonProcessDesc builder(argv[1],argc,argv);
  boost::shared_ptr<edm::ParameterSet> cfg(
    builder.processDesc()->getProcessPSet()
    );
  
  // Instantiate the analyzer:
  cit::VgAnalyzer analyzer(cfg);
  
  // Run the analyzer:
  analyzer.run();
  
  std::cout.precision(1);
  std::cout << "CPU time: "  << analyzer.humanReadableTime(stopwatch.CpuTime())
            << ", real time: " 
            << analyzer.humanReadableTime(stopwatch.RealTime()) << "." 
            << std::endl;
  
  // That's it!
  printGoodbyeMessage();
} // main
