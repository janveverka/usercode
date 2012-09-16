/**
 * \class VgException
 * \brief Exceptions thrown by the Vgamma analysis code.
 * Can pass the location string in the constructor and message with
 * a left bit shift operator like this
 * throw VgException("VgException.h:5 what()") << "What did just happen?";
 *
 * \author Jan Veverka, Caltech
 * \date 16 September 2012.
 */

#ifndef Vgamma_Analysis_VgException_h
#define Vgamma_Analysis_VgException_h

#include <exception>
#include <iostream>
#include <sstream>
#include <string>
#include <boost/shared_ptr.hpp>

namespace cit {

  class VgException: public std::exception {
  public:
    typedef boost::shared_ptr<std::ostringstream> oss_ptr;
    typedef boost::shared_ptr<std::string> str_ptr;
    VgException(const char * where = "");
    VgException(VgException const&);
    ~VgException() throw() {}
    virtual const char* what() const throw();
    template<typename T>
    VgException & operator<<(T);
  private:
    str_ptr where_;
    oss_ptr what_;
  }; // class VgException

} // namespace cit

using cit::VgException;

//______________________________________________________________________________
/// Default ctor 
VgException::VgException(const char* where) :
  std::exception(),
  where_(new std::string(where)),
  what_(new std::ostringstream())
{} // Default ctor


//______________________________________________________________________________
/// Copy ctor 
VgException::VgException(VgException const& src) :
  std::exception(),
  where_(src.where_),
  what_(src.what_)
{} // Copy ctor


//______________________________________________________________________________
/// Behave like an output stream
template<typename T>
VgException &
VgException::operator<<(T what)
{
  (*what_) << what;
  return *this;
} // operator<<(..)


//______________________________________________________________________________
/// Error message
const char*
VgException::what() const throw()
{
  std::string message = *where_;
  if (what_->str() != std::string("")) message += ": ";
  message += what_->str();
  return message.c_str();
} // what()

#endif // #define Vgamma_Analysis_VgException_h
