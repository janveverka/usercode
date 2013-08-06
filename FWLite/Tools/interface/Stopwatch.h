/**
 * Definition of \class Stopwatch inherited from
 * TStopwatch to extend the functionality with conversion of the
 * time to human readable format.
 *
 * TODO: Add reporting on the event processing? (or in a new class)
 *
 * Jan Veverka, MIT, jan.veverka@cern.ch
 * 05 August 2013.
 */

#ifndef FWLite_Tools_Stopwatch_h
#define FWLite_Tools_Stopwatch_h

#include <string>
#include "TStopwatch.h"

//_____________________________________________________________________________
class Stopwatch : public TStopwatch {
public:
  Stopwatch() : TStopwatch() {}
  Stopwatch(const Stopwatch& other) : TStopwatch(other) {}
  ~Stopwatch() {}
  std::string humanReadableCpuTime();
  std::string humanReadableRealTime();
  std::string humanReadableTime(Double_t) const;
}; // class Stopwatch

#endif // ifndef FWLite_Tools_Stopwatch_h