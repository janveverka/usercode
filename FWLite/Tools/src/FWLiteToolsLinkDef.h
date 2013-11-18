#ifndef FWLITE_TOOLS_LINKDEF_H
#define FWLITE_TOOLS_LINKDEF_H
// needed to get rid of pesky "deprecated conversion from
// string constant to char *" compilation error
#pragma GCC diagnostic ignored "-Wwrite-strings" 

#include "FWLite/Tools/interface/DataDrivenBinning.h"
#include "FWLite/Tools/interface/DummyRootClass.h"
#include "FWLite/Tools/interface/DummyIntRootClass.h"
#include "FWLite/Tools/interface/DummyIntRootClass2.h"
#include "FWLite/Tools/interface/DummyRootClassTemplate.tpp"
#include "FWLite/Tools/interface/Double32IOEmulator.h"
#include "FWLite/Tools/interface/GraphInterpolationFunctor.h"
#include "FWLite/Tools/interface/ModalInterval.h"
#include "FWLite/Tools/interface/RooChi2Calculator.h"
#include "FWLite/Tools/interface/RooRelativisticBreitWigner.h"
#include "FWLite/Tools/interface/RooRhoKeysPdf.h"
#include "FWLite/Tools/interface/RooNumInverse.h"
#include "FWLite/Tools/interface/tools.h"

#ifdef __CINT__

namespace fwlite {
  typedef DummyRootClassTemplate<Int_t> DummyIntRootClass3;
  ClassImp(DummyFloatRootClass3)
}

//never even gets here...
#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;
#pragma link C++ nestedclass;
#pragma link C++ nestedtypedef;
#pragma link C++ namespace fwlite;
//#pragma GCC diagnostic ignored "-Wformat"
// #pragma GCC diagnostic warning "-Wwrite-strings"

#pragma link C++ class DataDrivenBinning;
#pragma link C++ class DummyRootClass;
#pragma link C++ class fwlite::DummyRootClassTemplate<Int_t>+;
#pragma link C++ class fwlite::DummyRootClassTemplate<Float_t>+;
/** The line below causes the following error (bug in ROOT?):
 *  Syntax error /home/veverka/cms/cmssw/031/CMSSW_5_3_10_patch1/src/FWLite/Tools/interface/DummyRootClassTemplate.h:16:
 *  Error: Symbol unsignedint fData is not defined in current scope  /home/veverka/cms/cmssw/031/CMSSW_5_3_10_patch1/src/FWLite/Tools/interface/DummyRootClassTemplate.h:23:
 *  Syntax error /home/veverka/cms/cmssw/031/CMSSW_5_3_10_patch1/src/FWLite/Tools/interface/DummyRootClassTemplate.tpp:19:
 */
//#pragma link C++ class fwlite::DummyRootClassTemplate<UInt_t>+;
#pragma link C++ class fwlite::DummyIntRootClass;
#pragma link C++ class fwlite::DummyIntRootClass2;
#pragma link C++ class fwlite::DummyIntRootClass3;
#pragma link C++ class Double32IOEmulator;
#pragma link C++ class GraphInterpolationFunctor;
#pragma link C++ class ModalInterval;
#pragma link C++ class RooChi2Calculator;
#pragma link C++ class RooRelativisticBreitWigner;
#pragma link C++ class RooRhoKeysPdf;
#pragma link C++ class RooNumInverse;

#pragma link C++ global gROOT;
#pragma link C++ global gEnv;

#pragma link C++ function effSigma(TH1*);
#pragma link C++ function zMassPdg();
#pragma link C++ function Oplus(Double_t, Double_t);
#pragma link C++ function Oplus(Double_t, Double_t, Double_t);
#pragma link C++ function muonSigmaPtOverPt(Double_t, Double_t);
#pragma link C++ function photonSigmaEOverE(Double_t, Double_t);
#pragma link C++ function photonSigmaPtOverPt(Double_t, Double_t);
#pragma link C++ function phoEtrue(Double_t);
#pragma link C++ function phoEmeas(Double_t, Double_t);
#pragma link C++ function kRatio(Double_t, Double_t);
#pragma link C++ function inverseK(Double_t, Double_t);
#pragma link C++ function scaledMmgMass10(Double_t, Double_t, Double_t,\
                                          Double_t, Double_t, Double_t,\
                                          Double_t, Double_t, Double_t,\
                                          Double_t);
#pragma link C++ function scaledMmgMass3(Double_t, Double_t, Double_t);
#pragma link C++ function scaledDimuonPhotonMass(Double_t, Double_t, Double_t,\
                                                 Double_t, Double_t, Double_t,\
                                                 Double_t, Double_t);
#pragma link C++ function twoBodyMass(Double_t, Double_t, Double_t, Double_t,\
                                      Double_t, Double_t, Double_t, Double_t);
#pragma link C++ function threeBodyMass(Double_t, Double_t, Double_t, Double_t,\
                                        Double_t, Double_t, Double_t, Double_t,\
                                        Double_t, Double_t, Double_t, Double_t);
#pragma link C++ function phoSmearE(Double_t, Double_t, Double_t, Double_t,\
                                    Double_t, Double_t)
#pragma link C++ function phoSmearF(Double_t, Double_t, Double_t, Double_t,\
                                    Double_t, Double_t)
#pragma link C++ function mmgMassPhoSmearE(Double_t, Double_t, Double_t,\
                                           Double_t, Double_t, Double_t,\
                                           Double_t, Double_t)

#endif
#endif
