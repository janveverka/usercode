/**
  * This is just a boiler plate for adding new classes to ROOT and
  * using scram/gcc for compilation.
  * Jan Veverka, Caltech,  26 October 2011
  */

#include "JPsi/MuMu/interface/DataDrivenBinning.h"

using namespace cit;

/// Make this a ROOT class
ClassImp(DataDrivenBinning)

///----------------------------------------------------------------------------
/// Default constructor
DataDrivenBinning::DataDrivenBinning()
{}


///----------------------------------------------------------------------------
DataDrivenBinning::DataDrivenBinning(const_iterator first, const_iterator last,
                                     size_t min, size_t max) :
  updated_(false), x_(first <= last ? last - first : 0), min_(min), max_(max),
  boundaries_(0), medians_(0)
{
  readData(first, last);
}


///----------------------------------------------------------------------------
DataDrivenBinning::DataDrivenBinning(size_t n, double* first,
                                     size_t min, size_t max) :
  updated_(false), x_(n), min_(min), max_(max), boundaries_(0), medians_(0)
{
  readData(first, first+n);
}


///----------------------------------------------------------------------------
DataDrivenBinning::DataDrivenBinning(std::vector<double> const & data,
                                     size_t min, size_t max) :
  updated_(false), x_(data), min_(min), max_(max), boundaries_(0), medians_(0)
{
  std::sort(x_.begin(), x_.end());
}


///----------------------------------------------------------------------------
DataDrivenBinning::~DataDrivenBinning()
{}


///----------------------------------------------------------------------------
void
DataDrivenBinning::readData(size_t n, double* first) {
  readData(first, first + n);
}


///----------------------------------------------------------------------------
void
DataDrivenBinning::readData(std::vector<double> const& data) {
  readData(data.begin(), data.end());
}


///----------------------------------------------------------------------------
/// The MEAT.
void
DataDrivenBinning::get()
{}



