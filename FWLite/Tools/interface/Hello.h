/**
 * \file FWLite/Tools/interface/Hello.h
 * \class fwlite::tools::Hello
 *
 * \brief Dummy class to test the testing with CppUnit
 *        Writes "hello, world!" to a stream by overloading >>.
 *
 * \author Jan Veverka, MIT, jan.veverka@cern.ch
 * \date 7 August 2013
 */

#ifndef FWLite_Tools_Hello_h
#define FWLite_Tools_Hello_h

#include <ostream>
#include <string>

namespace fwlite {
  namespace tools {
    
    //__________________________________________________________________________
    class Hello {
      public:
        Hello (std::string message = "hello, world!") : message_(message) {}
        void print(std::ostream&) const;
      private:
        std::string message_;
    }; // class Hello
    
  } // namespace tools
} // namespace fwlite

std::ostream&
operator<<(std::ostream&, fwlite::tools::Hello const&);


#endif // ifndef FWLite_Tools_Hello_h