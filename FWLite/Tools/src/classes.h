#ifndef FWLITE_TOOLS_CLASSES_H
#define FWLITE_TOOLS_CLASSES_H

#include "FWLite/Tools/interface/DataDrivenBinning.h"
#include "FWLite/Tools/interface/ModalInterval.h"

// namespace cit {
  struct toolDict {
    DataDrivenBinning _ddbins;
    ModalInterval     _mi;
  };
// }

#endif
