#include <iostream>
/**
 * Produces a root file with various histograms of the of the 
 * VecBos trees.
 * 
 * Jan Veverka, Caltech, 12 June 2012
 */


/*****************************************************************************
 * Declare all functions here
 *****************************************************************************/
int checkCommandLineArguments(int, char **);
void printWelcomeMessage();
void printUsage();
int main(int, char **);


//_____________________________________________________________________________
/**
 * Prints a friendly welcome message to the standard output.
 **/
void printWelcomeMessage() {
  std::cout << "Welcome to VecBos Analysis!" << std::endl; 
} // printWelcomeMessage


//_____________________________________________________________________________
/**
 * Prints usage to the standard output.
 */
void printUsage() {
  std::cout << "Usage: analyze-vecbos [cfg.py]" << std::endl; 
} // printUsage


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
 * Main entry point of execution
 */
int main(int argc, char **argv) {
  int status = checkCommandLineArguments(argc, argv);
  if (status > 0) {
    return status;
  }
  printWelcomeMessage();
} // main
