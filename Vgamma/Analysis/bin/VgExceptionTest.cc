/**
 * \brief Unit test of the VgException class.
 * \author Jan Veverka, Caltech
 * \date 15 September 2012
 */

#include <assert.h>
#include <iostream>
#include "FWCore/Utilities/interface/Exception.h"

using namespace std;
typedef cms::Exception Bad;

//_____________________________________________________________________________
/**
 * Main entry point of execution
 */
int 
main(int argc, char **argv) {
  try {
    throw Bad("Test") << "thrown test cms::Exception in " << __FUNCTION__ 
			<< " on line " << __LINE__;
  } catch (std::exception& e) {
    // cout << "Caught test exception: " << e.what() << endl;
    ;
  }

  try {
    throw Bad("Test1");
  } catch (std::exception& e) {
    // cout << "Caught test exception: " << e.what() << endl;
    assert(string(e.what()).find("Test1") != string::npos);
  }

  return 0;
} // int main(..)


