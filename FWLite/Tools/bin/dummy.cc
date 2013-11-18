/**
 * Tests DummyRootClassTemplate.
 * Jan Veverka, MIT, 18 November 2013
 */

#include <iostream>
#include "FWLite/Tools/interface/DummyRootClassTemplate.tpp"
#include "FWLite/Tools/interface/DummyIntRootClass.h"
#include "FWLite/Tools/interface/DummyIntRootClass2.h"

using fwlite::DummyRootClassTemplate;

// Derived from DummyRootClassTemplate<Int_t> using only its header file.
// Has own implementation and header files and dictionary (?).
using fwlite::DummyIntRootClass;

// typedef of DummyRootClassTemplate<Int_t> using only its header file
// Has own implementation and header files and dictionary (?).
using fwlite::DummyIntRootClass2;

// typdef of DummyRootClassTemplate<Int_t> in the *LinkDef.h file.
// Has no implentation nor header files but does have a dictionary (?).
typedef DummyRootClassTemplate<Int_t> DummyIntRootClass3;

// Defined only here.
// Has neither the implementation nor header files nor dictionary (?).
typedef DummyRootClassTemplate<Int_t> DummyIntRootClass4;

//_____________________________________________________________________________
int main(int argc, char **argv) {
  DummyRootClassTemplate<Float_t> fdummy (1.2);
  DummyRootClassTemplate<Int_t  > idummy (1);
  DummyIntRootClass2              idummy2(2);
  DummyIntRootClass3              idummy3(3);
  DummyIntRootClass4              idummy4(4);

  std::cout << fdummy .Class_Name() << " "; fdummy .printData();
  std::cout << idummy .Class_Name() << " "; idummy .printData();
  std::cout << idummy2.Class_Name() << " "; idummy2.printData();
  std::cout << idummy3.Class_Name() << " "; idummy3.printData();
  std::cout << idummy4.Class_Name() << " "; idummy4.printData();

  return 0;
} 

