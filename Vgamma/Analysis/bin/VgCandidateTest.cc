/**
 * \brief Unit test of the VgCandidate class.
 * \author Jan Veverka, Caltech
 * \date 15 September 2012
 */

#include <assert.h>
#include "TLorentzVector.h"
#include "Vgamma/Analysis/interface/VgCandidate.h"

//_____________________________________________________________________________
/**
 * Main entry point of execution
 */
int main(int argc, char **argv) {
  typedef cit::VgCandidate Cand;
  Cand cand;
  
  assert(cand.momentum() == TLorentzVector(0, 0, 0, 0));
  assert(cand.type() == Cand::kCombined);
  assert(cand.weight() == 1.);
  assert(cand.charge() == 0);

  TLorentzVector v1(1, 2, 3, 4);
  cand.setMomentum(v1);
  assert(cand.momentum() == v1);

  cand.setType(Cand::kPhoton);
  assert(cand.type() == Cand::kPhoton);

  cand.scaleWeight(0.9);
  cand.scaleWeight(1.2);
  assert(cand.weight() == 1. * 0.9 * 1.2);
  
  cand.setCharge(1);
  assert(cand.charge() == 1);
  
  Cand otherCand(cand);
  assert(cand == otherCand);

  return 0;
} // int main(..)
