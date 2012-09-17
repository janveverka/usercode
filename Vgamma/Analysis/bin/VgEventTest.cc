/**
 * \brief Unit test of the VgEvent class.
 * \author Jan Veverka, Caltech
 * \date 15 September 2012
 */

#include <assert.h>
#include <exception>
#include <math.h>
#include <iostream>
#include <stdlib.h>
#include <string>
#include <boost/shared_ptr.hpp>
#include "TDirectory.h"
#include "TFile.h"
#include "TLorentzVector.h"
#include "TTree.h"
#include "Vgamma/Analysis/interface/VgAnalyzerTree.h"
#include "Vgamma/Analysis/interface/VgEvent.h"

using namespace std;
using cit::VgAnalyzerTree;
using cit::VgEvent;

typedef boost::shared_ptr<VgAnalyzerTree> TreePtr;

//_____________________________________________________________________________
/**
 * Function declarations.
 */
int main(int, char**);
TTree * getTree();
// bool areEqual(double, double);

//_____________________________________________________________________________
/**
 * Main entry point of execution
 */
int 
main(int argc, char **argv) {
  // Get a VgAnalyzerTree.
  TreePtr tree(new VgAnalyzerTree(getTree()));
  
  // Load an entry
  Long64_t ientry = 0;
  assert(tree->LoadTree(ientry) >= 0);
  assert(tree->fChain->GetEntry(ientry) > 0);

  /// Loop over entries
  Long64_t maxEntry = tree->fChain->GetEntriesFast();
  for (ientry=0; ientry < maxEntry; ientry++) {
    // cout << "Entry: " << ientry << endl;
    if (tree->LoadTree(ientry) < 0) break;
    tree->fChain->GetEntry(ientry);
    
    VgEvent event(*tree);    
    VgEvent otherEvent(*tree);

    /// Test putting empty collections
    otherEvent.putMuons  (cit::VgLeafCandidates());
    otherEvent.putPhotons(cit::VgLeafCandidates());
    assert(otherEvent.muons  ().size() == 0);
    assert(otherEvent.photons().size() == 0);
    
    /// Test putting non-empty collections
    otherEvent.putMuons  (event.muons  ());
    otherEvent.putPhotons(event.photons());
    assert(event.muons  ().size() == otherEvent.muons  ().size());
    assert(event.photons().size() == otherEvent.photons().size());
    
    // Check copy constructor
    VgEvent eventCopy(event);
    assert(event.muons()  .size() == eventCopy.muons()  .size());
    assert(event.photons().size() == eventCopy.photons().size());
  } // loop over entries

  return 0;
} // int main(..)


//_____________________________________________________________________________
/**
 * Get a test EventTree.
 */
TTree * 
getTree() {
  assert(getenv("CMSSW_BASE") != 0);
  std::string path = getenv("CMSSW_BASE");
  path += "/src/Vgamma/Analysis/data/";
  path += "ZGammaToMuMuGamma_2Jet_MG5_TuneZ2_mmgSkim_test10.root";

  TDirectory *cwd = gDirectory;
  TFile file(path.c_str(), "read");
  TTree *srcTree = (TTree*) file.Get("EventTree");
  TTree *myTree = srcTree->CopyTree("");
  myTree->SetDirectory(cwd);
  file.Close();
  
  return myTree;
} // VgAnalyzerTree * getTree();


//_____________________________________________________________________________
/**
 * Tests if two floats are almost equal.
 */
// bool
// areEqual(double x, double y)
// {
//   double epsilonRelative = 1e-5;
//   double epsilonAbsolute = 1e-5;
//   if (fabs(y) < epsilonAbsolute) 
//     return fabs(x - y) < epsilonAbsolute;
//   else
//     return fabs(x / y - 1.) < epsilonRelative;
// }
