/**
 * \brief Unit test of the VgCandidate class.
 * \author Jan Veverka, Caltech
 * \date 15 September 2012
 */

#include <assert.h>
#include <math.h>
#include "TLorentzVector.h"
#include "Vgamma/Analysis/interface/VgCandidate.h"

bool areEqual(double x, double y);
int main(int, char **);

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

  otherCand.setPt(cand.pt() + 10.);
  assert(otherCand != cand);
  assert(otherCand.eta() == cand.eta());
  assert(otherCand.phi() == cand.phi());
  assert(areEqual(otherCand.m  (), cand.m  ()));

  return 0;
} // int main(..)


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
