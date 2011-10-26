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
  x_(last - first), min_(min), max_(max), boundaries_(0), medians_(0)
{}


///----------------------------------------------------------------------------
DataDrivenBinning::DataDrivenBinning(size_t n, double* first,
                                     size_t min, size_t max) :
  x_(n), min_(min), max_(max), boundaries_(0), medians_(0)
{}


///----------------------------------------------------------------------------
DataDrivenBinning::DataDrivenBinning(std::vector<double> const & data,
                                     size_t min, size_t max) :
  x_(data), min_(min), max_(max), boundaries_(0), medians_(0)
{}


///----------------------------------------------------------------------------
DataDrivenBinning::~DataDrivenBinning()
{}


///----------------------------------------------------------------------------
/// The MEAT.
void
DataDrivenBinning::get()
{}



