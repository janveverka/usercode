#include "JPsi/MuMu/interface/RooBifurGshPdf.h"
#include "JPsi/MuMu/interface/RooBifurSechPdf.h"
#include "JPsi/MuMu/interface/RooCruijff.h"
#include "JPsi/MuMu/interface/RooGshPdf.h"
#include "JPsi/MuMu/interface/RooSechPdf.h"

namespace jpsimumu {
  struct dictionary {
    RooBifurGshPdf  _bgsh;
    RooBifurSechPdf _bsech;
    RooCruijff      _cruijff;
    RooGshPdf       _gsh;
    RooSechPdf      _sech;
  };
}
