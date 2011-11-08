#pragma GCC diagnostic ignored "-Wwrite-strings" //needed to get rid of pesky "deprecated conversion from string constant to char *" compilation error
// #include "PhysicsTools/TagAndProbe/interface/RooCBExGaussShape.h"
// #include "PhysicsTools/TagAndProbe/interface/ZGeneratorLineShape.h"
// #include "PhysicsTools/TagAndProbe/interface/RooCMSShape.h"
#include "JPsi/MuMu/interface/DummyRootClass.h"
#include "JPsi/MuMu/interface/DataDrivenBinning.h"
#include "JPsi/MuMu/interface/ModalInterval.h"
#include "JPsi/MuMu/interface/RooBifurGshPdf.h"
#include "JPsi/MuMu/interface/RooBifurSechPdf.h"
#include "JPsi/MuMu/interface/RooChi2Calculator.h"
#include "JPsi/MuMu/interface/RooCruijff.h"
#include "JPsi/MuMu/interface/RooGshPdf.h"
#include "JPsi/MuMu/interface/RooLogSqrtCBShape.h"
#include "JPsi/MuMu/interface/RooSechPdf.h"
#include "TVirtualFFT.h"

#ifdef __CINT__

//never even gets here...
#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;
//#pragma GCC diagnostic ignored "-Wformat"
// #pragma GCC diagnostic warning "-Wwrite-strings"

#pragma link C++ class cit::DummyRootClass;

#pragma link C++ class cit::DataDrivenBinning;
#pragma link C++ class cit::ModalInterval;
#pragma link C++ class cit::RooChi2Calculator;

#pragma link C++ class RooBifurGshPdf;
#pragma link C++ class RooBifurSechPdf;
#pragma link C++ class RooCruijff;
#pragma link C++ class RooGshPdf;
#pragma link C++ class RooLogSqrtCBShape;
#pragma link C++ class RooSechPdf;

#pragma link C++ global gROOT;
#pragma link C++ global gEnv;

#endif
