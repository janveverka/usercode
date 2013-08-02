#include "FWLite/Tools/interface/DummyRootClass.h"
/**
  * Implementation of \class DummyRootClass
  * Originally written in the JPsi/MuMu package
  * Jan Veverka, MIT, 2 August 2013
  */

#include <iostream>

/// Make this a ROOT class
ClassImp(DummyRootClass)

///----------------------------------------------------------------------------
/// Constructor
DummyRootClass::DummyRootClass()
{}


///----------------------------------------------------------------------------
/// Destructor
DummyRootClass::~DummyRootClass()
{}


///----------------------------------------------------------------------------
/// Example method. Prints some information about adding new classes to ROOT
/// in the standard output.
void
DummyRootClass::about()
{
  std::cout <<
    "This is a dummy class demonstrating how to add a new class to ROOT\n"
    "and use it with PyROOT.\n"
    "It lives in UserCode/JanVeverka/FWLite/Tools corresponding to the package\n"
    "FWLite/Tools.  Modify accordingly for the package at hand."
    "Relative to `$CMSSW_BASE/src/FWLite/Tools', the files that are\n"
    "involved in the process are:\n"
    "  1. interface/DummyRootClass.h\n"
    "  2. src/DummyRootClass.cc\n"
    "  3. src/LinkDef.h\n"
    "  4. src/classes.h\n"
    "  5. src/classes_def.xml\n"
    "  6. BuildFile.xml\n"
    "  7. python/dummyrootclass.py\n"
    "\n"
    "To print this message in PyROOT, you can do:\n"
    "  from FWLite.Tools.dummyrootclass import DummyRootClass\n"
    "  dummy = DummyRootClass()\n"
    "  dummy.about()\n";
} /// end of about()
