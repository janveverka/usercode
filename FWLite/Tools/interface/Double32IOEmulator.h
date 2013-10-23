#ifndef FWLITE_TOOLS_DOUBLE32IOEMULATOR_H
#define FWLITE_TOOLS_DOUBLE32IOEMULATOR_H

#include "Rtypes.h"
#include "TObject.h"

/**
  * Class for emulation of Double32_t ROOT Input/Output
  * Jan Veverka, MIT,  23 October 2013
  */

class Double32IOEmulator : public TObject {
public:
  Double32IOEmulator(Int_t nbits=14);
  virtual ~Double32IOEmulator();

  /// Print info about this class.
  Double_t operator()(Double_t x);

  /// Make this a ROOT class.
  /// Use 1 as the 2nd arg to store class in a ROOT file.
  ClassDef(Double32IOEmulator,0)
private:
  Int_t nbits_;
};  /// End of declaration of class Double32IOEmulator

#endif
