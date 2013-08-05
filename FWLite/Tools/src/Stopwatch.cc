/**
 * Implementation of \class Stopwatch
 * 
 * Jan Veverka, MIT, jan.veverka@cern.ch
 * 05 August 2013.
 */

#include <tgmath.h>
#include "FWLite/Tools/interface/Stopwatch.h"

//_____________________________________________________________________________
/**
 * Returns the elapsed CPU time as a human readable string.
 */
std::string
Stopwatch::humanReadableCpuTime()
{  
  return humanReadableTime(TStopwatch::CpuTime());
} // std::string humanReadableCpuTime()


//_____________________________________________________________________________
/**
 * Returns the elapsed real time as a human readable string.
 */
std::string
Stopwatch::humanReadableRealTime()
{  
  return humanReadableTime(TStopwatch::RealTime());
} // std::string humanReadableRealTime()


//_____________________________________________________________________________
/**
 * Converts the given time in seconds to a human readable string.
 */
std::string
Stopwatch::humanReadableTime(Double_t timeInSeconds) const
{  
  char buffer[64];
  sprintf(buffer, "%01.0f:%02.0f:%02.1f", 
          floor(timeInSeconds / 3600.), 
          floor(fmod(timeInSeconds, 3600.) / 60.),
          fmod(timeInSeconds, 60.));
  return std::string(buffer);
} // std::string humanReadableTime()
