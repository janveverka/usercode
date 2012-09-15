/**
 * \file Vgamma/Analysis/bin/skim.cc
 * \brief Copies selected tree entries from a file to a new file.
 * Inspired by CopyTree of Andrew Hidas, Irakli Svintradze and
 * Lindsey Gray in 
 * UserCode/LGray/ElectroWeakAnalysis/MultiBosons/bin/CopyTree.C
 * of
 * http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/
 * 
 * Use:
 * skim [options] tree destination.root source.root [source2.root source3.root ...]
 * Options:
 *  -c <cut>  -- apply a selection in the form of a TTree::Draw expression
 *  -n <number> -- store maximum <number> entries in the output.
 *  -v -- verbose output; prints the usage info.
 * 
 * \author Jan Veverka, Caltech
 * \date 13 September 2012
 */

#include <cstdlib>
#include <iostream>

#include "TChain.h"
#include "TDirectory.h"
#include "TEntryList.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"

#include "FWLite/Tools/interface/ArgParser.h"

using cit::ArgParser;

enum ExitStatus {kSuccess = 0, kInputArgumentsError};

/*****************************************************************************
 * Declare all functions here
 *****************************************************************************/
int main(int, char **);
// int copyEvents(TString const, TString const, TString const, double const);
int copyEvents(ArgParser &);
int checkCommandLineArguments(ArgParser &);
void printWelcomeMessage();
void printGoodbyeMessage();

//_____________________________________________________________________________
/**
 * Main entry point of execution
 */
int main(int argc, char **argv) {
  ArgParser parser(argc,argv);

  int status;
  status = checkCommandLineArguments(parser);
  if (status > kSuccess) {
    return status;
  }
    
  printWelcomeMessage();

//   status = copyEvents(parser.getArgument("source"), 
//                       parser.getArgument("destination"),
//                       parser.getArgument("tree"), 
//                       1.);
  status = copyEvents(parser);
  
  if (status > kSuccess) {
    return status;
  }

  printGoodbyeMessage();
  
  return kSuccess;
}


//_____________________________________________________________________________
/**
 * Main workhorse
 */
// int copyEvents(TString const InFileName, TString const OutFileName, 
//                TString const TreeName, double const weight)
int copyEvents(ArgParser & parser)
{
  TString const InFileName  = parser.getArgument("source");
  TString const OutFileName = parser.getArgument("destination");
  TString const TreeName    = parser.getArgument("tree");
  double weight = 1.;
  int verbosity = 0;
  
  if (parser.shortFlagPres('w')) 
    weight = atof(parser.getShortFlag('w').c_str());
  
  if (parser.shortFlagPres('v')) 
    verbosity = 1;
  
  if (verbosity > 0)
      parser.printOptions("skim");
  
  // Open the input file and get input tree
//   TFile* InFile = new TFile(InFileName, "read");
//   TTree* InTree = (TTree*) InFile->Get(TreeName);
  
  // TFile* InFile = new TFile(InFileName, "read");
  TChain* InTree = new TChain(TreeName);
  InTree->Add(InFileName);
  
  // Add optional additional input files
  std::vector<std::string>::const_iterator filename;
  for (filename = parser.getUnlimitedArgument("sources");
       filename != parser.args_end(); ++ filename)
    InTree->Add(filename->c_str());
  
  // Apply optional cut
  Long64_t lastEntry = 0;
  if (parser.shortFlagPres('c')) {
    // Select entries
    std::cout << "Applying cut `" << parser.getShortFlag('c') << "' ..."
              << std::endl;
    InTree->Draw(">>elist", parser.getShortFlag('c').c_str(), "entrylist");
    TEntryList* elist = (TEntryList*)gDirectory->Get("elist");
    InTree->SetEntryList(elist);
    lastEntry = elist->GetN();
  } else {
    lastEntry = InTree->GetEntries();
  }

  // Open output file, clone input tree, and set the output tree to the output file
  TFile* OutFile = new TFile(OutFileName, "recreate");
  TTree* OutTree = (TTree*) InTree->CloneTree(0);
  OutTree->SetDirectory(OutFile);
  
  if (parser.shortFlagPres('n')) 
    lastEntry = atoi(parser.getShortFlag('n').c_str());
  
  Long64_t reportEvery = -1;
  if (parser.shortFlagPres('e')) 
    reportEvery = atoi(parser.getShortFlag('e').c_str());
  
  // Loop over all entries in input tree
  for (int outEntry = 0; outEntry < lastEntry; ++outEntry) {
//   for (int outEntry = 0; outEntry < 100; ++outEntry) {
    // if (outEntry % 1000 == 0) {
    
    Long64_t inEntry = InTree->GetEntryNumber(outEntry);
    if (inEntry < 0) break;

    if (InTree->GetEntry(inEntry) < 0) break;

    if (reportEvery > 0 && outEntry % reportEvery == 0) {
      std::cout << "Processing output entry " << outEntry
                << " corresponding to input entry " << inEntry << std::endl;
    }
    
    // Fill _this_ entry in the output tree
    OutTree->Fill();    
    
  }
  
  OutTree->SetWeight(weight);
  // Write and close output file
  OutFile->Write();
  OutFile->Close();
  // InFile->Close();
  
  return kSuccess;
}


//_____________________________________________________________________________
/**
 * Checks the validity of the command line arguments; prints usage
 * information to the standard output if needed.  Returns the status
 * if the check; status = 0 means no problem, status > 0 means error.
 */
int checkCommandLineArguments(ArgParser & parser) {
  /// Define the options and arguments
  parser.addShortOption('c', ArgParser::reqArg, 
                        "cut - a TFormula expression selecting events to be "
                        "stored");
  
  parser.addShortOption('e', ArgParser::reqArg, 
                        "Report every n-th processed output event");
  
  parser.addShortOption('n', ArgParser::reqArg, 
                        "(maximum) number of output entries");
  
  parser.addShortOption('s', ArgParser::reqArg, 
                        "number of first input entries to skip");
  
  parser.addShortOption('w', ArgParser::reqArg,
                        "weight applied to the output tree");
  
  parser.addShortOption('v', ArgParser::noArg, "verbose mode");  
  
  parser.addArgument("tree", ArgParser::required, 
                     "tree name optionally preceded by path: [<path>/]tree");
  
  parser.addArgument("destination", ArgParser::required,
                     "name of the destination root file");
  
  parser.addArgument("source", ArgParser::required,
                     "name of the source root file");
  
  parser.addUnlimitedArgument("sources", 
                              "names of optional additional source root files");
  std::string error;
  int retCode = parser.process(error);

  if(retCode != 0){
    std::cerr << "ERROR Parsing option: " << error 
              << "   return code: " << retCode << std::endl;
    parser.printOptions("skim");
    return kInputArgumentsError;
  }
  
  return kSuccess;
} // checkCommandLineArguments


//_____________________________________________________________________________
/**
 * Prints a friendly welcome message to the standard output.
 **/
void printWelcomeMessage() {
  std::cout << "Welcome to `skim'!" << std::endl; 
} // printWelcomeMessage


//_____________________________________________________________________________
/**
 * Prints a friendly good-bye message to the standard output.
 **/
void printGoodbyeMessage() {
  std::cout << "Exiting `skim' with success." << std::endl; 
} // printGoodbyeMessage


