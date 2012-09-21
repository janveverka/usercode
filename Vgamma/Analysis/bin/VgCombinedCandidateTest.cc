/**
 * \brief Unit test of the VgCombinedCandidate class.
 * \author Jan Veverka, Caltech
 * \date 20 September 2012
 */

#include <assert.h>
#include <exception>
#include <math.h>
#include <stdlib.h>
#include <string>
#include <boost/shared_ptr.hpp>
#include "TDirectory.h"
#include "TFile.h"
#include "TLorentzVector.h"
#include "TTree.h"
#include "Vgamma/Analysis/interface/VgAnalyzerTree.h"
#include "Vgamma/Analysis/interface/VgCombinedCandidate.h"
#include "Vgamma/Analysis/interface/VgLeafCandidate.h"

using namespace std;
using cit::VgAnalyzerTree;

typedef boost::shared_ptr<VgAnalyzerTree> TreePtr;
typedef cit::VgCandidate     Cand;
typedef cit::VgLeafCandidate LeafCand;
typedef cit::VgCombinedCandidate CombCand;

//_____________________________________________________________________________
/**
 * Function declarations.
 */
int main(int, char**);
TTree * getTree();
void testCand(CombCand const &);
bool areEqual(double x, double y);

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
    
    CombCand leptojet;
    // Add electrons.
    for (unsigned i=0; i < (unsigned) tree->nEle; ++i) {
      LeafCand ele(*tree, Cand::kElectron, i);
      leptojet.addDaughter(ele);
      LeafCand const & lastDaughter = leptojet.daughter(leptojet.numDaughters() - 1);
      assert(lastDaughter == ele);
    }
    assert((int) leptojet.numDaughters() == tree->nEle);

    // Add muons
    for (unsigned i=0; i < (unsigned) tree->nMu; ++i) {
      LeafCand mu(*tree, Cand::kMuon, i);
      leptojet.addDaughter(mu);
      LeafCand const & lastDaughter = leptojet.daughter(leptojet.numDaughters() - 1);
      assert(lastDaughter == mu);      
    }
    assert((int) leptojet.numDaughters() == tree->nEle + tree->nMu);

    // Add photons
    for (unsigned i=0; i < (unsigned) tree->nPho; ++i) {
      LeafCand pho(*tree, Cand::kPhoton, i);
      leptojet.addDaughter(pho);
      LeafCand const & lastDaughter = leptojet.daughter(leptojet.numDaughters() - 1);
      assert(lastDaughter == pho);      
    }
    assert((int) leptojet.numDaughters() == tree->nEle + tree->nMu + tree->nPho);

    testCand(leptojet);

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
 * Test a candidate.
 */
void
testCand(CombCand const & cand) {
  
  CombCand otherCand(cand);
  assert(otherCand == cand);

  TLorentzVector momentum;
  int charge = 0;
  double weight = 1.;
  
  // loop over daughters
  for (unsigned i = 0; i < cand.numDaughters(); ++i) {
    LeafCand const & dau = cand.daughter(i);
    assert(dau == otherCand.daughter(i));
    momentum += dau.momentum();
    charge += dau.charge();
    weight *= dau.weight();
  } // loop over daughters
  
  assert(cand.momentum() == momentum);
  assert(areEqual(cand.momentum().Pt (), momentum.Pt ()));
  assert(charge == cand.charge());
  assert(weight == cand.weight());

  if (cand.numDaughters() > 0) {
    otherCand.addDaughter(cand.daughter(0));
    assert(otherCand != cand);
  }
  
  // assert(areEqual(cand.momentum().Eta(), candEta[key]));
  // assert(areEqual(cand.momentum().Phi(), candPhi[key]));
  // assert(areEqual(cand.momentum().M  (), mass        ));
  // assert(cand.type() == type);
  // assert(cand.weight() == 1.);
  
  // TLorentzVector v1(1, 2, 3, mass);
  // cand.setMomentum(v1);
  // assert(cand.momentum() == v1);

  // cand.setType(Cand::kPhoton);
  // assert(cand.type() == Cand::kPhoton);

  // cand.scaleWeight(0.9);
  // cand.scaleWeight(1.2);
  // assert(cand.weight() == 1. * 0.9 * 1.2);
} // void testCand(..)


//_____________________________________________________________________________
/**
 * Tests if two floats are almost equal.
 */
bool
areEqual(double x, double y)
{
  double epsilonRelative = 1e-5;
  double epsilonAbsolute = 1e-5;
  if (fabs(y) < epsilonAbsolute) 
    return fabs(x - y) < epsilonAbsolute;
  else
    return fabs(x / y - 1.) < epsilonRelative;
}
