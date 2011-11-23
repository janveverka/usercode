#include "JPsi/MuMu/interface/DummyRootClass.h"
#include "JPsi/MuMu/interface/DataDrivenBinning.h"
#include "JPsi/MuMu/interface/ModalInterval.h"
#include "JPsi/MuMu/interface/RooBifurGshPdf.h"
#include "JPsi/MuMu/interface/RooBifurSechPdf.h"
#include "JPsi/MuMu/interface/RooChi2Calculator.h"
#include "JPsi/MuMu/interface/RooCruijff.h"
#include "JPsi/MuMu/interface/RooGshPdf.h"
#include "JPsi/MuMu/interface/RooLogSqrtCBShape.h"
#include "JPsi/MuMu/interface/RooLogSqrtGaussian.h"
#include "JPsi/MuMu/interface/RooSechPdf.h"

namespace jpsimumu {
  struct toolDict {
    cit::DataDrivenBinning _ddb;
    cit::ModalInterval     _mi;
    cit::DummyRootClass    _drc;
    cit::RooChi2Calculator _rcc;
  };

  struct pdfDict {
    RooBifurGshPdf  _bgsh;
    RooBifurSechPdf _bsech;
    RooCruijff      _cruijff;
    RooGshPdf       _gsh;
    RooSechPdf      _sech;
    RooLogSqrtCBShape _lscb;
    RooLogSqrtGaussian   _lsg;
  };
}
