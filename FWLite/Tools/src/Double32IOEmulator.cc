#include "FWLite/Tools/interface/Double32IOEmulator.h"
/**
  * Implementation of \class Double32IOEmulator
  * Jan Veverka, MIT, 23 October 2013
  */

#include <iostream>

/// Make this a ROOT class
ClassImp(Double32IOEmulator)

///----------------------------------------------------------------------------
/// Constructor
Double32IOEmulator::Double32IOEmulator(Int_t nbits) :
  nbits_(nbits)
{}


///----------------------------------------------------------------------------
/// Destructor
Double32IOEmulator::~Double32IOEmulator()
{}


///----------------------------------------------------------------------------
Double_t
Double32IOEmulator::operator()(Double32_t x)
{
  // Emulate the streaming of Double32_t to a file, extracted from:
  // TBufferFile::WriteDouble32(...)
  union {
    Float_t xx;
    Int_t   ix;
  };

  xx = (Float_t) x;
  UChar_t  theExp = (UChar_t) (0x000000ff & ((ix << 1) >> 24));
  UShort_t theMan = ((1 << (nbits_ + 1)) - 1) & (ix >> (23 - nbits_ -1));
  theMan++;
  theMan = theMan >> 1;
  
  if (theMan & 1 << nbits_) {
    theMan = (1 << nbits_) - 1;
  }
  
  if (xx < 0) {
    theMan |= 1 << (nbits_ + 1);
  }

  // Emulate the reading of Double32_t from a file, extracted from:
  // TBufferFile::ReadWithNbits(...)
  ix = theExp;
  ix <<= 23;
  ix |= (theMan & ((1 << (nbits_ + 1)) - 1)) << (23 - nbits_);

  if (1 << (nbits_ + 1) & theMan) {
    xx = -xx;
  }

  return (Double_t) xx;

} 
