/**
 * \brief Unit test of the VgLeafCandidate class.
 * \author Jan Veverka, Caltech
 * \date 15 September 2012
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
#include "Vgamma/Analysis/interface/VgLeafCandidate.h"
#include "Vgamma/Analysis/interface/VgException.h"

using namespace std;
using cit::VgAnalyzerTree;
using cit::VgLeafCandidate;

typedef boost::shared_ptr<VgAnalyzerTree> TreePtr;
typedef VgLeafCandidate Cand;

//_____________________________________________________________________________
/**
 * Function declarations.
 */
int main(int, char**);
TTree * getTree();
void testCand(TreePtr, Cand::ParticleType, unsigned);
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

  // Check exception when electron index is out of range.
  try {
    testCand(tree, Cand::kElectron, tree->nEle);
  } catch (exception& e) {
    assert(string(e.what()).find("outside of range nEle") != string::npos);
  }

  // Check exception when muon index is out of range.
  try {
    testCand(tree, Cand::kMuon, tree->nMu);
  } catch (exception& e) {
    assert(string(e.what()).find("outside of range nMu") != string::npos);
  }

  // Check exception when photon index is out of range.
  try {
    testCand(tree, Cand::kPhoton, tree->nPho);
  } catch (exception& e) {
    assert(string(e.what()).find("outside of range nPho") != string::npos);
  }

  /// Loop over entries
  Long64_t maxEntry = tree->fChain->GetEntriesFast();
  for (ientry=0; ientry < maxEntry; ientry++) {
    // cout << "Entry: " << ientry << endl;
    if (tree->LoadTree(ientry) < 0) break;
    tree->fChain->GetEntry(ientry);
    
    // Test electrons.
    for (unsigned i=0; i < (unsigned) tree->nEle; ++i)
      testCand(tree, Cand::kElectron, i);

    // Test muons
    for (unsigned i=0; i < (unsigned) tree->nMu; ++i)
      testCand(tree, Cand::kMuon    , i);

    // Test photons
    for (unsigned i=0; i < (unsigned) tree->nPho; ++i)
      testCand(tree, Cand::kPhoton  , 0);
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
testCand(TreePtr tree, Cand::ParticleType type, unsigned key) {
  // cout << "type, key: " << type << ", " << key << endl;
  // Define the candidate
  Cand cand(*tree, type, key);
  
  double mass = 0.;
  Float_t * candPt  = tree->phoEt ;
  Float_t * candEta = tree->phoEta;
  Float_t * candPhi = tree->phoPhi;
  switch (type) {
  case Cand::kElectron: 
    candPt  = tree->elePt;
    candEta = tree->eleEta;
    candPhi = tree->elePhi;
    mass    = Cand::kElectronMass;
    break;
  case Cand::kMuon: 
    candPt  = tree->muPt;
    candEta = tree->muEta;
    candPhi = tree->muPhi;
    mass = Cand::kMuonMass; 
    break;
  default: 
    mass = 0.;
  } // switch (type)
  
  // cout << "cand.momentum().M(), mass: " << cand.momentum().M() << ", " 
  //      << mass << endl;

  // Test it
  assert(areEqual(cand.momentum().Pt (), candPt [key]));
  assert(areEqual(cand.momentum().Eta(), candEta[key]));
  assert(areEqual(cand.momentum().Phi(), candPhi[key]));
  assert(areEqual(cand.momentum().M  (), mass        ));
  assert(cand.type() == type);
  assert(cand.weight() == 1.);
  
  TLorentzVector v1(1, 2, 3, mass);
  cand.setMomentum(v1);
  assert(cand.momentum() == v1);

  cand.setType(Cand::kPhoton);
  assert(cand.type() == Cand::kPhoton);

  cand.scaleWeight(0.9);
  cand.scaleWeight(1.2);
  assert(cand.weight() == 1. * 0.9 * 1.2);
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
