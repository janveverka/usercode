#ifndef FWLITE_TOOLS_LINKDEF_H
#define FWLITE_TOOLS_LINKDEF_H
//needed to get rid of pesky "deprecated conversion from string constant to char *" compilation error
#pragma GCC diagnostic ignored "-Wwrite-strings" 

#include "FWLite/Tools/interface/DataDrivenBinning.h"
#include "FWLite/Tools/interface/ModalInterval.h"
#include "FWLite/Tools/interface/RooChi2Calculator.h"

#ifdef __CINT__

//never even gets here...
#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;
//#pragma GCC diagnostic ignored "-Wformat"
// #pragma GCC diagnostic warning "-Wwrite-strings"


#pragma link C++ class DataDrivenBinning;
#pragma link C++ class ModalInterval;
#pragma link C++ class RooChi2Calculator;

#pragma link C++ global gROOT;
#pragma link C++ global gEnv;

#endif
#endif
