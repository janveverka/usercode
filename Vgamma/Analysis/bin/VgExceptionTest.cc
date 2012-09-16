/**
 * \brief Unit test of the VgException class.
 * \author Jan Veverka, Caltech
 * \date 15 September 2012
 */

#include <iostrea>
#include "Vgamma/Analysis/interface/VgException.h"
using namespace std;
typedef cit::VgException Bad;

//_____________________________________________________________________________
/**
 * Main entry point of execution
 */
int 
main(int argc, char **argv) {
  try {
    throw Bad(__FILE__) << "thrown test VgException in " << __FUNCTION__ 
			<< " on line " << __LINE__;
  } catch (VgException& e) {
    // cout << "Caught test exception: " << e.what() << endl;
  }

  try {
    throw Bad("test1");
  } catch (VgException& e) {
    assert(string("test1") == e.what());
  }

  return 0;
} // int main(..)


