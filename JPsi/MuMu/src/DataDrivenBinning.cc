/**
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
                                     size_t minBinContent,
				     size_t maxBinContent) :
  ModalInterval(first, last, 1.), minBinContent_(minBinContent),
  maxBinContent_(maxBinContent), boundaries_(0), medians_(0)
{}


///----------------------------------------------------------------------------
DataDrivenBinning::DataDrivenBinning(size_t n, double* first,
                                     size_t minBinContent,
				     size_t maxBinContent) :
  ModalInterval(n, first, 1.), minBinContent_(minBinContent),
  maxBinContent_(maxBinContent), boundaries_(0), medians_(0)
{}


///----------------------------------------------------------------------------
DataDrivenBinning::DataDrivenBinning(std::vector<double> const & data,
                                     size_t minBinContent, size_t maxBinContent) :
  ModalInterval(data, 1.), minBinContent_(minBinContent),
  maxBinContent_(maxBinContent), boundaries_(0), medians_(0)
{}


///----------------------------------------------------------------------------
DataDrivenBinning::~DataDrivenBinning()
{}


///----------------------------------------------------------------------------
/// The MEAT.
void
DataDrivenBinning::get()
{}

