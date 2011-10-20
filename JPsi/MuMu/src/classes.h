#include "JPsi/MuMu/interface/RooCruijff.h"
#include "JPsi/MuMu/interface/RooSechPdf.h"
#include "JPsi/MuMu/interface/RooBifurSechPdf.h"
#include "JPsi/MuMu/interface/RooGshPdf.h"

namespace jpsimumu {
  struct dictionary {
    RooCruijff _cruijff;
    RooSechPdf _sech;
    RooSechPdf _bsech;
    RooGshPdf _gsh;
  };
}
