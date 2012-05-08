#ifndef FWLITE_TOOLS_LINKDEF_H
#define FWLITE_TOOLS_LINKDEF_H
//needed to get rid of pesky "deprecated conversion from string constant to char *" compilation error
#pragma GCC diagnostic ignored "-Wwrite-strings" 

#include "FWLite/Tools/interface/DataDrivenBinning.h"
#include "FWLite/Tools/interface/ModalInterval.h"
#include "FWLite/Tools/interface/RooChi2Calculator.h"
#include "FWLite/Tools/interface/RooRelativisticBreitWigner.h"
#include "FWLite/Tools/interface/RooRhoKeysPdf.h"
#include "FWLite/Tools/interface/tools.h"

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
#pragma link C++ class RooRelativisticBreitWigner;
#pragma link C++ class RooRhoKeysPdf;

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
