#include "JPsi/MuMu/interface/RooCruijff.h"
#include "JPsi/MuMu/interface/RooSechPdf.h"

namespace jpsimumu {
  struct dictionary {
    RooCruijff _cruijff;
    RooSechPdf _sech;
  };
}
