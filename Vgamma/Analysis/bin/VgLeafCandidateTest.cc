/**
 * \brief Unit test of the VgLeafCandidate class.
 * \author Jan Veverka, Caltech
 * \date 15 September 2012
 */

#include <assert.h>
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
  
  testCand(tree, Cand::kElectron, 0);
  testCand(tree, Cand::kMuon    , 0);
  testCand(tree, Cand::kMuon    , 1);
  testCand(tree, Cand::kPhoton  , 0);

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
  double epsilonAbsolute = 1e-10;
  if (fabs(y) < epsilonAbsolute) 
    return fabs(x - y) < epsilonAbsolute;
  else
    return fabs(x / y - 1.) < epsilonRelative;
}
