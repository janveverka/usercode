/**
 * \file FWLite/Tools/src/Hello.cc
 * \class fwlite::tools::Hello
 *
 * \brief Implementation
 *
 * \author Jan Veverka, MIT, jan.veverka@cern.ch
 * \date 7 August 2013
 */

#include "FWLite/Tools/interface/Hello.h"

using fwlite::tools::Hello;

//__________________________________________________________________________
void
Hello::print(std::ostream& out) const
{
  out << message_;
} // Hello::print(std::ostream& out)


//__________________________________________________________________________
std::ostream&
operator<<(std::ostream& out, Hello const& hello)
{
  hello.print(out);
  return out;
} // operator<<(std::ostream& out, const Hello& hello)


