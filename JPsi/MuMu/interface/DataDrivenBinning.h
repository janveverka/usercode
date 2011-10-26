#ifndef JPSI_MUMU_DATADRIVENBINNING_H
#define JPSI_MUMU_DATADRIVENBINNING_H

#include "TObject.h"

namespace cit {
  class DataDrivenBinning : public TObject {
    public:
      DataDrivenBinning();
      virtual ~DataDrivenBinning();

      /// Make this a ROOT class.
      ClassDef(DataDrivenBinning,0)

  };  /// end of declaration of class DataDrivenBinning
} /// end of namespace cit

#endif
