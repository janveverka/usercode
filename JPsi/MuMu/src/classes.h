#include "JPsi/MuMu/interface/RooCruijff.h"
#include "JPsi/MuMu/interface/RooSechPdf.h"
#include "JPsi/MuMu/interface/RooGshPdf.h"

namespace jpsimumu {
  struct dictionary {
    RooCruijff _cruijff;
    RooSechPdf _sech;
    RooGshPdf _gsh;
  };
}
