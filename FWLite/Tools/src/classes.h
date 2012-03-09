#ifndef FWLITE_TOOLS_CLASSES_H
#define FWLITE_TOOLS_CLASSES_H

#include "FWLite/Tools/interface/DataDrivenBinning.h"
#include "FWLite/Tools/interface/ModalInterval.h"
#include "FWLite/Tools/interface/RooChi2Calculator.h"

// namespace cit {
  struct toolDict {
    DataDrivenBinning _ddbins;
    ModalInterval     _mi;
    RooChi2Calculator _dummyChi2Calculator;
  };
// }

#endif
